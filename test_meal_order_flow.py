#!/usr/bin/env python3
"""
Test script to verify meal order flow
This script tests the complete flow from flight info to meal orders
"""

import os
from dotenv import load_dotenv
from app.agent_builder import build_root_agent

def test_meal_order_flow():
    """Test the complete meal order flow"""
    
    # Load environment variables
    load_dotenv()
    
    print("🔍 Testing Meal Order Flow...")
    print("=" * 50)
    
    try:
        # Build the agent
        print("Building agent...")
        agent = build_root_agent()
        
        # Test meal order query
        test_query = "What is the meal order for the flight EK0203 20-Jan-2024"
        print(f"\n📝 Test Query: {test_query}")
        print("-" * 50)
        
        # Get response
        response = agent.run(test_query)
        print(f"\n✅ Response:")
        print(response)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_meal_order_flow()
    
    if success:
        print("\n🎉 Meal order flow test completed successfully!")
    else:
        print("\n❌ Meal order flow test failed!") 