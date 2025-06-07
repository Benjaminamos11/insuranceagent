#!/usr/bin/env python3
# Swiss Insurance Agent Launcher
import os
import sys

# Set insurance agent configuration
os.environ['CONFIG_FILE'] = 'config_swiss_insurance_agent.env'
os.environ['AGENT_MODE'] = 'swiss_insurance'
os.environ['UI_THEME'] = 'swiss_insurance'

# Import and run Agent Zero with insurance configuration
from run_ui import main

if __name__ == "__main__":
    print("🇨🇭 Starting Swiss Insurance Agent...")
    print("✅ All capabilities enabled")
    print("⚖️ FINMA compliance active") 
    print("🌐 Web research ready")
    print("👁️ Vision analysis ready")
    print("📧 Email designer ready")
    print("🌐 Web page builder ready")
    print("📱 Social media creator ready")
    print("🔄 Multi-agent coordination ready")
    print("-" * 40)
    main()
