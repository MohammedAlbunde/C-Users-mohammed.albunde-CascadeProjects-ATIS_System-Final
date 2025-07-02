from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
import socket
import json

class NetworkSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AWOS Network Configuration")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # AWOS Connection Group
        awos_group = QGroupBox("AWOS Connection Settings")
        awos_layout = QVBoxLayout()
        
        # IP Address
        ip_layout = QHBoxLayout()
        ip_label = QLabel("IP Address:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        ip_layout.addWidget(ip_label)
        ip_layout.addWidget(self.ip_input)
        
        # Port
        port_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("8080")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        
        # Add to AWOS group
        awos_layout.addLayout(ip_layout)
        awos_layout.addLayout(port_layout)
        awos_group.setLayout(awos_layout)
        
        # Status Group
        status_group = QGroupBox("Connection Status")
        status_layout = QVBoxLayout()
        self.status_label = QLabel("Not Connected")
        self.status_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.test_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # Add all to main layout
        layout.addWidget(awos_group)
        layout.addWidget(status_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def test_connection(self):
        ip = self.ip_input.text() or "192.168.1.100"
        try:
            port = int(self.port_input.text() or "8080")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid port number")
            return
            
        try:
            # Create a socket and attempt connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            sock.connect((ip, port))
            
            # Send test request
            test_request = json.dumps({"type": "test"}).encode()
            sock.send(test_request)
            
            # Wait for response
            response = sock.recv(1024)
            
            sock.close()
            
            self.status_label.setText("Connected Successfully")
            self.status_label.setStyleSheet("color: green;")
            QMessageBox.information(self, "Success", "Connection test successful!")
            
        except Exception as e:
            self.status_label.setText(f"Connection Failed: {str(e)}")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.warning(self, "Error", f"Connection test failed: {str(e)}")
    
    def save_settings(self):
        # Validate inputs
        if not self.ip_input.text():
            QMessageBox.warning(self, "Error", "IP Address is required")
            return
            
        try:
            port = int(self.port_input.text() or "8080")
            if port < 1 or port > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
            return
            
        # Save settings to configuration
        settings = {
            'awos_ip': self.ip_input.text(),
            'awos_port': port
        }
        
        try:
            with open('network_config.json', 'w') as f:
                json.dump(settings, f)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {str(e)}")
