param (
    [int]$WarningThresholdGB = 25
)

$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)
$totalGB = [math]::Round($disk.Size / 1GB, 2)
$pctFree = [math]::Round(($freeGB / $totalGB) * 100, 1)

Write-Output "================================================="
Write-Output "  PROJECT REVOLUTION — DISK SPACE MONITOR"
Write-Output "================================================="
Write-Output "Drive C: Total: $totalGB GB | Free: $freeGB GB ($pctFree% available)"

if ($freeGB -lt $WarningThresholdGB) {
    Write-Warning "LOW DISK SPACE ALERT! Free space ($freeGB GB) is below safety threshold of $WarningThresholdGB GB."
} else {
    Write-Output "STATUS: Disk space is within acceptable operational range."
}

# Check Project directory size
$projPath = "C:\Users\npal7\PROJECT\REVOLUTION"
if (Test-Path $projPath) {
    $projSizeMB = [math]::Round((Get-ChildItem -Path $projPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    Write-Output "REVOLUTION Directory Size: $projSizeMB MB"
}

# Check Unreal Engine default cache directory
$ddcPath = "$env:LOCALAPPDATA\UnrealEngine\Common\DerivedDataCache"
if (Test-Path $ddcPath) {
    $ddcSizeGB = [math]::Round((Get-ChildItem -Path $ddcPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB, 2)
    Write-Output "Unreal Engine DDC Cache Size: $ddcSizeGB GB"
} else {
    Write-Output "Unreal Engine DDC Cache: Not yet generated."
}
