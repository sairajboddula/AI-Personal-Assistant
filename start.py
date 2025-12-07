#!/usr/bin/env python3
"""
Unified Startup Script for AI Personal Assistant
Starts AI Engine and Frontend with new backend structure
"""

import subprocess
import sys
import time
import os
import signal
import platform
from pathlib import Path

# Set UTF-8 encoding for Windows console to support emojis
if platform.system() == "Windows":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
    # Set console to UTF-8
    os.system("chcp 65001 >nul 2>&1")

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    """Print colored message"""
    print(f"{color}{message}{Colors.ENDC}")

def print_header(message):
    """Print header message"""
    print_colored(f"\n{'='*50}", Colors.OKCYAN)
    print_colored(f"  {message}", Colors.BOLD)
    print_colored(f"{'='*50}\n", Colors.OKCYAN)

def check_dependencies():
    """Check if required dependencies are installed"""
    print_colored("🔍 Checking dependencies...", Colors.OKBLUE)
    
    # Check Python packages
    try:
        import fastapi
        import uvicorn
        import mcp
        print_colored("✅ Backend dependencies installed", Colors.OKGREEN)
    except ImportError as e:
        print_colored(f"❌ Missing backend dependencies: {e}", Colors.FAIL)
        print_colored("Installing backend dependencies...", Colors.WARNING)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check Node.js and npm
    try:
        # On Windows, we need shell=True to find commands in PATH
        is_windows = platform.system() == "Windows"
        
        node_result = subprocess.run(
            ["node", "--version"], 
            capture_output=True, 
            shell=is_windows,
            text=True
        )
        npm_result = subprocess.run(
            ["npm", "--version"], 
            capture_output=True, 
            shell=is_windows,
            text=True
        )
        
        if node_result.returncode == 0 and npm_result.returncode == 0:
            print_colored("✅ Node.js and npm installed", Colors.OKGREEN)
            print_colored(f"   Node: {node_result.stdout.strip()}", Colors.OKCYAN)
            print_colored(f"   npm: {npm_result.stdout.strip()}", Colors.OKCYAN)
        else:
            raise FileNotFoundError("Node.js or npm not found")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print_colored("❌ Node.js or npm not found in PATH", Colors.FAIL)
        print_colored("", Colors.WARNING)
        print_colored("Please ensure Node.js is installed and added to PATH:", Colors.WARNING)
        print_colored("1. Download from: https://nodejs.org/", Colors.WARNING)
        print_colored("2. During installation, check 'Add to PATH'", Colors.WARNING)
        print_colored("3. Restart your terminal/PowerShell", Colors.WARNING)
        print_colored("", Colors.WARNING)
        print_colored("Or start services manually:", Colors.OKBLUE)
        print_colored("  AI Engine: python -m uvicorn backend.ai_engine.main:app --port 8001", Colors.OKCYAN)
        print_colored("  Frontend:  cd frontend && npm run dev", Colors.OKCYAN)
        sys.exit(1)
    
    # Check if frontend dependencies are installed
    if not Path("frontend/node_modules").exists():
        print_colored("📦 Installing frontend dependencies...", Colors.WARNING)
        is_windows = platform.system() == "Windows"
        subprocess.run(["npm", "install"], cwd="frontend", shell=is_windows, check=True)
    else:
        print_colored("✅ Frontend dependencies installed", Colors.OKGREEN)

def wait_for_service(url, service_name, max_attempts=30):
    """Wait for a service to be ready"""
    import urllib.request
    import urllib.error
    
    print_colored(f"⏳ Waiting for {service_name} to be ready...", Colors.OKBLUE)
    
    for attempt in range(max_attempts):
        try:
            urllib.request.urlopen(url, timeout=1)
            print_colored(f"✅ {service_name} is ready!", Colors.OKGREEN)
            return True
        except (urllib.error.URLError, ConnectionRefusedError, TimeoutError):
            time.sleep(1)
            if attempt % 5 == 0 and attempt > 0:
                print_colored(f"   Still waiting... ({attempt}/{max_attempts})", Colors.WARNING)
    
    print_colored(f"❌ {service_name} failed to start", Colors.FAIL)
    return False

def main():
    """Main startup function"""
    print_header("AI Personal Assistant - Startup")
    print_colored("🚀 Starting services with new backend structure...\n", Colors.BOLD)
    
    # Check dependencies
    check_dependencies()
    
    processes = []
    
    try:
        # Start AI Engine with new path
        print_colored("🚀 Starting AI Engine on port 8001...", Colors.OKBLUE)
        print_colored("   Using: backend/ai_engine/main.py", Colors.OKCYAN)
        ai_engine = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.ai_engine.main:app", "--port", "8001", "--reload"],
            cwd="."
        )
        processes.append(("AI Engine", ai_engine))
        
        # Wait for AI Engine
        if not wait_for_service("http://localhost:8001/health", "AI Engine"):
            raise Exception("AI Engine failed to start")
        
        # Start Frontend
        print_colored("🚀 Starting Frontend on port 3000...", Colors.OKBLUE)
        is_windows = platform.system() == "Windows"
        frontend = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd="frontend",
            shell=is_windows
        )
        processes.append(("Frontend", frontend))
        
        # Wait a bit for frontend
        time.sleep(3)
        
        # Success message
        print_header("All Services Started Successfully!")
        print_colored("📍 Services running at:", Colors.OKGREEN)
        print_colored("   • AI Engine:   http://localhost:8001", Colors.OKBLUE)
        print_colored("   • Frontend:    http://localhost:3000", Colors.OKBLUE)
        print_colored("\n📦 New Backend Structure:", Colors.OKGREEN)
        print_colored("   • backend/ai_engine/     - AI Engine package", Colors.OKCYAN)
        print_colored("   • backend/mcp_servers/   - MCP Servers package", Colors.OKCYAN)
        print_colored("   • requirements.txt       - Consolidated dependencies", Colors.OKCYAN)
        print_colored("\n💡 Press Ctrl+C to stop all services\n", Colors.WARNING)
        
        # Wait for processes
        for name, process in processes:
            process.wait()
    
    except KeyboardInterrupt:
        print_colored("\n\n🛑 Shutting down all services...", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Error: {e}", Colors.FAIL)
    finally:
        # Cleanup
        for name, process in processes:
            try:
                if platform.system() == "Windows":
                    process.terminate()
                else:
                    process.send_signal(signal.SIGTERM)
                process.wait(timeout=5)
                print_colored(f"✅ {name} stopped", Colors.OKGREEN)
            except subprocess.TimeoutExpired:
                process.kill()
                print_colored(f"⚠️  {name} force killed", Colors.WARNING)
            except Exception as e:
                print_colored(f"⚠️  Error stopping {name}: {e}", Colors.WARNING)
        
        print_colored("\n✅ All services stopped\n", Colors.OKGREEN)

if __name__ == "__main__":
    main()
