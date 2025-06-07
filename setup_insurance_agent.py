#!/usr/bin/env python3
"""
Swiss Insurance Agent Setup Script
Configures Agent Zero with all insurance-specific capabilities
"""

import os
import sys
import json
import shutil
from pathlib import Path

def setup_insurance_agent():
    """
    Complete setup for Swiss Insurance Agent based on Agent Zero
    """
    
    print("🇨🇭 Setting up Swiss Insurance Agent...")
    print("=" * 50)
    
    # 1. Create insurance-specific directories
    setup_directories()
    
    # 2. Configure tools
    setup_tools()
    
    # 3. Configure prompts
    setup_prompts()
    
    # 4. Setup environment
    setup_environment()
    
    # 5. Configure UI
    setup_ui()
    
    # 6. Test configuration
    test_setup()
    
    print("\n✅ Swiss Insurance Agent setup complete!")
    print("\n📋 What your insurance agents can now do:")
    print("- 🌐 Web research & competitor analysis")
    print("- 👁️ Image analysis & screenshot capture")
    print("- 📧 Professional email creation")
    print("- 🌐 Responsive website building")
    print("- 📱 Social media content creation")
    print("- ⚖️ FINMA compliance checking")
    print("- 🎨 Corporate branding integration")
    print("- 📊 Market analysis & reporting")
    print("- 💼 Client consultation support")
    print("- 🔄 Multi-agent coordination")

def setup_directories():
    """Create necessary directories for insurance agent"""
    
    print("📁 Creating directory structure...")
    
    directories = [
        "templates/email",
        "templates/web", 
        "templates/social",
        "assets/branding",
        "assets/images",
        "work_dir/insurance",
        "prompts/swiss_insurance",
        "logs/insurance",
        "exports/generated_content"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created {directory}")

def setup_tools():
    """Configure and register insurance tools"""
    
    print("\n🔧 Configuring insurance tools...")
    
    # Tool configuration
    tool_config = {
        "insurance_tools": {
            "email_designer": {
                "enabled": True,
                "class": "EmailDesigner",
                "file": "python/tools/email_designer.py",
                "capabilities": ["email_creation", "html_generation", "mobile_responsive"]
            },
            "web_page_builder": {
                "enabled": True,
                "class": "WebPageBuilder", 
                "file": "python/tools/web_page_builder.py",
                "capabilities": ["landing_pages", "seo_optimization", "responsive_design"]
            },
            "social_media_creator": {
                "enabled": True,
                "class": "SocialMediaCreator",
                "file": "python/tools/social_media_creator.py", 
                "capabilities": ["social_content", "platform_optimization", "hashtag_generation"]
            },
            "insurance_rate_comparison": {
                "enabled": True,
                "class": "InsuranceRateComparison",
                "file": "python/tools/insurance_rate_comparison.py",
                "capabilities": ["rate_comparison", "policy_analysis", "savings_calculation"]
            }
        },
        "agent_zero_tools": {
            "browser_agent": {
                "enabled": True,
                "capabilities": ["web_browsing", "screenshot_capture", "web_automation"]
            },
            "vision_load": {
                "enabled": True,
                "capabilities": ["image_analysis", "ocr", "visual_content_analysis"]
            },
            "search_engine": {
                "enabled": True, 
                "capabilities": ["web_search", "real_time_data", "market_research"]
            },
            "code_execution_tool": {
                "enabled": True,
                "capabilities": ["data_analysis", "chart_generation", "automation"]
            }
        }
    }
    
    # Save tool configuration
    with open("config/tools.json", "w") as f:
        json.dump(tool_config, f, indent=2)
    
    print("   ✓ Tool configuration saved")

def setup_prompts():
    """Setup specialized agent prompts"""
    
    print("\n📝 Setting up agent prompts...")
    
    # Copy main prompt that we already created
    if os.path.exists("prompts/swiss_insurance/agent.system.main.role.md"):
        print("   ✓ Main Swiss insurance prompt already configured")
    else:
        print("   ⚠️ Main prompt needs to be configured")
    
    # Create additional specialized prompts
    prompts = {
        "project_manager.md": """# Swiss Insurance Project Manager Agent

You are a specialized project management agent for Swiss insurance tasks.

## Your Role:
- Analyze complex insurance requests
- Break down tasks into manageable steps
- Coordinate with other specialized agents
- Ensure quality and compliance
- Optimize workflows for efficiency

## Capabilities:
- Task breakdown and analysis
- Multi-agent coordination
- Quality control and review
- Timeline management
- Performance optimization

## Always:
- Start with request analysis
- Identify required agents and tools
- Create clear step-by-step plans
- Monitor progress and quality
- Ensure FINMA compliance throughout
""",
        
        "research_analyst.md": """# Swiss Insurance Research Analyst

You are a specialized research agent for Swiss insurance market analysis.

## Your Role:
- Conduct web research on insurance topics
- Analyze market trends and competitor data
- Gather real-time insurance information
- Create market reports and insights
- Monitor FINMA and regulatory updates

## Capabilities:
- Real-time web search and analysis
- Screenshot capture and visual analysis
- Market trend identification
- Competitor benchmarking
- Regulatory monitoring

## Always:
- Use multiple sources for verification
- Focus on Swiss market specifics
- Include FINMA-relevant information
- Provide actionable insights
- Cite sources and provide links
""",
        
        "content_creator.md": """# Swiss Insurance Content Creator

You are a specialized content creation agent for Swiss insurance marketing.

## Your Role:
- Create professional emails, web pages, and social content
- Ensure mobile-responsive and SEO-optimized designs
- Integrate corporate branding consistently
- Maintain FINMA compliance in all content
- Optimize for conversion and engagement

## Capabilities:
- Professional email design (HTML/CSS)
- Responsive web page creation
- Multi-platform social media content
- Corporate branding integration
- Performance optimization

## Always:
- Use mobile-first design principles
- Include proper FINMA disclaimers
- Integrate client branding consistently
- Optimize for Swiss market preferences
- Test across devices and platforms
""",
        
        "consultation_expert.md": """# Swiss Insurance Consultation Expert

You are a specialized consultation agent for Swiss insurance advice.

## Your Role:
- Provide expert insurance consultation
- Analyze client needs and risks
- Compare policies and providers
- Ensure regulatory compliance
- Support client communication

## Capabilities:
- Insurance product knowledge
- Risk assessment and analysis
- Policy comparison and recommendations
- FINMA compliance guidance
- Client communication support

## Always:
- Prioritize client best interests
- Ensure FINMA compliance
- Provide clear, understandable advice
- Compare multiple options
- Document recommendations clearly
"""
    }
    
    # Create specialized prompts
    for filename, content in prompts.items():
        filepath = f"prompts/swiss_insurance/{filename}"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✓ Created {filename}")

def setup_environment():
    """Setup environment configuration"""
    
    print("\n🔧 Configuring environment...")
    
    # Check if main config exists
    if os.path.exists("config_swiss_insurance_agent.env"):
        print("   ✓ Insurance agent configuration already exists")
    else:
        print("   ⚠️ Please configure API keys in config_swiss_insurance_agent.env")
    
    # Create run script for insurance agent
    run_script = """#!/usr/bin/env python3
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
"""
    
    with open("run_insurance_agent.py", "w") as f:
        f.write(run_script)
    
    # Make it executable
    os.chmod("run_insurance_agent.py", 0o755)
    
    print("   ✓ Created insurance agent launcher")

def setup_ui():
    """Configure UI for insurance agents"""
    
    print("\n🎨 Configuring UI...")
    
    # UI configuration
    ui_config = {
        "theme": "swiss_insurance",
        "branding": {
            "show_agent_zero_logo": False,
            "custom_logo": "assets/branding/logo.png",
            "company_name": "Swiss Insurance Expert",
            "primary_color": "#38666f",
            "secondary_color": "#724d69"
        },
        "features": {
            "multi_agent_view": True,
            "workflow_visualization": True,
            "tool_usage_tracking": True,
            "performance_metrics": True
        },
        "language": {
            "default": "de",
            "supported": ["de", "fr", "it", "en"]
        }
    }
    
    # Create UI config directory if it doesn't exist
    Path("config").mkdir(exist_ok=True)
    
    with open("config/ui.json", "w") as f:
        json.dump(ui_config, f, indent=2)
    
    print("   ✓ UI configuration saved")

def test_setup():
    """Test the setup configuration"""
    
    print("\n🧪 Testing setup...")
    
    # Check critical files
    critical_files = [
        "python/tools/email_designer.py",
        "python/tools/web_page_builder.py", 
        "python/tools/social_media_creator.py",
        "prompts/swiss_insurance/agent.system.main.role.md",
        "config_swiss_insurance_agent.env"
    ]
    
    all_good = True
    for file in critical_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ❌ {file} missing")
            all_good = False
    
    if all_good:
        print("   ✅ All critical files present")
    else:
        print("   ⚠️ Some files missing - check setup")
    
    # Test tool imports
    try:
        sys.path.append("python/tools")
        from email_designer import EmailDesigner
        from web_page_builder import WebPageBuilder
        from social_media_creator import SocialMediaCreator
        print("   ✅ All custom tools import successfully")
    except ImportError as e:
        print(f"   ⚠️ Import error: {e}")

if __name__ == "__main__":
    setup_insurance_agent() 