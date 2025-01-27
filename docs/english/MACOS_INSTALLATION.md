# Detailed MacOS Installation Guide for ATIS Pro

## Prerequisites
- MacBook Pro with macOS 10.15 (Catalina) or later
- At least 4GB of free RAM
- At least 1GB of free disk space
- Internet connection
- Administrator access to your MacBook

## Step 1: Open Terminal
1. Click the Apple menu (🍎) in the top-left corner
2. Click "System Settings"
3. Click "Privacy & Security"
4. Scroll down to "Developer Tools"
5. Enable Terminal if not already enabled
6. Press `Command (⌘) + Space` on your keyboard
7. Type "Terminal"
8. Press `Return` (Enter)

## Step 2: Install Command Line Tools
1. In Terminal, paste this command:
```bash
xcode-select --install
```
2. Click "Install" when prompted
3. Wait for the installation to complete (5-10 minutes)
4. When finished, click "Done"

## Step 3: Install Homebrew
1. In Terminal, paste this command:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Press `Return` (Enter)
3. Enter your MacBook password when prompted
4. Wait for Homebrew installation to complete (5-10 minutes)
5. When finished, run these two commands:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Step 4: Install Python and Git
1. In Terminal, run:
```bash
brew install python@3.8
brew install git
```
2. Wait for installation to complete (3-5 minutes)
3. Add Python to your PATH:
```bash
echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Step 5: Install Qt Framework
1. In Terminal, run:
```bash
brew install qt
```
2. Wait for installation to complete (5-10 minutes)

## Step 6: Download ATIS Pro
1. Navigate to Documents:
```bash
cd ~/Documents
```
2. Clone the repository:
```bash
git clone https://github.com/MohammedAlbunde/C-Users-mohammed.albunde-CascadeProjects-ATIS_System-Final.git ATIS_Pro
```
3. Enter the project directory:
```bash
cd ATIS_Pro
```

## Step 7: Set Up Python Environment
1. Create a virtual environment:
```bash
python3 -m venv venv
```
2. Activate the virtual environment:
```bash
source venv/bin/activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```

## Step 8: Configure System Permissions
1. Click the Apple menu (🍎)
2. Open "System Settings"
3. Click "Privacy & Security"
4. Click "Microphone"
   - Enable access for Terminal
   - Enable access for Python
5. Click "Input Monitoring"
   - Enable access for Terminal
   - Enable access for Python
6. Click "Accessibility"
   - Enable access for Terminal
   - Enable access for Python

## Step 9: Start ATIS Pro
1. Make the startup script executable:
```bash
chmod +x START_HERE.sh
```
2. Run the startup script:
```bash
./START_HERE.sh
```
3. From the menu that appears:
   - Press `1` to install dependencies
   - Press `3` to start ATIS Pro

## Step 10: Verify Installation
1. The ATIS Pro GUI should appear
2. Check these components:
   - Weather Information Panel
   - VHF Radio Control
   - System Status indicators
3. Test the audio system:
   - Click "Test Audio"
   - You should hear a test message

## Troubleshooting

### If Python is not found:
```bash
export PATH="/usr/local/opt/python@3.8/bin:$PATH"
source ~/.zshrc
```

### If PyQt installation fails:
```bash
brew uninstall qt
brew install qt
pip install PyQt6
```

### If audio doesn't work:
1. Open System Settings
2. Go to Sound
3. Check Input/Output devices
4. Make sure volume is not muted

### If AWOS connection fails:
1. Check USB connections
2. Run the connection test:
```bash
python3 software/awos_rvr.py --test
```

## Support Contact
If you encounter any issues:
- Email: moh.iq8567@gmail.com
- Phone: +1(226)-789-8500
- Working Hours: 9 AM - 5 PM (Baghdad Time)
