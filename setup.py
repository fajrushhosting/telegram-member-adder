cat > setup.py << 'EOF'
#!/usr/bin/env python3
"""
Setup Script untuk Termux
"""

import os
import sys
import subprocess

def run_command(cmd):
    """Run shell command"""
    print(f"📦 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    return result.returncode

def main():
    print("🔧 Telegram Member Bot Setup")
    print("="*50)
    
    # Check Termux
    if os.path.exists('/data/data/com.termux/files/home'):
        print("📱 Detected: Termux Android")
        
        # Update Termux packages
        print("\n🔄 Updating Termux packages...")
        run_command("pkg update -y && pkg upgrade -y")
        
        # Install Python
        print("\n🐍 Installing Python...")
        run_command("pkg install python -y")
        
        # Install git (optional)
        print("\n📦 Installing git...")
        run_command("pkg install git -y")
    
    # Install Python packages
    print("\n📦 Installing Python dependencies...")
    packages = [
        "telethon",
        "colorama",
        "python-dotenv"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        run_command(f"pip install {package}")
    
    # Create necessary files
    print("\n📁 Creating files...")
    
    # Create members.csv if not exists
    if not os.path.exists("members.csv"):
        with open("members.csv", "w") as f:
            f.write("# Add usernames here\n")
            f.write("@real_user_1\n")
            f.write("real_user_2\n")
        print("✅ Created members.csv")
    
    # Create .env.example
    with open(".env.example", "w") as f:
        f.write("""# Telegram API Configuration
# Get from: https://my.telegram.org

API_ID=1234567
API_HASH=abcdef1234567890abcdef
PHONE_NUMBER=+6281234567890

# Settings
DELAY=30
""")
    print("✅ Created .env.example")
    
    # Create run.sh
    with open("run.sh", "w") as f:
        f.write("""#!/bin/bash
echo "🚀 Running Telegram Member Bot..."
python real_bot.py
""")
    os.chmod("run.sh", 0o755)
    print("✅ Created run.sh")
    
    print("\n" + "="*50)
    print("✅ SETUP COMPLETE!")
    print("\n📋 NEXT STEPS:")
    print("1. Edit real_bot.py - Set your API credentials")
    print("   - Line 15-17: API_ID, API_HASH, PHONE")
    print("2. Add usernames to members.csv")
    print("3. Run: python real_bot.py")
    print("\n⚠️  IMPORTANT:")
    print("- You must be ADMIN in the target group")
    print("- Group must allow adding members")
    print("- Start with 5-10 members per day")
    print("="*50)

if __name__ == "__main__":
    main()
EOF

python setup.py
