@echo off
title Restart Claude Desktop
color 0A
cls
echo ==============================================================================
echo                      RESTARTING CLAUDE DESKTOP
echo ==============================================================================
echo.
echo Stopping running Claude processes...
powershell -NoProfile -Command "Stop-Process -Name 'claude' -Force -ErrorAction SilentlyContinue"
echo Waiting 2 seconds...
powershell -NoProfile -Command "Start-Sleep -Seconds 2"
echo Launching Claude Desktop with updated MCP configuration...
powershell -NoProfile -Command "Start-Process 'shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude'"
echo.
echo Claude Desktop has been restarted!
echo Check Settings -> Developer / Integrations or the tools menu in Claude chat.
echo ==============================================================================
echo.
pause
