import serial
import time
import random
import logging
from datetime import datetime
import json
import csv
from pathlib import Path
import threading
from queue import Queue
import numpy as np

class Sensor:
    def __init__(self, name, unit, min_val, max_val, precision):
        self.name = name
        self.unit = unit
        self.min_val = min_val
        self.max_val = max_val
        self.precision = precision
        self.value = None
        self.last_update = None
        self.status = "OK"
        self.history = []
        
    def update(self, value):
        """Update sensor value with validation"""
        try:
            value = float(value)
            if self.min_val <= value <= self.max_val:
                self.value = round(value, self.precision)
                self.last_update = datetime.now()
                self.status = "OK"
                self.history.append((self.last_update, self.value))
                if len(self.history) > 1000:  # Keep last 1000 readings
                    self.history.pop(0)
                return True
        except ValueError:
            self.status = "ERROR: Invalid value"
        return False
    
    def get_trend(self, minutes=30):
        """Calculate trend over specified minutes"""
        if len(self.history) < 2:
            return "STEADY"
            
        recent = [v for t, v in self.history if (datetime.now() - t).total_seconds() <= minutes * 60]
        if len(recent) < 2:
            return "STEADY"
            
        slope = np.polyfit([i for i in range(len(recent))], recent, 1)[0]
        
        if abs(slope) < 0.1:
            return "STEADY"
        elif slope > 0:
            return "RISING"
        else:
            return "FALLING"

class AWOS_RVR_System:
    def __init__(self, config=None):
        self.config = config
        self.com_port = config.get("awos", "com_port") if config else None
        self.baud_rate = config.get("awos", "baud_rate") if config else 9600
        self.serial_connection = None
        self.running = False
        self.data_queue = Queue()
        self.last_update = None
        
        # Initialize sensors
        self.sensors = {
            "wind_speed": Sensor("Wind Speed", "knots", 0, 99, 1),
            "wind_direction": Sensor("Wind Direction", "degrees", 0, 359, 0),
            "wind_gust": Sensor("Wind Gust", "knots", 0, 99, 1),
            "temperature": Sensor("Temperature", "°C", -30, 50, 1),
            "dewpoint": Sensor("Dewpoint", "°C", -30, 50, 1),
            "pressure": Sensor("Pressure", "hPa", 800, 1100, 1),
            "visibility": Sensor("Visibility", "meters", 0, 10000, 0),
            "ceiling": Sensor("Ceiling", "feet", 0, 99999, 0),
            "precipitation": Sensor("Precipitation", "mm/hr", 0, 999, 1),
            "rvr_touchdown": Sensor("RVR Touchdown", "meters", 0, 2000, 0),
            "rvr_midpoint": Sensor("RVR Midpoint", "meters", 0, 2000, 0),
            "rvr_rollout": Sensor("RVR Rollout", "meters", 0, 2000, 0)
        }
        
        # Setup logging
        self.setup_logging()
        
        # Connect to hardware
        self.connect()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_data, daemon=True)
        self.process_thread.start()
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "awos.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AWOS")
    
    def connect(self):
        """Connect to AWOS hardware"""
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
                self.logger.info(f"Connected to AWOS on {self.com_port}")
                self.running = True
                return True
            except Exception as e:
                self.logger.error(f"Failed to connect to AWOS: {str(e)}")
        return False
    
    def _process_data(self):
        """Process incoming data from AWOS"""
        while True:
            try:
                if self.serial_connection and self.serial_connection.is_open:
                    data = self.serial_connection.readline().decode().strip()
                    if data:
                        self.parse_data(data)
                else:
                    # Simulate data for testing
                    self._simulate_data()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Data processing error: {str(e)}")
                time.sleep(1)
    
    def parse_data(self, data):
        """Parse data from AWOS hardware"""
        try:
            # Example parsing for common AWOS format
            # Modify this based on your AWOS protocol
            parts = data.split(",")
            if len(parts) >= 12:
                self.sensors["wind_speed"].update(parts[0])
                self.sensors["wind_direction"].update(parts[1])
                self.sensors["temperature"].update(parts[2])
                self.sensors["dewpoint"].update(parts[3])
                self.sensors["pressure"].update(parts[4])
                self.sensors["visibility"].update(parts[5])
                self.sensors["ceiling"].update(parts[6])
                self.sensors["precipitation"].update(parts[7])
                self.sensors["rvr_touchdown"].update(parts[8])
                self.sensors["rvr_midpoint"].update(parts[9])
                self.sensors["rvr_rollout"].update(parts[10])
                self.sensors["wind_gust"].update(parts[11])
                
                self.last_update = datetime.now()
                self._log_data()
        except Exception as e:
            self.logger.error(f"Data parsing error: {str(e)}")
    
    def _simulate_data(self):
        """Generate simulated weather data for testing"""
        self.sensors["wind_speed"].update(random.uniform(5, 15))
        self.sensors["wind_direction"].update(random.uniform(0, 359))
        self.sensors["wind_gust"].update(random.uniform(10, 25))
        self.sensors["temperature"].update(random.uniform(15, 25))
        self.sensors["dewpoint"].update(random.uniform(10, 20))
        self.sensors["pressure"].update(random.uniform(1013, 1015))
        self.sensors["visibility"].update(random.uniform(5000, 10000))
        self.sensors["ceiling"].update(random.uniform(1000, 3000))
        self.sensors["precipitation"].update(random.uniform(0, 0.5))
        self.sensors["rvr_touchdown"].update(random.uniform(1500, 2000))
        self.sensors["rvr_midpoint"].update(random.uniform(1500, 2000))
        self.sensors["rvr_rollout"].update(random.uniform(1500, 2000))
        
        self.last_update = datetime.now()
        self._log_data()
    
    def _log_data(self):
        """Log sensor data to file"""
        log_dir = Path("data_logs")
        log_dir.mkdir(exist_ok=True)
        
        date_str = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"awos_data_{date_str}.csv"
        
        # Create new file with headers if it doesn't exist
        if not log_file.exists():
            headers = ["timestamp"] + [f"{name}_{field}" for name in self.sensors.keys() 
                                    for field in ["value", "unit", "status"]]
            with open(log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        
        # Log current values
        data = [datetime.now().isoformat()]
        for sensor in self.sensors.values():
            data.extend([sensor.value, sensor.unit, sensor.status])
        
        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    
    def get_weather_report(self):
        """Generate formatted weather report"""
        if not self.last_update or (datetime.now() - self.last_update).total_seconds() > 60:
            return "WARNING: Weather data may be outdated"
        
        report = []
        
        # Wind information
        wind_speed = self.sensors["wind_speed"].value
        wind_dir = self.sensors["wind_direction"].value
        wind_gust = self.sensors["wind_gust"].value
        
        report.append(f"WIND {wind_dir:03.0f} AT {wind_speed:.0f} KNOTS")
        if wind_gust and wind_gust > wind_speed + 5:
            report.append(f"GUSTING {wind_gust:.0f}")
        
        # Visibility
        vis = self.sensors["visibility"].value
        if vis is not None:
            vis_sm = vis * 0.000621371  # Convert meters to statute miles
            report.append(f"VISIBILITY {vis_sm:.1f} SM")
        
        # Ceiling
        ceiling = self.sensors["ceiling"].value
        if ceiling is not None:
            report.append(f"CEILING {ceiling:.0f} FT")
        
        # Temperature and dewpoint
        temp = self.sensors["temperature"].value
        dewpoint = self.sensors["dewpoint"].value
        if temp is not None and dewpoint is not None:
            temp_f = (temp * 9/5) + 32
            dewpoint_f = (dewpoint * 9/5) + 32
            report.append(f"TEMPERATURE {temp_f:.1f} F ({temp:.1f} C)")
            report.append(f"DEWPOINT {dewpoint_f:.1f} F ({dewpoint:.1f} C)")
        
        # Pressure
        pressure = self.sensors["pressure"].value
        if pressure is not None:
            altimeter = pressure * 0.02953  # Convert hPa to inHg
            report.append(f"ALTIMETER {altimeter:.2f} inHg ({pressure:.1f} hPa)")
        
        # Precipitation
        precip = self.sensors["precipitation"].value
        if precip is not None and precip > 0:
            report.append(f"PRECIPITATION {precip:.1f} MM/HR")
        
        # Trends
        temp_trend = self.sensors["temperature"].get_trend()
        pressure_trend = self.sensors["pressure"].get_trend()
        if temp_trend != "STEADY":
            report.append(f"TEMPERATURE {temp_trend}")
        if pressure_trend != "STEADY":
            report.append(f"PRESSURE {pressure_trend}")
        
        return " / ".join(report)
    
    def get_rvr_report(self):
        """Generate RVR report"""
        if not self.last_update or (datetime.now() - self.last_update).total_seconds() > 60:
            return "WARNING: RVR data may be outdated"
        
        report = []
        
        for position in ["touchdown", "midpoint", "rollout"]:
            rvr = self.sensors[f"rvr_{position}"].value
            if rvr is not None:
                rvr_ft = rvr * 3.28084  # Convert meters to feet
                report.append(f"RVR {position.upper()} {rvr_ft:.0f} FT")
        
        return " / ".join(report)
    
    def get_combined_report(self):
        """Generate combined ATIS report"""
        weather = self.get_weather_report()
        rvr = self.get_rvr_report()
        
        report = [
            "AUTOMATIC TERMINAL INFORMATION SERVICE",
            datetime.now().strftime("%H%M UTC"),
            weather,
            rvr,
            "ADVISE CONTROLLER ON INITIAL CONTACT YOU HAVE INFORMATION ALPHA"
        ]
        
        return "\n".join(report)
    
    def check_alerts(self):
        """Check for alert conditions"""
        alerts = []
        
        # Wind alert
        if self.sensors["wind_speed"].value > 25:
            alerts.append(f"HIGH WIND: {self.sensors['wind_speed'].value} knots")
        
        # Visibility alert
        vis = self.sensors["visibility"].value
        if vis and vis < 1600:  # Less than 1 mile
            alerts.append(f"LOW VISIBILITY: {vis} meters")
        
        # Ceiling alert
        ceiling = self.sensors["ceiling"].value
        if ceiling and ceiling < 500:
            alerts.append(f"LOW CEILING: {ceiling} feet")
        
        # RVR alert
        for position in ["touchdown", "midpoint", "rollout"]:
            rvr = self.sensors[f"rvr_{position}"].value
            if rvr and rvr < 600:  # Less than 2000 feet
                alerts.append(f"LOW RVR {position.upper()}: {rvr} meters")
        
        return alerts
    
    def close(self):
        """Clean up resources"""
        self.running = False
        if self.serial_connection:
            self.serial_connection.close()
        self.logger.info("AWOS system closed")
