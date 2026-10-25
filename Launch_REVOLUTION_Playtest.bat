@echo off
title PROJECT REVOLUTION - Playtest Launcher
echo ================================================================================
echo   PROJECT REVOLUTION (क्रांति) — Standalone Playtest Launcher
echo ================================================================================
echo Launching standalone Windows 64-bit client...
start "" "%~dp0Build\Candidate_Windows\Windows\REVOLUTION.exe" -windowed -ResX=1920 -ResY=1080
exit
