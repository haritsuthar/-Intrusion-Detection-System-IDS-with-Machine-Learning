@echo off
echo 🚀 Uploading Intrusion Detection System to GitHub
echo.

REM Initialize git repository
echo 📁 Initializing Git repository...
git init

REM Add all files
echo 📦 Adding files to Git...
git add .

REM Create initial commit
echo 💾 Creating initial commit...
git commit -m "Initial commit: Complete Intrusion Detection System with ML and Web Interface

Features:
- Random Forest classifier for network intrusion detection
- Modern responsive web interface
- Real-time threat analysis with confidence scores
- Performance visualizations (confusion matrix, ROC curve, feature importance)
- REST API for training and predictions
- Comprehensive documentation and setup scripts
- Support for NSL-KDD dataset

Tech Stack: Python, Flask, scikit-learn, HTML/CSS/JavaScript"

echo.
echo 🌐 Next steps:
echo 1. Create a new repository on GitHub.com
echo 2. Copy the repository URL (e.g., https://github.com/username/repo-name.git)
echo 3. Run these commands:
echo.
echo    git branch -M main
echo    git remote add origin YOUR_GITHUB_REPO_URL
echo    git push -u origin main
echo.
echo Replace YOUR_GITHUB_REPO_URL with your actual GitHub repository URL
echo.
pause