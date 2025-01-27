# Complete ATIS Pro Setup Guide
## Baghdad International Airport

This guide will help you set up and run the ATIS Pro system, even if you have no prior experience. Follow each step carefully.

## Table of Contents
1. [Required Equipment](#required-equipment)
2. [Software Installation](#software-installation)
3. [Hardware Connections](#hardware-connections)
4. [System Configuration](#system-configuration)
5. [Running the System](#running-the-system)
6. [Troubleshooting](#troubleshooting)

## Required Equipment

### Hardware
1. Computer with:
   - At least 4GB RAM
   - 1GB free disk space
   - 2 available USB ports
   - Audio output port

2. Cables:
   - RS-232 to USB converter cable (for AWOS)
   - Audio cable (3.5mm or appropriate size)
   - USB to Serial converter (for VHF radio)

3. AWOS Equipment:
   - Vaisala AWOS system
   - RS-232 port access
   - System documentation

4. VHF Radio:
   - Aviation band radio (118-137 MHz)
   - DATA/ACC port
   - PTT (Push-to-Talk) control
   - Audio input port

### Software
- ATIS Pro system files
- Python 3.8 or later
- Required Python libraries

## Software Installation

### Step 1: Download Project Files
1. Open your web browser
2. Go to: https://github.com/MohammedAlbunde/C-Users-mohammed.albunde-CascadeProjects-ATIS_System-Final
3. Click the green "Code" button
4. Click "Download ZIP"
5. Extract the ZIP file to your computer

### Step 2: Install Python
1. Go to https://python.org/downloads
2. Download Python 3.8 or later
3. Run the installer
4. Important: Check "Add Python to PATH"
5. Click "Install Now"

### Step 3: Install Required Libraries
1. Open Command Prompt/Terminal
2. Navigate to project folder:
   ```bash
   cd path/to/ATIS_Pro
   ```
3. Create virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
5. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Hardware Connections

### Step 1: AWOS Connection
[Diagram: AWOS_Connection.png]

1. Locate the RS-232 port on your Vaisala AWOS system
   - Usually labeled "DATA" or "SERIAL"
   - Typically a 9-pin connector

2. Connect RS-232 to USB converter:
   - Plug RS-232 end into AWOS port
   - Plug USB end into computer
   - Note down which USB port you used

3. Find the COM port number:
   - Windows:
     1. Right-click Start Menu
     2. Select "Device Manager"
     3. Expand "Ports (COM & LPT)"
     4. Note the COM number (e.g., COM3)
   - Linux:
     - Usually `/dev/ttyUSB0`
   - macOS:
     - Usually `/dev/tty.usbserial-*`

### Step 2: VHF Radio Connection
[Diagram: VHF_Connection.png]

1. Audio Connection:
   - Connect computer's audio output to radio's audio input
   - Use appropriate audio cable (usually 3.5mm)
   - Make sure connection is secure

2. PTT Connection:
   - Connect radio's PTT port to USB-Serial converter
   - Note down which USB port you used
   - Find COM port number (as above)

3. Radio Settings:
   - Set to correct frequency (ask your supervisor)
   - Set squelch level to appropriate setting
   - Enable external PTT control
   - Set audio input to external

## System Configuration

### Step 1: AWOS Configuration
1. Open `config/awos_config.json`
2. Update these settings:
   ```json
   {
     "port": "COM3",        // Your AWOS COM port
     "baudrate": 9600,      // Usually 9600
     "databits": 8,
     "parity": "none",
     "stopbits": 1
   }
   ```

### Step 2: Radio Configuration
1. Open `config/radio_config.json`
2. Update these settings:
   ```json
   {
     "port": "COM4",        // Your radio's COM port
     "frequency": "118.000", // Your assigned frequency
     "ptt_control": true,
     "audio_device": "default"
   }
   ```

### Step 3: Airport Configuration
1. Open `config/airport_config.json`
2. Update these settings:
   ```json
   {
     "airport_name": "Baghdad International",
     "airport_code": "ORBI",
     "elevation": 114,      // In feet
     "magnetic_variation": 5
   }
   ```

## Running the System

### Step 1: Start the System
1. Open Command Prompt/Terminal
2. Navigate to project folder
3. Run the startup script:
   - Windows:
     ```bash
     START_HERE.bat
     ```
   - Linux/macOS:
     ```bash
     ./START_HERE.sh
     ```

### Step 2: Verify Operation
1. Check AWOS Data:
   - Temperature displays correctly
   - Wind information updates
   - All sensors showing data

2. Check Radio:
   - Status indicator is green
   - Correct frequency displayed
   - Audio levels normal

### Step 3: Test Broadcast
1. Click "Preview" button
   - Should hear message through computer speakers
2. Click "Broadcast" button
   - Radio should transmit
   - Check with handheld radio

### Step 4: Enable Auto Mode
1. Set update interval (usually 30 minutes)
2. Click "Enable Auto Broadcast"
3. Monitor first few broadcasts

## Troubleshooting

### No AWOS Data
1. Check physical connections
2. Verify COM port number
3. Check AWOS is sending data:
   ```bash
   python software/awos_rvr.py --test
   ```

### Radio Not Transmitting
1. Check audio connections
2. Verify PTT connection
3. Test radio manually
4. Check audio levels

### Software Issues
1. Verify Python installation:
   ```bash
   python --version
   ```
2. Check all libraries installed:
   ```bash
   pip list
   ```
3. Look for error messages in terminal

## Support Contact

If you need help:
- Email: moh.iq8567@gmail.com
- Phone: +1(226)-789-8500
- Hours: 9 AM - 5 PM (Baghdad Time)

## Safety Notes

1. Never disconnect cables while system is running
2. Always monitor first few broadcasts
3. Test system before going live
4. Keep backup of configuration files
5. Document any changes made

[Include actual diagrams in the same folder]
