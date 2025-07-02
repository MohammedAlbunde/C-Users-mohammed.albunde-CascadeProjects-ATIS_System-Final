import sys
import os
import random
from datetime import datetime
import queue

# Remove Windows-specific environment variable
# os.environ['QT_QPA_PLATFORM'] = 'windows'

# Use PyQt5 instead of PyQt6 for Raspberry Pi compatibility
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout,
                           QComboBox, QTextEdit, QTabWidget, QGroupBox, QCheckBox, QDoubleSpinBox,
                           QMenuBar, QMenu, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

from awos_rvr import AWOS_RVR_System
from vhf_radio import VHFRadio
import pyttsx3
from network_settings import NetworkSettingsDialog

class ATISDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mohammed D-ATIS Control System with AWOS/RVR")
        self.setMinimumSize(1200, 800)
        
        # Initialize systems
        self.awos_rvr = AWOS_RVR_System()
        self.vhf_radio = VHFRadio()  # Add COM port if available, e.g., 'COM3'
        
        # Initialize attributes
        self.value_labels = {}
        self.source_checkboxes = {}
        self.message_queue = queue.Queue()
        
        # Set light theme for entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QWidget {
                background-color: #F0F0F0;
                color: #202020;
            }
            QGroupBox {
                border: 1px solid #D0D0D0;
                border-radius: 8px;
                margin-top: 1ex;
                font-size: 14px;
                font-weight: bold;
                padding: 15px;
            }
            QGroupBox::title {
                color: #202020;
            }
            QTextEdit {
                background-color: #FFFFFF;
                color: #202020;
                border: 1px solid #D0D0D0;
                border-radius: 5px;
            }
            QComboBox {
                background-color: #FFFFFF;
                color: #202020;
                border: 1px solid #D0D0D0;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0077ee;
            }
            QPushButton:pressed {
                background-color: #0055bb;
            }
            QLabel {
                color: #202020;
            }
            QCheckBox {
                color: #202020;
            }
        """)

        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        network_action = settings_menu.addAction("Network Configuration")
        network_action.triggered.connect(self.show_network_settings)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tab widget
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Create tabs
        self.atis_tab = QWidget()
        self.awos_tab = QWidget()
        self.rvr_tab = QWidget()
        
        tab_widget.addTab(self.atis_tab, "ATIS")
        tab_widget.addTab(self.awos_tab, "AWOS")
        tab_widget.addTab(self.rvr_tab, "RVR")

        # Setup tabs
        self.setup_atis_tab()
        self.setup_awos_tab()
        self.setup_rvr_tab()

        # Create status bar
        self.status_label = QLabel("Status: System initialized")
        self.statusBar().addWidget(self.status_label)

        # Create update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_displays)
        self.update_timer.start(5000)  # Update every 5 seconds

    def setup_atis_tab(self):
        layout = QVBoxLayout(self.atis_tab)
        
        # ATIS Information Group
        atis_group = QGroupBox("ATIS Information")
        layout.addWidget(atis_group)
        
        atis_layout = QVBoxLayout(atis_group)
        
        # VHF Settings
        vhf_group = QGroupBox("VHF Radio Settings")
        vhf_layout = QHBoxLayout()
        
        # Frequency control
        freq_label = QLabel("Frequency (MHz):")
        self.freq_spinbox = QDoubleSpinBox()
        self.freq_spinbox.setRange(118.0, 137.0)
        self.freq_spinbox.setSingleStep(0.025)
        self.freq_spinbox.setValue(118.0)
        self.freq_spinbox.valueChanged.connect(self.on_frequency_change)
        
        vhf_layout.addWidget(freq_label)
        vhf_layout.addWidget(self.freq_spinbox)
        vhf_group.setLayout(vhf_layout)
        atis_layout.addWidget(vhf_group)
        
        # Message display
        self.atis_display = QTextEdit()
        self.atis_display.setReadOnly(True)
        self.atis_display.setMinimumHeight(200)
        atis_layout.addWidget(self.atis_display)
        
        # Control buttons
        button_layout = QHBoxLayout()
        record_btn = QPushButton("Record")
        play_btn = QPushButton("Play")
        update_btn = QPushButton("Update")
        broadcast_btn = QPushButton("Broadcast")
        
        record_btn.clicked.connect(self.on_record)
        play_btn.clicked.connect(self.on_play)
        update_btn.clicked.connect(self.on_update)
        broadcast_btn.clicked.connect(self.on_broadcast)
        
        button_layout.addWidget(record_btn)
        button_layout.addWidget(play_btn)
        button_layout.addWidget(update_btn)
        button_layout.addWidget(broadcast_btn)
        atis_layout.addLayout(button_layout)

    def setup_awos_tab(self):
        layout = QVBoxLayout(self.awos_tab)
        
        awos_group = QGroupBox("Automated Weather Observation System")
        layout.addWidget(awos_group)
        
        awos_layout = QVBoxLayout(awos_group)
        self.awos_display = QTextEdit()
        self.awos_display.setReadOnly(True)
        awos_layout.addWidget(self.awos_display)
        
        # Add manual refresh button
        refresh_btn = QPushButton("Refresh AWOS Data")
        refresh_btn.clicked.connect(self.update_awos_display)
        awos_layout.addWidget(refresh_btn)

    def setup_rvr_tab(self):
        layout = QVBoxLayout(self.rvr_tab)
        
        rvr_group = QGroupBox("Runway Visual Range Information")
        layout.addWidget(rvr_group)
        
        rvr_layout = QVBoxLayout(rvr_group)
        self.rvr_display = QTextEdit()
        self.rvr_display.setReadOnly(True)
        rvr_layout.addWidget(self.rvr_display)
        
        # Add manual refresh button
        refresh_btn = QPushButton("Refresh RVR Data")
        refresh_btn.clicked.connect(self.update_rvr_display)
        rvr_layout.addWidget(refresh_btn)

    def update_displays(self):
        """Update all displays with latest information"""
        self.update_awos_display()
        self.update_rvr_display()
        self.update_atis_display()

    def update_awos_display(self):
        """Update AWOS display with latest weather information"""
        weather_report = self.awos_rvr.get_weather_report()
        self.awos_display.setText(weather_report)
        self.status_label.setText(f"Status: AWOS updated at {datetime.now().strftime('%H:%M:%S')}")
        
    def update_rvr_display(self):
        """Update RVR display with latest runway visual range information"""
        rvr_report = self.awos_rvr.get_rvr_report()
        self.rvr_display.setText(rvr_report)
        
    def update_atis_display(self):
        """Update ATIS display with combined information"""
        combined_report = self.awos_rvr.get_combined_report()
        self.atis_display.setText(combined_report)

    def on_frequency_change(self, value):
        """Handle VHF frequency changes"""
        try:
            self.vhf_radio.set_frequency(value)
            self.status_label.setText(f"Status: VHF frequency set to {value:.3f} MHz")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def on_broadcast(self):
        """Broadcast current ATIS message over VHF"""
        try:
            message = self.atis_display.toPlainText()
            if message:
                self.vhf_radio.queue_message(message)
                self.status_label.setText("Status: Broadcasting ATIS message...")
            else:
                self.status_label.setText("Error: No message to broadcast")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def on_record(self):
        """Record ATIS message"""
        try:
            message = self.atis_display.toPlainText()
            if message:
                # Save to file for later playback
                with open("last_atis.txt", "w") as f:
                    f.write(message)
                self.status_label.setText("Status: ATIS message recorded")
            else:
                self.status_label.setText("Error: No message to record")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def on_play(self):
        """Play recorded ATIS message"""
        try:
            if os.path.exists("last_atis.txt"):
                with open("last_atis.txt", "r") as f:
                    message = f.read()
                    
                # Use text-to-speech to play message
                engine = pyttsx3.init()
                engine.say(message)
                engine.runAndWait()
                self.status_label.setText("Status: Playing ATIS message")
            else:
                self.status_label.setText("Error: No recorded message found")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def on_update(self):
        """Update ATIS display with latest information"""
        try:
            combined_report = self.awos_rvr.get_combined_report()
            self.atis_display.setText(combined_report)
            self.status_label.setText("Status: ATIS information updated")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def show_network_settings(self):
        dialog = NetworkSettingsDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """Clean up resources when closing"""
        self.awos_rvr.close()
        self.vhf_radio.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ATISDisplay()
    window.show()
    return app.exec_()  # Note: In PyQt5, it's exec_() with underscore

if __name__ == '__main__':
    sys.exit(main())
