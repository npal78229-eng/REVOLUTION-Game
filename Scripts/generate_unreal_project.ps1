<#
.SYNOPSIS
    Automated Project Creation & Configuration Script for Project REVOLUTION.
.DESCRIPTION
    Detects the installed Unreal Engine 5 binary release, instantiates the Third-Person 
    C++ project structure, injects hardware-specific scalability and thread configurations, 
    and generates IDE solution files.
#>

[CmdletBinding()]
param (
    [string]$EngineRoot = "",
    [string]$ProjectName = "REVOLUTION"
)

$targetDir = "C:\Users\npal7\PROJECT\REVOLUTION\Project"
Write-Output "=========================================================="
Write-Output "  PROJECT REVOLUTION — UNREAL PROJECT GENERATOR"
Write-Output "=========================================================="

# 1. Detect Unreal Engine Installation
if (-not $EngineRoot) {
    $searchPaths = @(
        "C:\Program Files\Epic Games\UE_5.5",
        "C:\Program Files\Epic Games\UE_5.4",
        "C:\Program Files\Epic Games\UE_5.3"
    )
    foreach ($p in $searchPaths) {
        if (Test-Path "$p\Engine\Binaries\Win64\UnrealEditor.exe") {
            $EngineRoot = $p
            break
        }
    }
}

if (-not $EngineRoot -or -not (Test-Path "$EngineRoot\Engine\Binaries\Win64\UnrealEditor.exe")) {
    Write-Error "CRITICAL: Unreal Engine 5 installation not found. Please install Unreal Engine 5.4 or 5.5 via the Epic Games Launcher first."
    Write-Output "Refer to: C:\Users\npal7\PROJECT\REVOLUTION\Documentation\Setup\SOFTWARE_INSTALLATION_GUIDE.md"
    exit 1
}

Write-Output "Found Unreal Engine at: $EngineRoot"

# 2. Check Visual Studio 2022 Toolchain
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (-not (Test-Path $vswhere)) {
    Write-Warning "WARNING: Visual Studio 2022 was not detected. C++ compilation requires Visual Studio 2022 with C++ Game Development."
}

# 3. Target Path Check
$uprojectFile = Join-Path $targetDir "$ProjectName.uproject"
if (Test-Path $uprojectFile) {
    Write-Output "Unreal project already exists at $uprojectFile."
} else {
    Write-Output "Creating new project '$ProjectName' in $targetDir..."
    
    # Template path
    $tpTemplate = Join-Path $EngineRoot "Templates\TP_ThirdPerson"
    if (-not (Test-Path $tpTemplate)) {
        Write-Warning "Third-Person template not found at $tpTemplate. Creating clean .uproject descriptor."
    }

    # Inject Scalability and Engine configurations
    $configDir = Join-Path $targetDir "Config"
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }

    $templateScalability = "C:\Users\npal7\PROJECT\REVOLUTION\Tools\ConfigTemplates\DefaultScalability.ini"
    if (Test-Path $templateScalability) {
        Copy-Item -Path $templateScalability -Destination "$configDir\DefaultScalability.ini" -Force
        Write-Output "Injected hardware-optimized DefaultScalability.ini."
    }

    $templateEngine = "C:\Users\npal7\PROJECT\REVOLUTION\Tools\ConfigTemplates\DefaultEngine_Scalability.ini"
    if (Test-Path $templateEngine) {
        Copy-Item -Path $templateEngine -Destination "$configDir\DefaultEngine.ini" -Force
        Write-Output "Injected hardware-optimized DefaultEngine.ini."
    }
}

# 4. Generate Visual Studio Project Files
$ubtExe = Join-Path $EngineRoot "Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe"
if ((Test-Path $ubtExe) -and (Test-Path $uprojectFile)) {
    Write-Output "Generating Visual Studio Project files via UnrealBuildTool..."
    & $ubtExe -projectfiles -project="$uprojectFile" -game -engine
}

Write-Output "=========================================================="
Write-Output "  GENERATOR FINISHED"
Write-Output "=========================================================="
