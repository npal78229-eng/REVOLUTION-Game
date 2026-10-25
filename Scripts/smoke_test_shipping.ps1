$proc = Start-Process -FilePath "C:\Users\npal7\PROJECT\REVOLUTION\Build\Shipping_Windows\Windows\REVOLUTION.exe" -ArgumentList "-windowed -ResX=1280 -ResY=720" -PassThru
Start-Sleep -Seconds 20
if (-not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force
}
Write-Host "Shipping game run complete."
