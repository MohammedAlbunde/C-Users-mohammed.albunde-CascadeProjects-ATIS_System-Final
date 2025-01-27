# ATIS Pro - Baghdad International Airport

Automated Terminal Information Service (ATIS) system for Baghdad International Airport, integrating AWOS/RVR data with VHF radio broadcasting.

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/mohammed-albunde/ATIS_Pro_Baghdad.git
cd ATIS_Pro_Baghdad
```

2. Run START_HERE.bat and follow the menu options:
   - Option 1: Install Python and dependencies
   - Option 2: Test AWOS connection
   - Option 3: Start ATIS Pro system
   - Option 4: View documentation

## Installation Guide for macOS

1. Open Terminal (press Cmd + Space, type "Terminal", press Enter)

2. Install Homebrew (macOS package manager) if not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. Install Git and Python:
```bash
brew install git python@3.8
```

4. Clone the repository:
```bash
cd ~/Documents
git clone https://github.com/MohammedAlbunde/C-Users-mohammed.albunde-CascadeProjects-ATIS_System-Final.git ATIS_Pro
cd ATIS_Pro
```

5. Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

6. Install required packages:
```bash
pip install -r requirements.txt
```

7. Start the ATIS Pro system:
```bash
cd software
python atis_full.py
```

## Installation

1. Install Python 3.8 or later from [python.org](https://www.python.org/downloads/)
2. Install required packages:
```bash
pip install -r requirements.txt
```

## System Requirements

### For macOS:
- macOS 10.15 (Catalina) or later
- 4GB RAM minimum
- 1GB free disk space
- Available USB port for AWOS connection
- Available audio output device

### For Windows:
- Windows 10 or later
- Python 3.8 or later
- 4GB RAM minimum
- 1GB free disk space
- Available COM port for AWOS connection
- Available audio output device

## Directory Structure

- `/software` - Python source files
- `/config` - Configuration files
- `/docs` - Documentation in English and Arabic
  - `/docs/english` - English documentation
  - `/docs/arabic` - Arabic documentation

## Troubleshooting

### macOS Issues:
1. If you get a "Python command not found" error:
```bash
export PATH="/usr/local/opt/python@3.8/bin:$PATH"
```

2. If you get a permission error:
```bash
chmod +x START_HERE.sh
```

3. If PyQt installation fails:
```bash
brew install qt
pip install PyQt6
```

4. If audio doesn't work:
   - Open System Preferences
   - Go to Security & Privacy
   - Allow microphone and audio access for Terminal/Python

## Support

For technical support, please contact:
- Phone: +1(226)-789-8500
- Email: moh.iq8567@gmail.com

## License

Copyright 2025 Baghdad International Airport. All rights reserved.
