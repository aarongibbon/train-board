from zeep import Client
from zeep import xsd

class TrainApi():

    def __init__(self, apiToken):
        api_url = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01"
        header_template = xsd.Element(
                '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
                xsd.ComplexType([
                    xsd.Element(
                        '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
                        xsd.String()),
                ])
        )
        self.client = Client(api_url)
        self.soapHeaders = header_template(TokenValue=apiToken)

    def getStationArrivalsDepartures(self, station):
        return self.client.service.GetArrDepBoardWithDetails(numRows=10, crs=station, timeWindow=120, _soapheaders=[self.soapHeaders])['trainServices']
