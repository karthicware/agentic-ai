class MealOrderModule:
    def __init__(self):
        self.flightList = []
        flight1 = {"mflId": 1, "f": 10, "j": 20, "w": 0, "y": 44}
        flight2 = {"mflId": 2, "f": 2, "j": 20, "w": 0, "y": 55}
        flight3 = {"mflId": 4, "f": 12, "j": 20, "w": 0, "y": 66}
        self.flightList.append(flight1)
        self.flightList.append(flight2)
        self.flightList.append(flight3)

    def get_meal_order_details(self, mflId: int):
        #check mflId is exist
        if not mflId:
            return "Please provide mflId"
        
        #return meal order details based on mflId fetched from the flightList
        for flight in self.flightList:
            if flight["mflId"] == mflId:
                return flight
        return "Meal order details not found"