@echo off
title PROJECT REVOLUTION - Push to GitHub
color 0A
cls
echo ==============================================================================
echo             PROJECT REVOLUTION - PUSH CODE & ASSETS TO GITHUB
echo ==============================================================================
echo.
echo Pushing branch 'main' and Git LFS assets to:
echo   https://github.com/npal78229-eng/REVOLUTION-Game.git
echo.
git push -u origin main
echo.
echo ==============================================================================
if %ERRORLEVEL% equ 0 (
    echo SUCCESS: Project pushed to GitHub successfully!
) else (
    echo NOTE: If the repo does not exist yet, make sure you clicked "Create repository" on GitHub!
)
echo ==============================================================================
pause
