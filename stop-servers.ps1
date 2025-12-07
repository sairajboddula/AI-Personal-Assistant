# Stop All Servers Script - Fixed Version
# Kills all running AI Assistant services

Write-Host "Stopping all AI Personal Assistant services..." -ForegroundColor Cyan

# Kill processes on specific ports
$ports = @(3000, 3001, 8001)

foreach ($port in $ports) {
    $connections = netstat -ano | Select-String ":$port" | Select-String "LISTENING"
    
    foreach ($connection in $connections) {
        if ($connection -match "LISTENING\s+(\d+)") {
            $processId = $Matches[1]  # Use different variable name to avoid $PID conflict
            try {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-Host "[OK] Stopped process on port $port (PID: $processId)" -ForegroundColor Green
            } catch {
                Write-Host "[WARN] Could not stop PID $processId" -ForegroundColor Yellow
            }
        }
    }
}

# Remove Next.js lock file
$lockFile = "frontend\.next\dev\lock"
if (Test-Path $lockFile) {
    Remove-Item $lockFile -Force
    Write-Host "[OK] Removed Next.js lock file" -ForegroundColor Green
}

# Clean up .next directory if needed
if (Test-Path "frontend\.next") {
    Write-Host "[INFO] Cleaning .next directory..." -ForegroundColor Cyan
    Remove-Item "frontend\.next" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Cleaned .next directory" -ForegroundColor Green
}

# Verify all ports are clear
Write-Host "`nVerifying ports are clear..." -ForegroundColor Cyan
Start-Sleep -Seconds 1
$stillRunning = netstat -ano | Select-String ":3000|:3001|:8001" | Select-String "LISTENING"

if ($stillRunning) {
    Write-Host "[WARN] Some ports are still in use:" -ForegroundColor Yellow
    $stillRunning
    Write-Host "`nTry restarting your computer if ports remain locked." -ForegroundColor Yellow
} else {
    Write-Host "[OK] All ports are clear!" -ForegroundColor Green
}

Write-Host "`nDone! You can now run 'python start.py'" -ForegroundColor Cyan
