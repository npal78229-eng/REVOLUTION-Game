$proc = Start-Process -FilePath "C:\Users\npal7\PROJECT\REVOLUTION\Build\Candidate_Windows\Windows\REVOLUTION.exe" -ArgumentList "-windowed -ResX=1280 -ResY=720 -log -LOG=Candidate_Final.log" -PassThru
Start-Sleep -Seconds 25
if (-not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force
}
Write-Host "Candidate game run complete."
