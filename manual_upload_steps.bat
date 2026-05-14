@echo off
echo Manual GitHub Upload Steps
echo.
echo 1. First, install Git from: https://git-scm.com/download/windows
echo 2. Create repository on GitHub.com
echo 3. Run these commands one by one:
echo.
echo git init
echo git add .
echo git commit -m "Initial commit: IDS ML project"
echo git branch -M main
echo git remote add origin YOUR_GITHUB_REPO_URL
echo git push -u origin main
echo.
echo Replace YOUR_GITHUB_REPO_URL with your actual repository URL
pause