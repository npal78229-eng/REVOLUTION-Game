# PROJECT REVOLUTION — Automated Release Packaging Script for Windows 64-bit
# Uses Unreal Automation Tool (RunUAT.bat) to build, cook, and package REVOLUTION

param (
    [string]$Config = "Development",
    [string]$OutputDir = "C:\Users\npal7\PROJECT\REVOLUTION\Build\Development"
)

$ErrorActionPreference = "Stop"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  PROJECT REVOLUTION -- AUTOMATED WIN64 RELEASE PACKAGING (UAT)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

$UATPath = "C:\Program Files\Epic Games\UE_5.5\Engine\Build\BatchFiles\RunUAT.bat"
$ProjectPath = "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject"

if (-not (Test-Path $UATPath)) {
    Write-Error "RunUAT.bat not found at: $UATPath"
}

if (-not (Test-Path $ProjectPath)) {
    Write-Error "Project file not found at: $ProjectPath"
}

if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    Write-Host "[INIT] Created output directory: $OutputDir" -ForegroundColor Green
}

Write-Host "[UAT] Launching BuildCookRun for platform Win64 [$Config]..." -ForegroundColor Yellow
$Sw = [System.Diagnostics.Stopwatch]::StartNew()

$UATArgs = @(
    "BuildCookRun",
    "-project=`"$ProjectPath`"",
    "-noP4",
    "-platform=Win64",
    "-clientconfig=$Config",
    "-cook",
    "-iterative",
    "-build",
    "-stage",
    "-pak",
    "-archive",
    "-archivedirectory=`"$OutputDir`"",
    "-map=/Game/Maps/L_Validation_Gym",
    "-unattended",
    "-utf8output"
)

$Process = Start-Process -FilePath $UATPath -ArgumentList $UATArgs -NoNewWindow -Wait -PassThru

$Sw.Stop()
$Elapsed = [math]::Round($Sw.Elapsed.TotalMinutes, 2)

if ($Process.ExitCode -eq 0) {
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  RELEASE PACKAGING COMPLETED SUCCESSFULLY in $Elapsed minutes!" -ForegroundColor Green
    Write-Host "  Standalone executable and assets archived to: $OutputDir" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
} else {
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host "  PACKAGING FAILED with exit code $($Process.ExitCode)" -ForegroundColor Red
    Write-Host "================================================================================" -ForegroundColor Red
    exit $Process.ExitCode
}
