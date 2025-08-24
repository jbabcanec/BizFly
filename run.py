#!/usr/bin/env python3
"""
BizFly - Single Entry Point Runner

This script provides a Python entry point for running BizFly.
Alternative to the bash script for cross-platform compatibility.
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def print_header(text):
    print(f"\n🚀 {text}")
    print("=" * (len(text) + 3))


def print_status(text):
    print(f"✅ {text}")


def print_error(text):
    print(f"❌ {text}")


def print_warning(text):
    print(f"⚠️  {text}")


def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print_warning(".env file not found. Creating from template...")
        subprocess.run(["cp", ".env.example", ".env"])
        print_error("Please edit .env file with your API keys:")
        print("- GOOGLE_MAPS_API_KEY")
        print("- ANTHROPIC_API_KEY")
        return False
    
    # Check for required keys
    env_content = env_file.read_text()
    required_keys = ["GOOGLE_MAPS_API_KEY", "ANTHROPIC_API_KEY"]
    
    for key in required_keys:
        if f"{key}=" not in env_content or f"{key}=your-" in env_content:
            print_error(f"Please set {key} in .env file")
            return False
    
    return True


def check_docker():
    """Check if Docker and docker-compose are available"""
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_with_docker():
    """Run BizFly using Docker"""
    print_header("Running with Docker")
    
    print_status("Building and starting services...")
    subprocess.run(["docker-compose", "up", "--build", "-d"], check=True)
    
    print_status("Waiting for services to start...")
    time.sleep(10)
    
    print_status("Seeding database with templates...")
    try:
        subprocess.run([
            "docker-compose", "exec", "-T", "backend", 
            "python", "scripts/seed_templates.py"
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print_warning("Template seeding skipped (may already exist)")
    
    print_header("BizFly is running!")
    print("🌐 Frontend: http://localhost:3000")
    print("⚡ Backend API: http://localhost:8000") 
    print("📊 API Docs: http://localhost:8000/docs")
    print("\nTo stop: docker-compose down")


def run_manual():
    """Run BizFly manually"""
    print_header("Running manual setup")
    print_warning("Make sure PostgreSQL and Redis are running")
    
    # Setup backend
    print_status("Setting up backend...")
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    if not venv_dir.exists():
        print_status("Creating Python virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        activate_script = venv_dir / "Scripts" / "activate.bat"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:  # Unix
        activate_script = venv_dir / "bin" / "activate"
        python_exe = venv_dir / "bin" / "python"
    
    # Install requirements
    print_status("Installing backend dependencies...")
    subprocess.run([
        str(python_exe), "-m", "pip", "install", "-r", "requirements.txt"
    ], cwd=backend_dir, check=True)
    
    # Setup frontend
    print_status("Setting up frontend...")
    frontend_dir = Path("frontend")
    
    if not (frontend_dir / "node_modules").exists():
        print_status("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    
    print_header("BizFly setup complete!")
    print("To start the services:")
    print("1. Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload")
    print("2. Frontend: cd frontend && npm run dev")


def main():
    print_header("BizFly - Business Website Generation Platform")
    
    # Check environment
    if not check_env_file():
        return
    
    # Choose deployment method
    if check_docker():
        run_with_docker()
    else:
        print_warning("Docker not found. Using manual setup...")
        run_manual()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)