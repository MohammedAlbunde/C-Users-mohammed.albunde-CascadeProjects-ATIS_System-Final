@echo off 
color 1F 
mode con: cols=80 lines=25 
title ATIS Pro - Baghdad International Airport 
 
:MENU 
cls 
echo =============================================================================== 
echo                         ATIS Pro - Baghdad International Airport 
echo =============================================================================== 
echo. 
echo  Please select an option: 
echo. 
echo  [1] Install Python and Required Packages 
echo  [2] Test AWOS Connection 
echo  [3] Start ATIS Pro System 
echo  [4] View Documentation 
echo  [5] Exit 
echo. 
echo  Support: +1(226)-789-8500 
echo  Email: moh.iq8567@gmail.com 
echo. 
echo =============================================================================== 
echo. 
set /p choice="Enter your choice (1-5): " 
 
if "%choice%"=="1" goto INSTALL 
if "%choice%"=="2" goto TEST 
if "%choice%"=="3" goto START 
if "%choice%"=="4" goto DOCS 
if "%choice%"=="5" goto END 
goto MENU 
 
:INSTALL 
cls 
echo Installing Python and required packages... 
echo. 
start https://www.python.org/downloads/ 
echo Please wait while Python installer downloads... 
echo. 
echo After Python installation completes: 
echo 1. Open Command Prompt 
echo 2. Type: pip install -r requirements.txt 
echo. 
pause 
goto MENU 
 
:TEST 
cls 
echo Testing AWOS Connection... 
cd software 
python test_vaisala_connection.py 
cd .. 
pause 
goto MENU 
 
:START 
cls 
echo Starting ATIS Pro System... 
cd software 
python atis_full.py 
cd .. 
goto MENU 
 
:DOCS 
cls 
echo Opening Documentation... 
echo. 
echo [1] English Documentation 
echo [2] Arabic Documentation 
echo [3] Return to Main Menu 
echo. 
set /p doc_choice="Enter your choice (1-3): " 
 
if "%doc_choice%"=="1" ( 
    start docs\english\INSTALLATION_GUIDE.md 
    goto DOCS 
) 
if "%doc_choice%"=="2" ( 
    start docs\arabic\INSTALLATION_GUIDE_AR.md 
    goto DOCS 
) 
if "%doc_choice%"=="3" goto MENU 
goto DOCS 
 
:END 
cls 
echo =============================================================================== 
echo                         Thank you for using ATIS Pro 
echo =============================================================================== 
echo. 
echo  For support, please contact: 
echo. 
echo  Phone: +1(226)-789-8500 
echo  Email: moh.iq8567@gmail.com 
echo. 
echo =============================================================================== 
timeout /t 5 
exit 
