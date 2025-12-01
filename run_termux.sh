cat > run_termux.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

# Telegram Member Bot - Termux Runner
# File: run_termux.sh

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   TELEGRAM MEMBER BOT - TERMUX      ║"
echo "║       REAL WORKING SCRIPT           ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
error() {
    echo -e "${RED}❌ $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Termux
if [ ! -d "/data/data/com.termux/files/home" ]; then
    warning "Not running in Termux"
fi

# Step 1: Check Python
info "Step 1: Checking Python..."
if command -v python3 &> /dev/null; then
    success "Python3 is installed: $(python3 --version)"
else
    error "Python3 not found!"
    echo "Installing Python..."
    pkg install python -y
fi

# Step 2: Check dependencies
info "Step 2: Checking dependencies..."
if pip list | grep -q telethon; then
    success "Telethon is installed"
else
    warning "Telethon not found, installing..."
    pip install telethon colorama
fi

# Step 3: Check files
info "Step 3: Checking files..."

if [ -f "real_bot.py" ]; then
    success "Main script found: real_bot.py"
    
    # Check if API is still default
    if grep -q "API_ID = 1234567" real_bot.py; then
        error "API credentials not configured!"
        echo ""
        info "📋 HOW TO CONFIGURE:"
        info "1. Get API from https://my.telegram.org"
        info "2. Edit real_bot.py (lines 15-17)"
        info "3. Set: API_ID, API_HASH, PHONE"
        echo ""
        echo "Edit now? (y/n)"
        read -r answer
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            nano real_bot.py
        fi
    else
        success "API credentials configured"
    fi
else
    error "Main script not found!"
    echo "Creating real_bot.py..."
    # Create minimal script
    cat > real_bot.py << 'SCRIPT'
#!/usr/bin/env python3
print("Please download the full script from GitHub")
print("Or copy the complete real_bot.py")
SCRIPT
fi

# Step 4: Check members.csv
if [ -f "members.csv" ]; then
    line_count=$(wc -l < members.csv)
    success "members.csv found with $line_count lines"
    
    # Show first 5 members
    echo ""
    info "First 5 members in members.csv:"
    head -n 10 members.csv | grep -v "^#" | head -n 5
else
    warning "members.csv not found, creating..."
    cat > members.csv << 'MEMBERS'
# Add target usernames here
# Format: username (with or without @)
# Example:
# @username1
# username2

# Add real usernames below:
MEMBERS
    success "Created members.csv"
fi

# Step 5: Run the bot
echo ""
info "Step 4: Running the bot..."
echo ""

# Ask for confirmation
warning "⚠️  IMPORTANT NOTES:"
echo "1. You must be ADMIN in target group"
echo "2. Group must allow adding members"
echo "3. Start with 5-10 members per day"
echo "4. Use 30+ seconds delay between adds"
echo ""
echo "Continue? (y/n)"
read -r confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    success "🚀 Starting Telegram Member Bot..."
    echo "──────────────────────────────────────"
    python3 real_bot.py
else
    echo ""
    info "Setup complete. You can run later with:"
    info "python3 real_bot.py"
fi

echo ""
info "📱 Need help?"
info "1. Edit config: nano real_bot.py"
info "2. Add members: nano members.csv"
info "3. Run again: python3 real_bot.py"
echo ""
EOF

chmod +x run_termux.sh
