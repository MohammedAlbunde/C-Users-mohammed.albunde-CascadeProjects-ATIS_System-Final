import serial
import time
import logging
from datetime import datetime
import threading
from queue import PriorityQueue
import os
from pathlib import Path
import json
import wave
import pyaudio
import numpy as np
from gtts import gTTS
import pyttsx3

class VHFRadio:
    def __init__(self, config=None):
        self.config = config
        self.com_port = config.get("radio", "com_port") if config else None
        self.baud_rate = config.get("radio", "baud_rate") if config else 9600
        self.frequency = config.get("radio", "frequency") if config else 118.0
        self.power = config.get("radio", "power") if config else "high"
        
        self.serial_connection = None
        self.ptt_enabled = False
        self.message_queue = PriorityQueue()
        self.running = True
        self.last_broadcast = None
        self.broadcast_count = 0
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        if config and config.get("radio", "voice", "voice_id"):
            self.tts_engine.setProperty('voice', config.get("radio", "voice", "voice_id"))
        self.tts_engine.setProperty('rate', config.get("radio", "voice", "rate") if config else 150)
        self.tts_engine.setProperty('volume', config.get("radio", "voice", "volume") if config else 1.0)
        
        # Setup logging
        self.setup_logging()
        
        # Connect to radio hardware
        self.connect()
        
        # Start broadcast thread
        self.broadcast_thread = threading.Thread(target=self._broadcast_worker, daemon=True)
        self.broadcast_thread.start()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_worker, daemon=True)
        self.monitor_thread.start()
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "vhf_radio.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("VHF")
    
    def connect(self):
        """Connect to VHF radio hardware"""
        if self.com_port:
            try:
                self.serial_connection = serial.Serial(
                    port=self.com_port,
                    baudrate=self.baud_rate,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1
                )
                self.logger.info(f"Connected to VHF radio on {self.com_port}")
                
                # Initialize radio
                self.set_frequency(self.frequency)
                self.set_power(self.power)
                return True
            except Exception as e:
                self.logger.error(f"Failed to connect to VHF radio: {str(e)}")
        return False
    
    def set_frequency(self, frequency):
        """Set VHF radio frequency"""
        if not 118.0 <= frequency <= 137.0:
            raise ValueError("Frequency must be between 118.0 and 137.0 MHz")
        
        self.frequency = frequency
        if self.serial_connection:
            try:
                # Format may vary by radio model
                command = f"FREQ {frequency:.3f}\r\n"
                self.serial_connection.write(command.encode())
                self.logger.info(f"Set frequency to {frequency:.3f} MHz")
                return True
            except Exception as e:
                self.logger.error(f"Failed to set frequency: {str(e)}")
        return False
    
    def set_power(self, power):
        """Set radio power level"""
        if power not in ["low", "medium", "high"]:
            raise ValueError("Power must be low, medium, or high")
        
        self.power = power
        if self.serial_connection:
            try:
                # Format may vary by radio model
                command = f"POWER {power.upper()}\r\n"
                self.serial_connection.write(command.encode())
                self.logger.info(f"Set power to {power}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to set power: {str(e)}")
        return False
    
    def enable_ptt(self):
        """Enable Push-to-Talk"""
        self.ptt_enabled = True
        if self.serial_connection:
            try:
                # Format may vary by radio model
                self.serial_connection.write(b"PTT ON\r\n")
                self.logger.info("PTT enabled")
                return True
            except Exception as e:
                self.logger.error(f"Failed to enable PTT: {str(e)}")
        return False
    
    def disable_ptt(self):
        """Disable Push-to-Talk"""
        self.ptt_enabled = False
        if self.serial_connection:
            try:
                # Format may vary by radio model
                self.serial_connection.write(b"PTT OFF\r\n")
                self.logger.info("PTT disabled")
                return True
            except Exception as e:
                self.logger.error(f"Failed to disable PTT: {str(e)}")
        return False
    
    def queue_message(self, message, priority=1):
        """Add message to broadcast queue"""
        try:
            # Generate audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"temp/message_{timestamp}.mp3"
            
            # Ensure temp directory exists
            Path("temp").mkdir(exist_ok=True)
            
            # Convert text to speech
            tts = gTTS(text=message, lang='en')
            tts.save(filename)
            
            # Add to queue with priority and timestamp
            self.message_queue.put((priority, timestamp, filename, message))
            self.logger.info(f"Message queued: {message[:50]}...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to queue message: {str(e)}")
            return False
    
    def _broadcast_worker(self):
        """Worker thread for broadcasting messages"""
        while self.running:
            try:
                if not self.message_queue.empty():
                    priority, timestamp, filename, message = self.message_queue.get()
                    
                    # Load audio file
                    if os.path.exists(filename):
                        # Enable PTT
                        self.enable_ptt()
                        time.sleep(0.5)  # Wait for PTT to engage
                        
                        # Play audio
                        os.system(f"start {filename}")
                        
                        # Wait for message duration (approximate)
                        words = len(message.split())
                        duration = (words * 0.4) + 1
                        time.sleep(duration)
                        
                        # Disable PTT
                        self.disable_ptt()
                        time.sleep(0.5)
                        
                        # Update broadcast stats
                        self.last_broadcast = datetime.now()
                        self.broadcast_count += 1
                        
                        # Log broadcast
                        self._log_broadcast(message)
                        
                        # Clean up
                        try:
                            os.remove(filename)
                        except:
                            pass
                    
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Broadcast error: {str(e)}")
                time.sleep(1)
    
    def _monitor_worker(self):
        """Worker thread for monitoring radio status"""
        while self.running:
            try:
                if self.serial_connection:
                    # Read radio status
                    status = self.serial_connection.readline().decode().strip()
                    if status:
                        self._parse_radio_status(status)
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Monitor error: {str(e)}")
                time.sleep(1)
    
    def _parse_radio_status(self, status):
        """Parse radio status message"""
        try:
            # Format may vary by radio model
            # Example: "STATUS:FREQ=118.000,PWR=HIGH,SWR=1.1,TEMP=35"
            if status.startswith("STATUS:"):
                parts = status[7:].split(",")
                for part in parts:
                    key, value = part.split("=")
                    if key == "TEMP" and float(value) > 50:
                        self.logger.warning(f"High radio temperature: {value}°C")
                    elif key == "SWR" and float(value) > 2.0:
                        self.logger.warning(f"High SWR: {value}")
        except Exception as e:
            self.logger.error(f"Status parsing error: {str(e)}")
    
    def _log_broadcast(self, message):
        """Log broadcast to file"""
        log_dir = Path("broadcast_logs")
        log_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"broadcast_log_{date_str}.csv"
        
        # Create new file with headers if needed
        if not log_file.exists():
            with open(log_file, 'w', newline='') as f:
                f.write("timestamp,frequency,power,message\n")
        
        # Log broadcast
        with open(log_file, 'a', newline='') as f:
            f.write(f"{datetime.now().isoformat()},{self.frequency:.3f},{self.power},{message}\n")
    
    def get_status(self):
        """Get radio status"""
        return {
            "frequency": self.frequency,
            "power": self.power,
            "ptt_enabled": self.ptt_enabled,
            "connected": bool(self.serial_connection),
            "last_broadcast": self.last_broadcast,
            "broadcast_count": self.broadcast_count,
            "queue_size": self.message_queue.qsize()
        }
    
    def close(self):
        """Clean up resources"""
        self.running = False
        self.disable_ptt()
        if self.serial_connection:
            self.serial_connection.close()
        
        # Clean up temp files
        try:
            for file in Path("temp").glob("message_*.mp3"):
                os.remove(file)
        except:
            pass
        
        self.logger.info("VHF radio system closed")
