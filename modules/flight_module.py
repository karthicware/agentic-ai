class FlightModule:
    def __init__(self):
        self.flightList = []
        flight1 = {"flightNo": "EK0202", "flightDate": "21-Jun-2025", "mflId": 1, "registration_number": "A6-ABC", "serviceType": "J", "flightStatus": "PD"}
        flight2 = {"flightNo": "EK0203", "flightDate": "20-Jun-2025", "mflId": 2, "registration_number": "A6-DEF", "serviceType": "P", "flightStatus": "PD"}
        flight3 = {"flightNo": "EK0500", "flightDate": "23-Jun-2025", "mflId": 4, "registration_number": "A6-GHI", "serviceType": "J", "flightStatus": "FO"}
        flight4 = {"flightNo": "EK0600", "flightDate": "23-Jun-2025", "mflId": 5, "registration_number": "A6-JKL", "serviceType": "J", "flightStatus": "FO"}
        self.flightList.append(flight1)
        self.flightList.append(flight2)
        self.flightList.append(flight3)
        self.flightList.append(flight4)

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