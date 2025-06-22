#!/usr/bin/env python3
"""
Simple test to verify meal order agent structure and tools
"""

import os
from dotenv import load_dotenv
from app.agent_builder import build_root_agent

def test_agent_structure():
    """Test the agent structure and tools"""
    
    print("🔍 Testing Agent Structure...")
    print("=" * 50)
    
    try:
        # Build the agent
        print("Building agent...")
        agent = build_root_agent()
        
        # Check agent structure
        print(f"✅ Root agent name: {agent.name}")
        print(f"✅ Root agent has {len(agent.sub_agents)} sub-agents")
        
        # Find main_multi_tool_agent
        main_agent = None
        for sub_agent in agent.sub_agents:
            if sub_agent.name == "main_multi_tool_agent":
                main_agent = sub_agent
                break
        
        if main_agent:
            print(f"✅ Found main_multi_tool_agent")
            print(f"✅ Main agent has {len(main_agent.tools)} tools (should be 0 for sub-agent architecture)")
            print(f"✅ Main agent has {len(main_agent.sub_agents)} sub-agents")
            
            # Find meal_order_agent
            meal_order_agent = None
            for sub_agent in main_agent.sub_agents:
                if sub_agent.name == "meal_order_info_agent":
                    meal_order_agent = sub_agent
                    break
            
            if meal_order_agent:
                print(f"✅ Found meal_order_info_agent")
                print(f"✅ Meal order agent has {len(meal_order_agent.tools)} tools")
                
                # Check if it has the required tools
                tool_names = [tool.__name__ for tool in meal_order_agent.tools]
                print(f"✅ Tools: {tool_names}")
                
                if "get_flight_details" in tool_names and "get_meal_order_details" in tool_names:
                    print("✅ SUCCESS: Meal order agent has both flight and meal order tools!")
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

def test_flight_module():
    """Test the flight module directly"""
    print("\n✈️ Testing Flight Module...")
    print("-" * 50)
    
    try:
        from modules.flight_module import FlightModule
        
        flight_module = FlightModule()
        result = flight_module.get_flight_details("EK0203", "20-Jan-2024")
        
        print(f"✅ Flight details retrieved: {result}")
        
        if isinstance(result, dict) and "mflId" in result:
            mflId = result["mflId"]
            print(f"✅ mflId extracted: {mflId}")
            return mflId
        else:
            print("❌ ISSUE: Flight details not in expected format")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def test_meal_order_module():
    """Test the meal order module directly"""
    print("\n🍽️ Testing Meal Order Module...")
    print("-" * 50)
    
    try:
        from modules.meal_order_module import MealOrderModule
        
        meal_module = MealOrderModule()
        result = meal_module.get_meal_order_details(2)  # mflId for EK0203
        
        print(f"✅ Meal order details retrieved: {result}")
        
        if isinstance(result, dict) and "status" in result:
            print(f"✅ Status: {result['status']}")
            if result['status'] == 'success':
                print(f"✅ Data: {result['data']}")
                return True
            else:
                print(f"❌ ISSUE: {result['message']}")
                return False
        else:
            print("❌ ISSUE: Meal order details not in expected format")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 SIMPLE MEAL ORDER TESTING")
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
    
    # Run tests
    agent_ok = test_agent_structure()
    mflId = test_flight_module()
    meal_ok = test_meal_order_module()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"Agent Structure: {'✅ PASS' if agent_ok else '❌ FAIL'}")
    print(f"Flight Module: {'✅ PASS' if mflId else '❌ FAIL'}")
    print(f"Meal Order Module: {'✅ PASS' if meal_ok else '❌ FAIL'}")
    
    if agent_ok and mflId and meal_ok:
        print("\n🎉 ALL TESTS PASSED! The meal order flow should work correctly.")
        print(f"📝 Expected flow: Flight EK0203 (mflId: {mflId}) → Meal orders retrieved successfully")
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")

if __name__ == "__main__":
    main() 