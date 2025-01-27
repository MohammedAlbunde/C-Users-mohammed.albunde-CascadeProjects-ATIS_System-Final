#!/bin/bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Welcome to ATIS Pro System${NC}"
echo "=============================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    python3 -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Dependencies installed successfully!${NC}"
    else
        echo -e "${RED}Error installing dependencies. Please check the error message above.${NC}"
    fi
}

# Function to test AWOS connection
test_awos() {
    echo -e "${YELLOW}Testing AWOS connection...${NC}"
    python3 software/awos_rvr.py --test
}

# Function to start ATIS Pro
start_atis() {
    echo -e "${YELLOW}Starting ATIS Pro system...${NC}"
    cd software
    python3 atis_full.py
}

# Main menu
while true; do
    echo ""
    echo "Please select an option:"
    echo "1. Install Python dependencies"
    echo "2. Test AWOS connection"
    echo "3. Start ATIS Pro system"
    echo "4. View documentation"
    echo "5. Exit"
    
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            install_dependencies
            ;;
        2)
            test_awos
            ;;
        3)
            start_atis
            ;;
        4)
            if command_exists "open"; then
                open docs/english/INSTALLATION_GUIDE.md
            else
                echo -e "${RED}Could not open documentation. Please navigate to docs/english/INSTALLATION_GUIDE.md${NC}"
            fi
            ;;
        5)
            echo -e "${GREEN}Thank you for using ATIS Pro!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
done
