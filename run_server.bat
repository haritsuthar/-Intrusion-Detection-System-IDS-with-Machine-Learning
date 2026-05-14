@echo off
echo 🚀 Starting IDS ML Server...
echo 📊 Frontend will be available at: http://127.0.0.1:5000
echo.

REM Check if data files exist
if not exist "KDDTrain+.txt" (
    echo ❌ Error: KDDTrain+.txt not found!
    echo Please download the NSL-KDD dataset files from:
    echo https://www.unb.ca/cic/datasets/nsl.html
    pause
    exit /b 1
)

if not exist "KDDTest+.txt" (
    echo ❌ Error: KDDTest+.txt not found!
    echo Please download the NSL-KDD dataset files from:
    echo https://www.unb.ca/cic/datasets/nsl.html
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo 🌐 Starting Flask server...
cd backend
python app.py

pause