#!/usr/bin/env python3
"""
Setup script for Auto Lister
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Auto Lister...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version} detected")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("💡 Try using: python -m pip install -r requirements.txt")
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install chromium", "Installing Playwright browsers"):
        print("💡 You may need to run: python -m playwright install chromium")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Create item folders in the 'items/' directory")
    print("2. Each folder should contain:")
    print("   - info.json (with title, description, price, platforms)")
    print("   - One or more image files")
    print("3. Run: python Main.py")
    print("\n💡 See items/sample_item/ for an example structure")
    print("\n⚠️  Make sure you're logged into your marketplace accounts in the browser")

if __name__ == "__main__":
    main()
