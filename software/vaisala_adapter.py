import serial
import socket
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class VaisalaAdapter:
    """Adapter for Vaisala AWOS/RVR systems"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.logger = logging.getLogger('VaisalaAdapter')
        self.config = self._load_config(config_file)
        self.connection = None
        self.last_data = {}
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config.get('vaisala', {})
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}
            
    def connect(self) -> bool:
        """Establish connection to Vaisala system"""
        try:
            if self.config.get('connection_type') == 'serial':
                self.connection = serial.Serial(
                    port=self.config['com_port'],
                    baudrate=self.config['baud_rate'],
                    timeout=self.config.get('timeout', 1)
                )
            else:  # TCP/IP
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((
                    self.config['host'],
                    self.config['port']
                ))
            self.logger.info("Connected to Vaisala system")
            return True
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return False
            
    def _parse_awos_data(self, data: str) -> Dict[str, Any]:
        """Parse AWOS data from Vaisala format"""
        try:
            # Example Vaisala format:
            # $VAISALA,AWOS,20250126,174500,WIND=120/15KT,TEMP=25.5C,DEW=20.0C,...
            parts = data.split(',')
            if len(parts) < 4:
                return {}
                
            parsed = {
                'timestamp': f"{parts[2]}T{parts[3]}",
                'wind_direction': None,
                'wind_speed': None,
                'temperature': None,
                'dewpoint': None,
                'pressure': None,
                'visibility': None,
                'ceiling': None,
                'weather': None
            }
            
            for part in parts[4:]:
                if '=' in part:
                    key, value = part.split('=')
                    if key == 'WIND':
                        dir_speed = value.split('/')
                        parsed['wind_direction'] = int(dir_speed[0])
                        parsed['wind_speed'] = float(dir_speed[1].replace('KT',''))
                    elif key == 'TEMP':
                        parsed['temperature'] = float(value.replace('C',''))
                    elif key == 'DEW':
                        parsed['dewpoint'] = float(value.replace('C',''))
                    elif key == 'QNH':
                        parsed['pressure'] = float(value.replace('HPA',''))
                    elif key == 'VIS':
                        parsed['visibility'] = float(value.replace('M',''))
                    elif key == 'CEIL':
                        parsed['ceiling'] = float(value.replace('FT',''))
                    elif key == 'WX':
                        parsed['weather'] = value
                        
            return parsed
        except Exception as e:
            self.logger.error(f"Failed to parse AWOS data: {e}")
            return {}
            
    def _parse_rvr_data(self, data: str) -> Dict[str, Any]:
        """Parse RVR data from Vaisala format"""
        try:
            # Example: $VAISALA,RVR,20250126,174500,RWY=16,TD=800M,MP=750M,RO=800M
            parts = data.split(',')
            if len(parts) < 4:
                return {}
                
            parsed = {
                'timestamp': f"{parts[2]}T{parts[3]}",
                'runway': None,
                'touchdown': None,
                'midpoint': None,
                'rollout': None
            }
            
            for part in parts[4:]:
                if '=' in part:
                    key, value = part.split('=')
                    if key == 'RWY':
                        parsed['runway'] = value
                    elif key == 'TD':
                        parsed['touchdown'] = float(value.replace('M',''))
                    elif key == 'MP':
                        parsed['midpoint'] = float(value.replace('M',''))
                    elif key == 'RO':
                        parsed['rollout'] = float(value.replace('M',''))
                        
            return parsed
        except Exception as e:
            self.logger.error(f"Failed to parse RVR data: {e}")
            return {}
            
    def get_weather_data(self) -> Dict[str, Any]:
        """Get latest weather data from Vaisala system"""
        try:
            if not self.connection:
                if not self.connect():
                    return {}
                    
            # Read data
            if isinstance(self.connection, serial.Serial):
                data = self.connection.readline().decode('utf-8').strip()
            else:
                data = self.connection.recv(1024).decode('utf-8').strip()
                
            # Parse based on message type
            if data.startswith('$VAISALA,AWOS'):
                self.last_data.update(self._parse_awos_data(data))
            elif data.startswith('$VAISALA,RVR'):
                self.last_data.update(self._parse_rvr_data(data))
                
            return self.last_data
            
        except Exception as e:
            self.logger.error(f"Failed to get weather data: {e}")
            return {}
            
    def close(self):
        """Close connection to Vaisala system"""
        try:
            if self.connection:
                self.connection.close()
                self.logger.info("Connection closed")
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")
            
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
