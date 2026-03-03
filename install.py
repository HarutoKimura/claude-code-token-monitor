#!/usr/bin/env python3
"""
Statusline Installer - Deploy to Claude Code
This script installs statusline.py and properly configures Claude Code settings.json
"""

import json
import os
import shutil
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(message, color):
    print(f"{color}{message}{Colors.NC}")

def print_header():
    print_colored("🚀 Statusline Installer", Colors.BLUE)
    print("==================================")

def get_claude_config_dir():
    """Resolve active Claude Code config directory."""
    config_dir = os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")
    return Path(config_dir).expanduser()

def format_home_path(path):
    """Render paths under home using ~ for readability."""
    path_str = str(path)
    home_str = str(Path.home())
    if path_str == home_str:
        return "~"
    if path_str.startswith(home_str + os.sep):
        return "~" + path_str[len(home_str):]
    return path_str

def check_requirements():
    """Check if required files and Python version are available"""
    # Check Python version
    if sys.version_info < (3, 7):
        print_colored("❌ Error: Python 3.7+ required", Colors.RED)
        sys.exit(1)
    
    # Check if statusline.py exists
    statusline_path = Path("statusline.py")
    if not statusline_path.exists():
        print_colored("❌ Error: statusline.py not found in current directory", Colors.RED)
        print("Please run this installer from the statusline project directory.")
        sys.exit(1)
    
    print_colored("✅ Python 3.7+ found", Colors.GREEN)
    print_colored("✅ statusline.py found", Colors.GREEN)
    return statusline_path

def install_statusline(source_path, claude_dir):
    """Install statusline.py to active Claude config directory"""
    target_path = claude_dir / "statusline.py"
    
    print_colored(f"📁 Creating {format_home_path(claude_dir)} directory...", Colors.YELLOW)
    claude_dir.mkdir(parents=True, exist_ok=True)
    
    print_colored(f"📋 Installing statusline to {target_path}...", Colors.YELLOW)
    shutil.copy2(source_path, target_path)
    target_path.chmod(0o755)  # Make executable
    
    print_colored(f"✅ Installed to {target_path}", Colors.GREEN)
    return target_path

def choose_display_option(statusline_script):
    """Let user choose display option by showing examples"""
    print()
    print_colored("🎨 Choose your status line display:", Colors.BLUE)
    print("="*50)
    script_command = str(statusline_script)
    
    # Display options with examples
    options = {
        "1": {
            "name": "Full Display (3 lines)",
            "command": script_command,
            "example": [
                "[Opus 4.6] | 🌿 main M2 +1 | 📁 statusline | 💬 254",
                "🪙  Compact: 116.0K/200.0K ████████▒▒▒▒▒▒▒ 58% ♻️  99% cached 💰 Cost: $0.031",
                "🔥 Burn:    2.1K (Rate: 127 t/m) ▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▁▁▂▃▄▅▆"
            ]
        },
        "2": {
            "name": "Simple Display (2 lines)",
            "command": f"{script_command} --show simple",
            "example": [
                "🪙  Compact: 116.0K/200.0K ████████▒▒▒▒▒▒▒ 58% ♻️  99% cached 💰 Cost: $0.031",
                "🔥 Burn:    2.1K (Rate: 127 t/m) ▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▁▁▂▃▄▅▆"
            ]
        },
        "3": {
            "name": "Essential Display (2 lines)",
            "command": f"{script_command} --show 1,2",
            "example": [
                "[Opus 4.6] | 🌿 main M2 +1 | 📁 statusline | 💬 254",
                "🪙  Compact: 116.0K/200.0K ████████▒▒▒▒▒▒▒ 58% ♻️  99% cached 💰 Cost: $0.031"
            ]
        },
        "4": {
            "name": "Minimal Display (1 line)",
            "command": f"{script_command} --show 2",
            "example": [
                "🪙  Compact: 116.0K/200.0K ████████▒▒▒▒▒▒▒ 58% ♻️  99% cached 💰 Cost: $0.031"
            ]
        }
    }
    
    # Show options
    for key, option in options.items():
        print()
        print_colored(f"{key}. {option['name']}", Colors.YELLOW)
        for line in option['example']:
            print(f"   {line}")
    
    print()
    while True:
        try:
            choice = input("Choose option (1-4) [default: 2]: ").strip()
            if not choice:
                choice = "2"  # Default to simple
            
            if choice in options:
                selected = options[choice]
                print_colored(f"✅ Selected: {selected['name']}", Colors.GREEN)
                return selected['command']
            else:
                print_colored("❌ Invalid choice. Please enter 1, 2, 3, or 4.", Colors.RED)
        except KeyboardInterrupt:
            print_colored("\n❌ Installation cancelled by user", Colors.RED)
            sys.exit(1)
        except EOFError:
            print_colored("\n❌ Installation cancelled", Colors.RED)
            sys.exit(1)

def configure_claude_settings(statusline_command, claude_dir):
    """Configure Claude Code settings.json with proper JSON handling"""
    settings_path = claude_dir / "settings.json"
    
    # statusLine configuration with chosen command
    statusline_config = {
        "type": "command",
        "command": statusline_command,
        "padding": 0
    }
    
    if settings_path.exists():
        print_colored("📝 Updating existing Claude Code settings...", Colors.YELLOW)
        
        # Create backup first (before any file operations)
        backup_path = settings_path.with_suffix('.json.backup')
        try:
            shutil.copy2(settings_path, backup_path)
            print_colored(f"💾 Backup created: {backup_path}", Colors.BLUE)
        except Exception as e:
            print_colored(f"❌ Error creating backup: {e}", Colors.RED)
            print_colored("   Installation aborted for safety", Colors.YELLOW)
            sys.exit(1)
        
        try:
            # Read existing settings
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Check if statusLine already exists
            if 'statusLine' in settings:
                print_colored("✅ statusLine configuration already exists", Colors.GREEN)
                print_colored("   Updating with new configuration...", Colors.YELLOW)
            
            # Update statusLine configuration
            settings['statusLine'] = statusline_config
            
            # Write updated settings
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            print_colored("✅ Claude Code settings updated", Colors.GREEN)
            
        except json.JSONDecodeError as e:
            print_colored(f"❌ Error: Invalid JSON in {settings_path}", Colors.RED)
            print_colored(f"   JSON Error: {e}", Colors.RED)
            print_colored("   Please fix the JSON syntax and run the installer again.", Colors.YELLOW)
            sys.exit(1)
        except Exception as e:
            print_colored(f"❌ Error updating settings: {e}", Colors.RED)
            sys.exit(1)
    
    else:
        print_colored("📝 Creating new Claude Code settings...", Colors.YELLOW)
        
        # Create new settings file
        settings = {
            "statusLine": statusline_config
        }
        
        # Ensure directory exists
        settings_path.parent.mkdir(exist_ok=True)
        
        # Write settings file
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        print_colored(f"✅ Created Claude Code settings at {settings_path}", Colors.GREEN)
    
    return settings_path

def print_success_message(target_path, settings_path, statusline_command):
    """Print installation success message"""
    print()
    print_colored("🎉 Installation Complete!", Colors.GREEN)
    print("==================================")
    print_colored(f"📍 Statusline installed to: {target_path}", Colors.BLUE)
    print_colored(f"⚙️  Claude Code settings: {settings_path}", Colors.BLUE)
    print_colored(f"🎨 Display command: {statusline_command}", Colors.BLUE)
    print()
    print_colored("Next Steps:", Colors.YELLOW)
    print("1. Restart Claude Code to see the new status line")
    print(f"2. Test manually: {statusline_command}")
    print()
    print_colored("💡 Tip: You can change display options anytime:", Colors.BLUE)
    print(f"   • Edit {format_home_path(settings_path)}")
    print("   • Or modify SHOW_LINE1-4 variables in statusline.py")
    print("   • Available options: --show simple, --show all, --show 1,2,3,4")
    print()
    print_colored("Happy coding with Claude! 🚀", Colors.GREEN)

def main():
    """Main installation function"""
    try:
        print_header()
        claude_dir = get_claude_config_dir()
        print_colored(f"📂 Claude config dir: {format_home_path(claude_dir)}", Colors.BLUE)
        
        # Check requirements
        statusline_path = check_requirements()
        
        # Install statusline
        target_path = install_statusline(statusline_path, claude_dir)
        
        # Let user choose display option
        statusline_command = choose_display_option(target_path)
        
        # Configure Claude Code settings
        settings_path = configure_claude_settings(statusline_command, claude_dir)
        
        # Print success message
        print_success_message(target_path, settings_path, statusline_command)
        
    except KeyboardInterrupt:
        print_colored("\n❌ Installation cancelled by user", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()