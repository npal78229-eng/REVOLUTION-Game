# PROJECT REVOLUTION — Master Continuous Integration (CI) Test Harness
# Executes all 6 QA verification suites in sequence and produces a unified audit report

$ErrorActionPreference = "Continue"

Write-Host '================================================================================' -ForegroundColor Cyan
Write-Host '  PROJECT REVOLUTION - MASTER CONTINUOUS INTEGRATION [CI] TEST HARNESS' -ForegroundColor Cyan
Write-Host '================================================================================' -ForegroundColor Cyan
Write-Host "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

$UECmd = "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
$UEPython = "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\ThirdParty\Python3\Win64\python.exe"
$Project = "C:\Users\npal7\PROJECT\REVOLUTION\Project\REVOLUTION.uproject"
$ScriptsDir = "C:\Users\npal7\PROJECT\REVOLUTION\Scripts"

$TestSuites = @(
    @{
        Id = 'TEST-01'
        Name = 'Quality-of-Life, Satchel Modal and Historical Codex'
        Script = "$ScriptsDir\verify_qol_and_codex.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-02'
        Name = 'Audio Mix, SoundClass Hierarchy and Dynamic Curfew Filter'
        Script = "$ScriptsDir\verify_audio_mix.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-03'
        Name = 'Cinematic Camera Sequences and C++ Director Actor'
        Script = "$ScriptsDir\verify_cinematic_sequences.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-04'
        Name = 'Act I Narrative Story Questline and Landmarks [206 Actors]'
        Script = "$ScriptsDir\verify_act1_questline.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-05'
        Name = 'Master PIE and Story Simulation [27 Milestones across Acts I-V]'
        Script = "$ScriptsDir\verify_pie_master_walkthrough.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-06'
        Name = 'Standalone Build Cook, IoStore Packaging and GTX 1650 Budget'
        Script = "$ScriptsDir\verify_standalone_package.py"
        Type = 'Python'
    },
    @{
        Id = 'TEST-07'
        Name = 'Civilian Dialogue Voice Localization and Ambient Proximity Audio'
        Script = "$ScriptsDir\verify_civilian_voice_localization.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-08'
        Name = 'Pedestrian Reaction, Dynamic Stumble and Curiosity System'
        Script = "$ScriptsDir\verify_pedestrian_reactions.py"
        Type = 'Commandlet'
    }
)

$Results = @()
$MasterSw = [System.Diagnostics.Stopwatch]::StartNew()
$AllPassed = $true

foreach ($Test in $TestSuites) {
    Write-Host "`n--------------------------------------------------------------------------------" -ForegroundColor DarkGray
    Write-Host "[$($Test.Id)] Running: $($Test.Name)..." -ForegroundColor Yellow
    Write-Host "  Script: $($Test.Script)" -ForegroundColor DarkGray

    $Sw = [System.Diagnostics.Stopwatch]::StartNew()
    $ExitCode = 1

    if ($Test.Type -eq "Commandlet") {
        $ArgsList = @(
            "`"$Project`"",
            "-run=pythonscript",
            "-script=`"$($Test.Script)`"",
            "-stdout",
            "-unattended",
            "-NullRHI"
        )
        $Proc = Start-Process -FilePath $UECmd -ArgumentList $ArgsList -NoNewWindow -Wait -PassThru
        $ExitCode = $Proc.ExitCode
    } else {
        $Proc = Start-Process -FilePath $UEPython -ArgumentList "`"$($Test.Script)`"" -NoNewWindow -Wait -PassThru
        $ExitCode = $Proc.ExitCode
    }

    $Sw.Stop()
    $DurationSec = [math]::Round($Sw.Elapsed.TotalSeconds, 2)
    $Status = if ($ExitCode -eq 0) { "PASS" } else { "FAIL" }

    if ($ExitCode -ne 0) {
        $AllPassed = $false
        Write-Host "  -> Result: $Status (Exit Code: $ExitCode) in ${DurationSec}s" -ForegroundColor Red
    } else {
        Write-Host "  -> Result: $Status (Exit Code: 0) in ${DurationSec}s" -ForegroundColor Green
    }

    $Results += [PSCustomObject]@{
        Id = $Test.Id
        Name = $Test.Name
        Status = $Status
        Duration = "${DurationSec}s"
        ExitCode = $ExitCode
    }
}

$MasterSw.Stop()
$TotalMinutes = [math]::Round($MasterSw.Elapsed.TotalMinutes, 2)

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host '  PROJECT REVOLUTION - MASTER CI VERIFICATION SUMMARY REPORT' -ForegroundColor Cyan
Write-Host '================================================================================' -ForegroundColor Cyan

$Results | Format-Table -AutoSize -Property Id, Status, Duration, Name

if ($AllPassed) {
    $PassCount = ($Results | Where-Object { $_.Status -eq 'PASS' }).Count
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  OVERALL RESULT: 100% PASS ($PassCount/$($TestSuites.Count) SUITES PASSED) in $TotalMinutes minutes!" -ForegroundColor Green
    Write-Host "  PROJECT REVOLUTION IS CERTIFIED GOLD MASTER READY!" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    exit 0
} else {
    Write-Host "================================================================================" -ForegroundColor Red
    Write-Host "  OVERALL RESULT: ONE OR MORE SUITES FAILED!" -ForegroundColor Red
    Write-Host "================================================================================" -ForegroundColor Red
    exit 1
}
