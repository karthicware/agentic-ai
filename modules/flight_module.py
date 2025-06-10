class FlightModule:
    def __init__(self):
        self.flightList = []
        flight1 = {"flightNo": "EK0202", "flightDate": "21-Jan-2024", "mflId": 1, "registration_number": "A6-ABC"}
        flight2 = {"flightNo": "EK0203", "flightDate": "20-Jan-2024", "mflId": 2, "registration_number": "A6-DEF"}
        flight3 = {"flightNo": "EK0500", "flightDate": "22-Mar-2025", "mflId": 4, "registration_number": "A6-GHI"}
        self.flightList.append(flight1)
        self.flightList.append(flight2)
        self.flightList.append(flight3)

    def get_flight_details(self, flightNo: str, flightDate: str):
        #check flightNo is exist and flightDate is no exist
        if not flightNo:
            return "Please provide flightNo"
        
        #return flight details based on flightNo and flightDate fetched from the flightList
        for flight in self.flightList:
            if not flightDate:
                if flight["flightNo"] == flightNo:
                    return flight
            elif flight["flightNo"] == flightNo and flight["flightDate"] == flightDate:
                return flight
        return "Flight details not found"