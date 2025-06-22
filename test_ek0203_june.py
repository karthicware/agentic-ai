#!/usr/bin/env python3
"""
Test for flight EK0203 20-Jun-2025 meal order
"""

from modules.flight_module import FlightModule
from modules.meal_order_module import MealOrderModule

def test_ek0203_june_meal_order():
    """Test meal order for flight EK0203 on 20-Jun-2025"""
    print("🧪 Testing EK0203 20-Jun-2025 Meal Order")
    print("=" * 50)
    
    # Test flight details
    flight_module = FlightModule()
    flight_result = flight_module.get_flight_details("EK0203", "20-Jun-2025")
    
    print(f"✈️ Flight details: {flight_result}")
    
    if isinstance(flight_result, dict) and "mflId" in flight_result:
        mflId = flight_result["mflId"]
        print(f"✅ mflId: {mflId}")
        
        # Test meal order details
        meal_module = MealOrderModule()
        meal_result = meal_module.get_meal_order_details(mflId)
        
        print(f"🍽️ Meal order result: {meal_result}")
        
        if meal_result["status"] == "success":
            print("✅ SUCCESS: Meal orders found!")
            print(f"📊 Data: {meal_result['data']}")
            return True
        else:
            print(f"❌ ISSUE: {meal_result['message']}")
            return False
    else:
        print(f"❌ ISSUE: Flight not found - {flight_result}")
        return False

if __name__ == "__main__":
    test_ek0203_june_meal_order() 