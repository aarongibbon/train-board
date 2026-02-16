import requests
import json

class TrainApi():

    def __init__(self, apiToken):
        self.api_url = "https://api1.raildata.org.uk/1010-live-arrival-and-departure-boards-arr-and-dep1_1/LDBWS/api/20220120/GetArrDepBoardWithDetails/"
        self.headers = {"x-apikey": apiToken}
        self.headers["User-Agent"] = "curl/8.5.0"


    def getStationArrivalsDepartures(self, station):
        response = requests.get(self.api_url+station, headers=self.headers)
        return response.json()
