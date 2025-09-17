#!/usr/bin/env python3
"""
GitHub Setup Script for AI-Enhanced Incident Response System
Helps prepare the Python project for GitHub upload
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"📋 {description}")
    print(f"💻 Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    print()
    return True

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_git_repo():
    """Set up git repository"""
    print("🚀 Setting up Git repository for Python files only")
    print("=" * 60)
    
    if not check_git_installed():
        print("❌ Git is not installed or not in PATH")
        print("   Please install Git first: https://git-scm.com/")
        return False
    
    # Initialize git repo if not exists
    if not os.path.exists('.git'):
        if not run_command("git init", "Initializing Git repository"):
            return False
    
    # Add Python files
    python_files = [
        "app.py",
        "project.py", 
        "ai_processor.py",
        "run.py",
        "requirements.txt",
        "test_app.py",
        "status_check.py",
        "start.bat",
        "README.md",
        ".gitignore"
    ]
    
    # Check which files exist
    existing_files = []
    missing_files = []
    
    for file in python_files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    print(f"📂 Found {len(existing_files)} Python project files:")
    for file in existing_files:
        print(f"   ✅ {file}")
    
    if missing_files:
        print(f"\n⚠️  Missing files (will be skipped):")
        for file in missing_files:
            print(f"   ❌ {file}")
    
    # Add files to git
    print(f"\n📝 Adding files to git...")
    for file in existing_files:
        if run_command(f"git add {file}", f"Adding {file}"):
            continue
        else:
            print(f"⚠️  Could not add {file}")
    
    # Check git status
    run_command("git status", "Checking git status")
    
    return True

def show_next_steps():
    """Show next steps for GitHub upload"""
    print("🎯 Next Steps for GitHub Upload:")
    print("=" * 40)
    print("1. Commit your changes:")
    print("   git commit -m \"Initial Python incident management system\"")
    print()
    print("2. Create GitHub repository:")
    print("   - Go to https://github.com/new")
    print("   - Name: incident-response-system-python")
    print("   - Description: AI-Enhanced Incident Response System in Python")
    print("   - Make it Public or Private")
    print("   - Don't initialize with README (we have one)")
    print()
    print("3. Add remote origin:")
    print("   git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git")
    print()
    print("4. Push to GitHub:")
    print("   git branch -M main")
    print("   git push -u origin main")
    print()
    print("📋 Files that will be uploaded:")
    python_files = ["app.py", "project.py", "ai_processor.py", "run.py", 
                   "requirements.txt", "README.md", ".gitignore"]
    for file in python_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")

def main():
    """Main function"""
    print("🐍 Python Project GitHub Setup")
    print("=" * 50)
    print("This script will prepare your Python incident management")
    print("system for upload to GitHub (Python files only)")
    print()
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📁 Working in: {project_dir}")
    print()
    
    # Setup git repository
    if setup_git_repo():
        print("✅ Git repository setup complete!")
        print()
        show_next_steps()
    else:
        print("❌ Failed to setup git repository")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())