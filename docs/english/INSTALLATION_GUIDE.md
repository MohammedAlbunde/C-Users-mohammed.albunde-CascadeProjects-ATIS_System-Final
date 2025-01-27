# ATIS Pro Installation Guide

## Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [Software Requirements](#software-requirements)
3. [Pre-Installation Checklist](#pre-installation-checklist)
4. [Hardware Installation](#hardware-installation)
5. [Software Installation](#software-installation)
6. [System Configuration](#system-configuration)
7. [Testing and Validation](#testing-and-validation)
8. [Troubleshooting](#troubleshooting)

## Hardware Requirements

### Computer System
- CPU: Intel Core i5/i7 (8th gen or newer)
- RAM: 16GB minimum
- Storage: 512GB SSD
- Display: 1920x1080 touch screen
- Network: Gigabit Ethernet
- USB Ports: Minimum 4x USB 3.0
- Serial Ports: Minimum 2x RS-232

### AWOS Hardware
- Wind Sensor
  - Model: AWOS-WS200
  - Mounting pole: 10m height
  - Power: 12V DC
  - Interface: RS-485

- Temperature/Humidity Sensor
  - Model: AWOS-TH100
  - Radiation shield required
  - Power: 12V DC
  - Interface: RS-485

- Pressure Sensor
  - Model: AWOS-BP500
  - Indoor mounting
  - Power: 12V DC
  - Interface: RS-485

- Visibility Sensor
  - Model: AWOS-VS1000
  - Mounting height: 2.5m
  - Power: 24V DC
  - Interface: RS-485

- Ceiling Sensor
  - Model: AWOS-CL2000
  - Mounting height: Ground level
  - Power: 24V DC
  - Interface: RS-485

### VHF Radio System
- Transmitter
  - Power: 25W minimum
  - Frequency range: 118.0-137.0 MHz
  - Interface: RS-232
  - Antenna system with lightning protection

### Power System
- UPS: 2000VA minimum
- Surge protection
- Ground system: <5 ohm resistance
- Battery backup: 4 hours minimum

## Software Requirements
- Windows 10/11 Pro 64-bit
- Python 3.8 or newer
- All required Python packages (see requirements.txt)
- SQL Server Express 2019 or newer
- Remote access software (optional)

## Pre-Installation Checklist

### Site Survey
- [ ] Verify line of sight for sensors
- [ ] Check power availability
- [ ] Verify network connectivity
- [ ] Assess environmental conditions
- [ ] Check radio frequency clearance
- [ ] Verify ground system availability

### Documentation Required
- [ ] Airport layout plan
- [ ] Radio frequency assignment
- [ ] Environmental approval
- [ ] Local authority permits
- [ ] Equipment certificates

### Tools Required
- [ ] Digital multimeter
- [ ] Network cable tester
- [ ] Serial port tester
- [ ] Basic hand tools
- [ ] Calibration equipment
- [ ] Laptop with diagnostic software

## Hardware Installation

### 1. Sensor Installation

#### Wind Sensor
1. Assemble mounting pole
2. Install lightning protection
3. Mount sensor head
4. Level sensor using bubble level
5. Connect power cable
6. Connect data cable
7. Verify orientation to true north

#### Temperature/Humidity Sensor
1. Mount radiation shield
2. Install sensor in shield
3. Connect power cable
4. Connect data cable
5. Verify ventilation

[Similar detailed steps for other sensors...]

### 2. VHF Radio Installation
1. Mount radio rack
2. Install radio unit
3. Connect antenna system
4. Install lightning arrestor
5. Connect power supply
6. Connect control interface
7. Set initial frequency
8. Test SWR

### 3. Computer System Setup
1. Mount computer rack
2. Install UPS
3. Connect power distribution
4. Install display mount
5. Connect peripherals
6. Install network equipment
7. Label all cables

## Software Installation

### 1. Operating System
1. Install Windows 10/11 Pro
2. Apply all updates
3. Configure network settings
4. Set up remote access
5. Configure firewall

### 2. Python Environment
```bash
# Install Python
python-3.8.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Create virtual environment
python -m venv atis_env
atis_env\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. ATIS Pro Software
1. Copy ATIS Pro files to C:\Program Files\ATIS_Pro
2. Run installer:
```bash
python setup.py install
```

3. Install license:
```bash
python license_manager.py --install LICENSE_KEY
```

## System Configuration

### 1. Configure config.json
```json
{
    "station": {
        "name": "KXXX",
        "elevation": 1000,
        "magnetic_variation": 0
    },
    "awos": {
        "com_port": "COM3",
        "baud_rate": 9600
    },
    "radio": {
        "com_port": "COM4",
        "frequency": 118.0,
        "power": "high"
    }
}
```

### 2. Sensor Configuration
1. Set sensor addresses
2. Configure update rates
3. Set measurement units
4. Configure alarm thresholds

### 3. Radio Configuration
1. Set operating frequency
2. Configure power level
3. Set broadcast intervals
4. Configure voice parameters

## Testing and Validation

### 1. Sensor Validation
1. Compare with calibrated instruments
2. Verify update rates
3. Check error conditions
4. Validate logging

### 2. Radio Testing
1. Check transmission power
2. Verify audio quality
3. Test coverage area
4. Validate PTT timing

### 3. System Testing
1. Run full system test
2. Verify data logging
3. Test backup systems
4. Validate alerts
5. Check remote access

## Troubleshooting

### Common Issues

#### Sensor Communication
- Check COM port assignments
- Verify baud rates
- Test cable connections
- Check power supply

#### Radio Issues
- Verify frequency settings
- Check antenna SWR
- Test audio levels
- Verify PTT timing

#### Software Issues
- Check log files
- Verify permissions
- Test database connection
- Validate configuration

### Support Contact
- Technical Support: +1 (555) 123-4567
- Email: support@atis-pro.com
- Web: support.atis-pro.com

## Maintenance Schedule

### Daily Checks
- [ ] Verify sensor readings
- [ ] Check radio operation
- [ ] Review error logs
- [ ] Backup data

### Weekly Tasks
- [ ] Clean sensors
- [ ] Test backup power
- [ ] Verify calibration
- [ ] Check system logs

### Monthly Tasks
- [ ] Full system backup
- [ ] Detailed calibration
- [ ] Update software
- [ ] Test emergency procedures

## Safety Notes
1. Always follow local safety regulations
2. Use proper PPE when working with equipment
3. Verify power is off before maintenance
4. Follow proper grounding procedures
5. Document all maintenance activities
