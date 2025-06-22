class MealOrderModule:
    def __init__(self):
        self.flightList = []
        flight1 = {"mflId": 1, "f": 8, "j": 15, "w": 0, "y": 40}  # EK0202 21-Jun-2025
        flight2 = {"mflId": 6, "f": 2, "j": 20, "w": 0, "y": 55}  # EK0203 20-Jun-2025
        flight3 = {"mflId": 4, "f": 12, "j": 20, "w": 0, "y": 66}  # EK0500 23-Jun-2025
        flight4 = {"mflId": 5, "f": 6, "j": 18, "w": 0, "y": 50}   # EK0600 23-Jun-2025
        self.flightList.append(flight1)
        self.flightList.append(flight2)
        self.flightList.append(flight3)
        self.flightList.append(flight4)

    def get_meal_order_details(self, mflId: int):
        # Check if mflId is provided
        if not mflId:
            return {
                "status": "error",
                "message": "Please provide a valid meal order ID (mflId).",
                "data": None,
                "total_items": 0
            }
        
        # Return meal order details based on mflId fetched from the flightList
        for flight in self.flightList:
            if flight["mflId"] == mflId:
                # Convert to structured format
                meal_orders = [
                    {"meal_type": "First Class", "quantity": flight["f"], "special_requests": "None", "status": "Confirmed"},
                    {"meal_type": "Business Class", "quantity": flight["j"], "special_requests": "None", "status": "Confirmed"},
                    {"meal_type": "Premium Economy", "quantity": flight["w"], "special_requests": "None", "status": "Confirmed"},
                    {"meal_type": "Economy Class", "quantity": flight["y"], "special_requests": "None", "status": "Confirmed"}
                ]
                
                return {
                    "status": "success",
                    "message": f"Meal order details found for mflId {mflId}",
                    "data": meal_orders,
                    "total_items": len(meal_orders)
                }
        
        # Enhanced error message with more context
        return {
            "status": "error",
            "message": f"No meal order data available for flight with mflId {mflId}.",
            "data": None,
            "total_items": 0
        }