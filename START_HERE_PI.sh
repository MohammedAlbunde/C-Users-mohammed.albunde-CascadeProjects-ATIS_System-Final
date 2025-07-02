#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Welcome to ATIS Pro System for Raspberry Pi${NC}"
echo "=========================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    
    # Check if virtual environment exists, if not create it
    if [ ! -d "atis_env" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m virtualenv atis_env
    fi
    
    # Activate virtual environment
    source atis_env/bin/activate
    
    # Create Raspberry Pi specific requirements file if it doesn't exist
    if [ ! -f "requirements_pi.txt" ]; then
        echo -e "${YELLOW}Creating Raspberry Pi specific requirements file...${NC}"
        sed 's/PyQt6/PyQt5/g' requirements.txt > requirements_pi.txt
    fi
    
    # Install dependencies
    pip install -r requirements_pi.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Dependencies installed successfully!${NC}"
    else
        echo -e "${RED}Error installing dependencies. Please check the error message above.${NC}"
    fi
}

# Function to test AWOS connection
test_awos() {
    echo -e "${YELLOW}Testing AWOS connection...${NC}"
    
    # Activate virtual environment if exists
    if [ -d "atis_env" ]; then
        source atis_env/bin/activate
    fi
    
    python3 software/awos_rvr.py --test
}

# Function to start ATIS Pro
start_atis() {
    echo -e "${YELLOW}Starting ATIS Pro system...${NC}"
    
    # Activate virtual environment if exists
    if [ -d "atis_env" ]; then
        source atis_env/bin/activate
    fi
    
    cd software
    python3 atis_full_pi.py
}

# Function to setup Raspberry Pi
setup_pi() {
    echo -e "${YELLOW}Setting up Raspberry Pi for ATIS Pro...${NC}"
    
    # Make the setup script executable
    chmod +x raspberry_pi_setup.sh
    
    # Run the setup script
    ./raspberry_pi_setup.sh
}

# Main menu
while true; do
    echo ""
    echo "Please select an option:"
    echo "1. Setup Raspberry Pi for ATIS Pro (first-time setup)"
    echo "2. Install Python dependencies"
    echo "3. Test AWOS connection"
    echo "4. Start ATIS Pro system"
    echo "5. View documentation"
    echo "6. Exit"
    
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1)
            setup_pi
            ;;
        2)
            install_dependencies
            ;;
        3)
            test_awos
            ;;
        4)
            start_atis
            ;;
        5)
            if command_exists "xdg-open"; then
                xdg-open docs/english/INSTALLATION_GUIDE.md
            else
                echo -e "${RED}Could not open documentation. Please navigate to docs/english/INSTALLATION_GUIDE.md${NC}"
            fi
            ;;
        6)
            echo -e "${GREEN}Thank you for using ATIS Pro!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
done
