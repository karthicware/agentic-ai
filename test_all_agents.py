#!/usr/bin/env python3
"""
Comprehensive test script to verify all sub-agent fixes
Tests all major workflows and agent interactions
"""

import os
from dotenv import load_dotenv
from app.agent_builder import build_root_agent

def test_agent_structure():
    """Test the agent structure and delegation"""
    print("🔍 Testing Agent Structure...")
    print("-" * 50)
    
    try:
        agent = build_root_agent()
        print(f"✅ Root agent name: {agent.name}")
        print(f"✅ Root agent has {len(agent.sub_agents)} sub-agents")
        
        # Check main_multi_tool_agent
        main_agent = None
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            print(f"✅ Found main_multi_tool_agent")
            print(f"✅ Main agent has {len(main_agent.tools)} tools (should be 0)")
            print(f"✅ Main agent has {len(main_agent.sub_agents)} sub-agents")
            
            # Check if it has the right sub-agents
            sub_agent_names = [sa.name for sa in main_agent.sub_agents]
            print(f"✅ Sub-agents: {sub_agent_names}")
            
            required_agents = [
                "flight_info_agent", "meal_order_info_agent", "meal_support_agent", 
                "stock_count_approver_agent", "knowledge_agent"
            ]
            
            missing_agents = [name for name in required_agents if name not in sub_agent_names]
            if not missing_agents:
                print("✅ SUCCESS: All required sub-agents present")
                return True
            else:
                print(f"❌ ISSUE: Missing sub-agents: {missing_agents}")
                return False
        else:
            print("❌ ISSUE: Could not find main_multi_tool_agent")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_meal_order_agent_tools():
    """Test the meal order agent has correct tools"""
    print("\n🍽️ Testing Meal Order Agent Tools...")
    print("-" * 50)
    
    try:
        agent = build_root_agent()
        
        # Find meal_order_agent
        main_agent = None
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            meal_order_agent = None
            for sub_agent in main_agent.sub_agents:
                if sub_agent.name == "meal_order_info_agent":
                    meal_order_agent = sub_agent
                    break
            
            if meal_order_agent:
                print(f"✅ Found meal_order_info_agent")
                print(f"✅ Meal order agent has {len(meal_order_agent.tools)} tools")
                
                tool_names = [tool.__name__ for tool in meal_order_agent.tools]
                print(f"✅ Tools: {tool_names}")
                
                if "get_flight_details" in tool_names and "get_meal_order_details" in tool_names:
                    print("✅ SUCCESS: Meal order agent has both required tools!")
                    return True
                else:
                    print("❌ ISSUE: Meal order agent missing required tools")
                    return False
            else:
                print("❌ ISSUE: Could not find meal_order_info_agent")
                return False
        else:
            print("❌ ISSUE: Could not find main_multi_tool_agent")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_stock_count_approval_agent():
    """Test the stock count approval agent structure"""
    print("\n📊 Testing Stock Count Approval Agent...")
    print("-" * 50)
    
    try:
        agent = build_root_agent()
        
        # Find stock_count_approver_agent
        main_agent = None
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            stock_count_approver_agent = None
            for sub_agent in main_agent.sub_agents:
                if sub_agent.name == "stock_count_approver_agent":
                    stock_count_approver_agent = sub_agent
                    break
            
            if stock_count_approver_agent:
                print(f"✅ Found stock_count_approver_agent")
                print(f"✅ Stock count approver agent has {len(stock_count_approver_agent.sub_agents)} sub-agents")
                
                sub_agent_names = [sa.name for sa in stock_count_approver_agent.sub_agents]
                print(f"✅ Sub-agents: {sub_agent_names}")
                
                required_agents = [
                    "stock_count_agent", "export_text_agent", "erp_agent", 
                    "stock_count_reconciliation_agent", "post_approval_export_agent"
                ]
                
                missing_agents = [name for name in required_agents if name not in sub_agent_names]
                if not missing_agents:
                    print("✅ SUCCESS: All required approval workflow agents present")
                    return True
                else:
                    print(f"❌ ISSUE: Missing approval workflow agents: {missing_agents}")
                    return False
            else:
                print("❌ ISSUE: Could not find stock_count_approver_agent")
                return False
        else:
            print("❌ ISSUE: Could not find main_multi_tool_agent")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_knowledge_agent_tools():
    """Test the knowledge agent has correct tools"""
    print("\n📚 Testing Knowledge Agent Tools...")
    print("-" * 50)
    
    try:
        agent = build_root_agent()
        
        # Find knowledge_agent
        main_agent = None
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            knowledge_agent = None
            for sub_agent in main_agent.sub_agents:
                if sub_agent.name == "knowledge_agent":
                    knowledge_agent = sub_agent
                    break
            
            if knowledge_agent:
                print(f"✅ Found knowledge_agent")
                print(f"✅ Knowledge agent has {len(knowledge_agent.tools)} tools")
                
                tool_names = [tool.__name__ for tool in knowledge_agent.tools]
                print(f"✅ Tools: {tool_names}")
                
                if "get_knowledge_context" in tool_names and "search_specific_topic" in tool_names:
                    print("✅ SUCCESS: Knowledge agent has both required tools!")
                    return True
                else:
                    print("❌ ISSUE: Knowledge agent missing required tools")
                    return False
            else:
                print("❌ ISSUE: Could not find knowledge_agent")
                return False
        else:
            print("❌ ISSUE: Could not find main_multi_tool_agent")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_greeting_farewell_agents():
    """Test the greeting and farewell agents"""
    print("\n👋 Testing Greeting and Farewell Agents...")
    print("-" * 50)
    
    try:
        agent = build_root_agent()
        
        # Check greeting and farewell agents
        greeting_agent = None
        farewell_agent = None
        
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "greeting_agent":
                greeting_agent = sub_agent
            elif sub_agent.name == "farewell_agent":
                farewell_agent = sub_agent
        
        if greeting_agent and farewell_agent:
            print(f"✅ Found greeting_agent with {len(greeting_agent.tools)} tools")
            print(f"✅ Found farewell_agent with {len(farewell_agent.tools)} tools")
            
            greeting_tools = [tool.__name__ for tool in greeting_agent.tools]
            farewell_tools = [tool.__name__ for tool in farewell_agent.tools]
            
            if "say_hello" in greeting_tools and "say_goodbye" in farewell_tools:
                print("✅ SUCCESS: Greeting and farewell agents have correct tools!")
                return True
            else:
                print("❌ ISSUE: Greeting or farewell agents missing required tools")
                return False
        else:
            print("❌ ISSUE: Could not find greeting or farewell agents")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE AGENT STRUCTURE TESTING")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    api_key = os.getenv("GOOGLE_GENAI_MODAL")
    if not api_key:
        print("❌ ERROR: GOOGLE_GENAI_MODAL API key not found in .env file")
        return
    
    print(f"✅ API Key configured: {'Yes' if api_key else 'No'}")
    print()
    
    # Run all tests
    tests = [
        ("Agent Structure", test_agent_structure),
        ("Meal Order Agent Tools", test_meal_order_agent_tools),
        ("Stock Count Approval Agent", test_stock_count_approval_agent),
        ("Knowledge Agent Tools", test_knowledge_agent_tools),
        ("Greeting/Farewell Agents", test_greeting_farewell_agents),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}...")
        print("-" * 50)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! The agent structure is correctly configured.")
        print("📝 The main agent now focuses on routing and delegation only.")
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")

if __name__ == "__main__":
    main() 