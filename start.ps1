# PowerShell startup script for AI-Powered Personal Assistant System
# Starts all services: MCP Server, AI Engine, and Frontend

$ErrorActionPreference = "Stop"

# Color functions
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Header($message) {
    Write-Host ""
    Write-ColorOutput Magenta ("=" * 60)
    Write-ColorOutput Magenta "  $message"
    Write-ColorOutput Magenta ("=" * 60)
    Write-Host ""
}

# Store job references
$jobs = @()

# Cleanup function
function Cleanup {
    Write-ColorOutput Yellow "`n`n🛑 Shutting down all services..."
    Get-Job | Stop-Job
    Get-Job | Remove-Job -Force
    Write-ColorOutput Green "✅ All services stopped"
    exit
}

# Register cleanup on Ctrl+C
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

try {
    Write-Header "AI-Powered Personal Assistant System"
    Write-ColorOutput Cyan "Starting all services...`n"

    # Check dependencies
    Write-Header "Checking Dependencies"
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput Green "✓ $pythonVersion"
    } catch {
        Write-ColorOutput Red "✗ Python not found! Please install Python 3.9+"
        exit 1
    }

    # Check Node.js
    try {
        $nodeVersion = node --version 2>&1
        Write-ColorOutput Green "✓ Node.js version: $nodeVersion"
    } catch {
        Write-ColorOutput Red "✗ Node.js not found! Please install Node.js 18+"
        exit 1
    }

    # Check npm
    try {
        $npmVersion = npm --version 2>&1
        Write-ColorOutput Green "✓ npm version: $npmVersion"
    } catch {
        Write-ColorOutput Red "✗ npm not found! Please install npm"
        exit 1
    }

    # Install dependencies
    Write-Header "Installing Dependencies"

    if (Test-Path "mcp-server\requirements.txt") {
        Write-ColorOutput Cyan "📦 Installing MCP Server dependencies..."
        python -m pip install -q -r mcp-server\requirements.txt
    }

    if (Test-Path "ai-engine\requirements.txt") {
        Write-ColorOutput Cyan "📦 Installing AI Engine dependencies..."
        python -m pip install -q -r ai-engine\requirements.txt
    }

    if (-not (Test-Path "frontend\node_modules")) {
        Write-ColorOutput Cyan "📦 Installing Frontend dependencies..."
        Push-Location frontend
        npm install
        Pop-Location
    }

    Write-ColorOutput Green "✅ All dependencies installed"

    # Start services
    Write-Header "Starting Services"

    # Start MCP Server
    Write-ColorOutput Blue "🚀 Starting MCP Server on port 8000..."
    $jobs += Start-Job -ScriptBlock {
        Set-Location $using:PWD\mcp-server
        python -m uvicorn main:app --port 8000 --reload
    }
    Start-Sleep -Seconds 3

    # Start AI Engine
    Write-ColorOutput Cyan "🚀 Starting AI Engine on port 8001..."
    $jobs += Start-Job -ScriptBlock {
        Set-Location $using:PWD\ai-engine
        python -m uvicorn main:app --port 8001 --reload
    }
    Start-Sleep -Seconds 3

    # Start Frontend
    Write-ColorOutput Green "🚀 Starting Frontend on port 3000..."
    $jobs += Start-Job -ScriptBlock {
        Set-Location $using:PWD\frontend
        npm run dev
    }
    Start-Sleep -Seconds 2

    Write-Header "All Services Started Successfully!"
    Write-ColorOutput White "📍 Services running at:"
    Write-ColorOutput Blue "   • MCP Server:  http://localhost:8000"
    Write-ColorOutput Cyan "   • AI Engine:   http://localhost:8001"
    Write-ColorOutput Green "   • Frontend:    http://localhost:3000"
    Write-ColorOutput Yellow "`n💡 Press Ctrl+C to stop all services`n"

    # Monitor jobs
    while ($true) {
        $runningJobs = Get-Job | Where-Object { $_.State -eq 'Running' }
        if ($runningJobs.Count -lt $jobs.Count) {
            Write-ColorOutput Red "⚠️  A service has stopped unexpectedly!"
            Get-Job | Receive-Job
            Cleanup
        }
        Start-Sleep -Seconds 1
    }

} catch {
    Write-ColorOutput Red "Error: $_"
    Cleanup
} finally {
    Cleanup
}
