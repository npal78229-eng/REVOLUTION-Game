param (
    [string]$Label = "manual"
)

$root = "C:\Users\npal7\PROJECT\REVOLUTION"
$backupDir = "$root\Backups"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveName = "REVOLUTION_Snapshot_${timestamp}_${Label}.zip"
$destinationZip = Join-Path $backupDir $archiveName

Write-Output "Creating snapshot backup: $archiveName"

# Create a temporary staging folder for files to back up
$stagingDir = "$env:TEMP\REVOLUTION_Backup_Staging_$timestamp"
New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

try {
    # Include Documentation, Design, Scripts, Tools, SourceControl
    $includeFolders = @("Documentation", "Design", "Scripts", "Tools", "SourceControl")
    foreach ($folder in $includeFolders) {
        $src = Join-Path $root $folder
        if (Test-Path $src) {
            $dest = Join-Path $stagingDir $folder
            Copy-Item -Path $src -Destination $dest -Recurse -Force
        }
    }
    
    # Include root files (.md, .gitignore, etc.)
    Get-ChildItem -Path $root -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $stagingDir -Force
    }

    # Include Project Source, Config, and .uproject if present (exclude Intermediate, Saved, Binaries)
    $projectDir = Join-Path $root "Project"
    if (Test-Path $projectDir) {
        $projStaging = Join-Path $stagingDir "Project"
        New-Item -ItemType Directory -Path $projStaging -Force | Out-Null
        
        $projItems = @("Source", "Config")
        foreach ($pi in $projItems) {
            $srcPi = Join-Path $projectDir $pi
            if (Test-Path $srcPi) {
                Copy-Item -Path $srcPi -Destination (Join-Path $projStaging $pi) -Recurse -Force
            }
        }
        Get-ChildItem -Path $projectDir -Filter "*.uproject" | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $projStaging -Force
        }
    }

    # Compress to Zip
    Compress-Archive -Path "$stagingDir\*" -DestinationPath $destinationZip -CompressionLevel Optimal -Force
    $zipSizeKB = [math]::Round((Get-Item $destinationZip).Length / 1KB, 2)
    Write-Output "SUCCESS: Backup created at $destinationZip ($zipSizeKB KB)"
} finally {
    if (Test-Path $stagingDir) {
        Remove-Item -Path $stagingDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
