import socket
import threading
import json
import time
from datetime import datetime

class AWOSNetworkClient:
    def __init__(self, host='192.168.1.100', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.data_callback = None
        self.error_callback = None
        self.running = False
        self.last_data = None
        self.reconnect_delay = 5  # seconds

    def connect(self):
        """Establish connection to AWOS server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to AWOS at {self.host}:{self.port}")
            return True
        except Exception as e:
            if self.error_callback:
                self.error_callback(f"Connection failed: {str(e)}")
            return False

    def start(self, data_callback=None, error_callback=None):
        """Start receiving data from AWOS"""
        self.data_callback = data_callback
        self.error_callback = error_callback
        self.running = True
        
        # Start receiver thread
        self.receiver_thread = threading.Thread(target=self._receive_data)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def stop(self):
        """Stop receiving data"""
        self.running = False
        if self.socket:
            self.socket.close()
        self.connected = False

    def _receive_data(self):
        """Receive and process data from AWOS"""
        while self.running:
            if not self.connected:
                if self.connect():
                    time.sleep(self.reconnect_delay)
                continue

            try:
                # Read data from socket
                data = self.socket.recv(1024)
                if not data:
                    raise ConnectionError("Connection lost")

                # Parse AWOS data
                decoded_data = self._parse_awos_data(data)
                self.last_data = decoded_data

                # Call callback with decoded data
                if self.data_callback:
                    self.data_callback(decoded_data)

            except Exception as e:
                if self.error_callback:
                    self.error_callback(f"Data reception error: {str(e)}")
                self.connected = False
                time.sleep(self.reconnect_delay)

    def _parse_awos_data(self, data):
        """Parse raw AWOS data into structured format"""
        try:
            # Decode bytes to string
            data_str = data.decode('utf-8')
            
            # Parse JSON data
            weather_data = json.loads(data_str)
            
            # Add timestamp
            weather_data['timestamp'] = datetime.utcnow().isoformat()
            
            return weather_data
        except Exception as e:
            if self.error_callback:
                self.error_callback(f"Data parsing error: {str(e)}")
            return None

    def get_last_data(self):
        """Return the most recent weather data"""
        return self.last_data

    def set_host(self, host, port):
        """Update connection settings"""
        self.host = host
        self.port = port
        if self.connected:
            self.stop()
            self.connect()
            if self.running:
                self.start(self.data_callback, self.error_callback)
