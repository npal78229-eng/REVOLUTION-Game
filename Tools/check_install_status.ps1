Write-Output "=== INSTALLATION STATUS CHECK ==="

# Check Visual Studio
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vswhere) {
    Write-Output "vswhere.exe FOUND! Querying Visual Studio installations:"
    & $vswhere -all -products * | Out-String | Write-Output
} else {
    Write-Output "vswhere.exe: Not yet present."
}

# Check VS Installer directories
$vsPaths = @(
    "C:\Program Files\Microsoft Visual Studio\2022",
    "C:\Program Files (x86)\Microsoft Visual Studio\Installer",
    "C:\ProgramData\Microsoft\VisualStudio\Packages"
)
foreach ($vp in $vsPaths) {
    if (Test-Path $vp) {
        Write-Output "Found VS directory: $vp"
    }
}

# Check Epic Games UE directories
Write-Output "--- Epic Games Status ---"
$ueItems = Get-ChildItem "C:\Program Files\Epic Games" -ErrorAction SilentlyContinue
foreach ($item in $ueItems) {
    Write-Output "  - $($item.FullName) ($($item.Mode))"
}

# Check Active Installer processes
Write-Output "--- Active Installer Processes ---"
Get-Process -ErrorAction SilentlyContinue | Where-Object { 
    $_.Name -match "setup|installer|epic|visualstudio|vs_|msiexec" 
} | Select-Object Name, Id, Responding, CPU | Format-Table -AutoSize | Out-String | Write-Output
