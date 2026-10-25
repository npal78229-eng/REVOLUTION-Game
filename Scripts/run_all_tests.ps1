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
        Name = 'Act I Narrative Story Questline and Landmarks [205 Actors]'
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
    },
    @{
        Id = 'TEST-09'
        Name = 'SteamOS & Handheld Proton Scalability Profile and Controller Mappings'
        Script = "$ScriptsDir\verify_steamos_handheld_profile.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-10'
        Name = 'Advanced Photogrammetry Texturing & Material Architecture'
        Script = "$ScriptsDir\verify_photogrammetry_materials.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-11'
        Name = 'Historical Narrative Epilogue, Codex 18th Record and Cinematic Director'
        Script = "$ScriptsDir\verify_task25_epilogue.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-12'
        Name = 'Multi-Dialect Punjabi Voice Recording Expansion and Bazaar Walla System'
        Script = "$ScriptsDir\verify_task26_multidialect_walla.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-13'
        Name = 'Dynamic Time-of-Day Weather States, Andhi Dust Storm and Volumetric Fog'
        Script = "$ScriptsDir\verify_task27_weather_states.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-14'
        Name = 'Curfew Sentry AI Collision Resolution and 3-Waypoint Patrol Routine'
        Script = "$ScriptsDir\verify_curfew_patrol.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-15'
        Name = 'Frontend Title Screen, Pause Menu System and Checkpoint Restart Loop'
        Script = "$ScriptsDir\verify_frontend_menus.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-16'
        Name = 'Persistent Disk Save/Load System (USaveGame) and Continue Journey Loop'
        Script = "$ScriptsDir\verify_save_load_system.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-17'
        Name = 'Procedural Skeletal Idle Animations, Occupational Routine Life and Heritage Attire'
        Script = "$ScriptsDir\verify_civilian_routines.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-18'
        Name = 'Haveli Ground Floor Domestic Dressing and Village Exploration Boundaries'
        Script = "$ScriptsDir\verify_haveli_boundaries.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-19'
        Name = 'Rooftop Traversal, Vertical Ladder Traversal and Mantling Feedback'
        Script = "$ScriptsDir\verify_rooftop_traversal.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-20'
        Name = 'Seamless Act I In-World Objective Beacons & Mohalla Compass Waypoints'
        Script = "$ScriptsDir\verify_objective_beacons.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-21'
        Name = 'Act I Finale to Act II Cinematic Handoff & Munadi Proclamation Sequence'
        Script = "$ScriptsDir\verify_act1_to_act2_handoff.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-22'
        Name = 'Grand Bazaar Chowk Munadi Crowd Clatter & Dynamic Dialogue System'
        Script = "$ScriptsDir\verify_chowk_munadi_crowd.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-23'
        Name = 'Act II Questline: ''The Rumors of Baisakhi'' & Checkpost Eavesdropping'
        Script = "$ScriptsDir\verify_act2_questline.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-24'
        Name = 'Baisakhi Fair Ground Atmosphere & Gathering Expansion'
        Script = "$ScriptsDir\verify_baisakhi_fairground.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-25'
        Name = 'RDR2-Inspired Volumetric Smoke, Curl Noise Flow & Atmospheric Optics'
        Script = "$ScriptsDir\verify_rdr2_smoke_integration.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-26'
        Name = 'Act II Climax: The Firing Line at Jallianwala Bagh & Escape Traversal'
        Script = "$ScriptsDir\verify_act2_climax_firing_line.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-27'
        Name = 'Act III: The Desolate Night & Clandestine Medical Evacuation'
        Script = "$ScriptsDir\verify_act3_medical_evacuation.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-28'
        Name = 'Act IV: The Rural Outskirts & Upper Bari Doab Canal Feeder Network'
        Script = "$ScriptsDir\verify_act4_canal_outskirts.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-29'
        Name = 'Act IV Climax: Bhatta Brick Kiln Resistance Infiltration & Underground Press'
        Script = "$ScriptsDir\verify_act4_climax_brick_kiln.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-30'
        Name = 'Act V: North Western Railway Cutting, Signal Gantry & Locomotive Climax'
        Script = "$ScriptsDir\verify_act5_railway_climax.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-31'
        Name = 'Community-Trust System [Izzat & Vishwas] & Localized Reputation'
        Script = "$ScriptsDir\verify_community_trust.py"
        Type = 'Commandlet'
    },
    @{
        Id = 'TEST-32'
        Name = 'End-to-End Interactive QA Playthrough Bot & 29-Stage Telemetry'
        Script = "$ScriptsDir\verify_e2e_interactive_playthrough.py"
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
        if ($ExitCode -ne 0) {
            Start-Sleep -Seconds 2
            $Proc = Start-Process -FilePath $UECmd -ArgumentList $ArgsList -NoNewWindow -Wait -PassThru
            $ExitCode = $Proc.ExitCode
        }
    } else {
        $Proc = Start-Process -FilePath $UEPython -ArgumentList "`"$($Test.Script)`"" -NoNewWindow -Wait -PassThru
        $ExitCode = $Proc.ExitCode
    }
    Start-Sleep -Milliseconds 500

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
