$blenderDir = "C:\Program Files\Blender Foundation\Blender 5.2"
if (Test-Path $blenderDir) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$blenderDir*") {
        $newPath = "$currentPath;$blenderDir"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Output "SUCCESS: Added Blender 5.2 to User PATH: $blenderDir"
    } else {
        Write-Output "INFO: Blender 5.2 is already in User PATH."
    }
} else {
    Write-Output "WARNING: Blender directory not found at $blenderDir"
}

# Also verify git and git-lfs in environment
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
$lfsCheck = Get-Command git-lfs -ErrorAction SilentlyContinue
Write-Output "Git verified: $($gitCheck.Source)"
Write-Output "Git LFS verified: $($lfsCheck.Source)"
