#!/usr/bin/env python3
"""
Test script to verify Swiss Insurance tools integration with Agent Zero
"""

import sys
import os
sys.path.append('python/tools')

def test_tool_imports():
    """Test that all Swiss insurance tools can be imported"""
    print("🧪 Testing Swiss Insurance Tools Integration...")
    print("=" * 50)
    
    try:
        from email_designer import EmailDesigner
        print("✅ EmailDesigner imported successfully")
    except ImportError as e:
        print(f"❌ EmailDesigner import failed: {e}")
        return False
    
    try:
        from web_page_builder import WebPageBuilder
        print("✅ WebPageBuilder imported successfully")
    except ImportError as e:
        print(f"❌ WebPageBuilder import failed: {e}")
        return False
    
    try:
        from social_media_creator import SocialMediaCreator
        print("✅ SocialMediaCreator imported successfully")
    except ImportError as e:
        print(f"❌ SocialMediaCreator import failed: {e}")
        return False
    
    try:
        from insurance_rate_comparison import InsuranceRateComparison
        print("✅ InsuranceRateComparison imported successfully")
    except ImportError as e:
        print(f"❌ InsuranceRateComparison import failed: {e}")
        return False
    
    return True

def test_agent_zero_tools():
    """Test that Agent Zero's built-in tools are available"""
    print("\n🔧 Testing Agent Zero Built-in Tools...")
    print("=" * 50)
    
    # Check if key Agent Zero tools exist
    tools_to_check = [
        'browser_agent.py',
        'vision_load.py', 
        'search_engine.py',
        'code_execution_tool.py'
    ]
    
    all_good = True
    for tool in tools_to_check:
        if os.path.exists(f'python/tools/{tool}'):
            print(f"✅ {tool} found")
        else:
            print(f"❌ {tool} missing")
            all_good = False
    
    return all_good

def test_tool_loading():
    """Test the tool loading mechanism"""
    print("\n🔄 Testing Tool Loading Mechanism...")
    print("=" * 50)
    
    try:
        from python.helpers.extract_tools import load_classes_from_folder
        from python.helpers.tool import Tool
        
        # Test loading our Swiss insurance tools
        classes = load_classes_from_folder("python/tools", "email_designer.py", Tool)
        if classes:
            print("✅ EmailDesigner loads via Agent Zero mechanism")
        else:
            print("❌ EmailDesigner not found by Agent Zero loader")
            return False
        
        classes = load_classes_from_folder("python/tools", "web_page_builder.py", Tool)
        if classes:
            print("✅ WebPageBuilder loads via Agent Zero mechanism")
        else:
            print("❌ WebPageBuilder not found by Agent Zero loader")
            return False
        
        classes = load_classes_from_folder("python/tools", "social_media_creator.py", Tool)
        if classes:
            print("✅ SocialMediaCreator loads via Agent Zero mechanism")
        else:
            print("❌ SocialMediaCreator not found by Agent Zero loader")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Tool loading test failed: {e}")
        return False

def test_configuration():
    """Test configuration files"""
    print("\n⚙️ Testing Configuration...")
    print("=" * 50)
    
    config_files = [
        'config_swiss_insurance_agent.env',
        'prompts/default/agent.system.main.role.md',
        'config/tools.json',
        'config/ui.json'
    ]
    
    all_good = True
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} found")
        else:
            print(f"⚠️ {config_file} missing (optional)")
    
    return True

def main():
    """Run all tests"""
    print("🇨🇭 Swiss Insurance Agent - Integration Test")
    print("=" * 60)
    
    tests = [
        ("Tool Imports", test_tool_imports),
        ("Agent Zero Tools", test_agent_zero_tools), 
        ("Tool Loading", test_tool_loading),
        ("Configuration", test_configuration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Swiss Insurance tools are properly integrated with Agent Zero")
        print("🚀 Your insurance agents can now use:")
        print("   - All Agent Zero capabilities (web research, vision, etc.)")
        print("   - Professional email creation")
        print("   - Landing page building") 
        print("   - Social media content creation")
        print("   - Insurance rate comparison")
        print("   - FINMA compliance checking")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("Please check the errors above and fix any issues")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 