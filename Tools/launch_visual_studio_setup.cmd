@echo off
echo ==============================================================================
echo   PROJECT REVOLUTION - VISUAL STUDIO 2022 INSTALLER LAUNCHER
echo ==============================================================================
echo Launching Visual Studio 2022 Community Installer with pre-configured:
echo   - Game development with C++
echo   - Desktop development with C++
echo   - Windows 11 SDK (10.0.22621.0)
echo   - Unreal Engine IDE support
echo.
start "" "C:\Users\npal7\Downloads\VisualStudioSetup.exe" --add Microsoft.VisualStudio.Workload.NativeGame --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --add Microsoft.VisualStudio.Component.VC.UnrealEngine
echo Installer process launched. Please accept the Windows UAC elevation prompt if shown.
