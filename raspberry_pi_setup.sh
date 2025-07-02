#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up ATIS Pro System for Raspberry Pi${NC}"
echo "=============================================="

# Update package lists
echo -e "${YELLOW}Updating package lists...${NC}"
sudo apt-get update

# Install Python and pip if not already installed
echo -e "${YELLOW}Installing Python and pip...${NC}"
sudo apt-get install -y python3 python3-pip

# Install required system dependencies for PyQt6, PyAudio, and other packages
echo -e "${YELLOW}Installing system dependencies...${NC}"
sudo apt-get install -y \
    python3-pyqt5 \
    libportaudio2 \
    libasound-dev \
    portaudio19-dev \
    libqt5gui5 \
    python3-dev \
    build-essential \
    libatlas-base-dev \
    libjasper-dev \
    libqtgui4 \
    libqt4-test \
    libhdf5-dev \
    libhdf5-serial-dev

# Install Python virtual environment
echo -e "${YELLOW}Installing Python virtual environment...${NC}"
sudo pip3 install virtualenv

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m virtualenv atis_env
source atis_env/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
# Replace PyQt6 with PyQt5 for Raspberry Pi compatibility
sed 's/PyQt6/PyQt5/g' requirements.txt > requirements_pi.txt
pip install -r requirements_pi.txt

echo -e "${GREEN}Setup complete! You can now run the ATIS system.${NC}"
echo "To activate the environment in the future, run: source atis_env/bin/activate"
echo "To start the ATIS system, run: python3 software/atis_full.py"
