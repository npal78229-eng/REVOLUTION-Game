$uri = "https://aka.ms/vs/17/release/vs_community.exe"
$out = "C:\Users\npal7\Downloads\VisualStudioSetup.exe"
Write-Output "Downloading $uri to $out..."
Invoke-WebRequest -Uri $uri -OutFile $out -UseBasicParsing
$item = Get-Item $out
Write-Output "Downloaded successfully: $($item.FullName) ($($item.Length) bytes)"
