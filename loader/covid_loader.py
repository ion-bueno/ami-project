from loader.loader import Loader
import pandas as pd
import seaborn as sns


class CovidLoader(Loader):

    def __init__(self):
        super().__init__()
        self.startdate = '2020-02-01'
        self.enddate = '2020-06-10'
        self.country = 'germany'
        self.my_path = "covid/"

    def load(self):
        self.data = self.getcountrycoviddata(self.country, self.startdate, self.enddate)
        pass

    def get_summary(self):
        germany = self.getcountrycoviddata('germany', self.startdate, self.enddate)
        tunisia = self.getcountrycoviddata('tunisia', self.startdate, self.enddate)
        afghanistan = self.getcountrycoviddata('afghanistan', self.startdate, self.enddate)
        italy = self.getcountrycoviddata('italy', self.startdate, self.enddate)
        spain = self.getcountrycoviddata('spain', self.startdate, self.enddate)
        china = self.getcountrycoviddata('china', self.startdate, self.enddate)
        data = pd.concat([germany, tunisia, afghanistan, italy, spain], axis=0, join='inner')

        # data = data.drop(columns=['Country', 'Date', 'City', 'Province', 'CityCode'])
        sns_plot = sns.pairplot(data, hue='CountryCode', palette='rainbow')
        sns_plot.savefig(self.result_path+self.my_path+"pairplot.png")
        pass

    def get_data(self):
        return self.data

    def getcountrycoviddata(self, country, startdate, enddate):
        import requests
        import json
        response = requests.get(
            "https://api.covid19api.com/country/" + country + "?from=" + startdate + "T00:00:00Z&to=" + enddate + "T00:00:00Z")
        # Print the status code of the response.
        data = json.loads(response.content)
        pd_data = pd.read_json(response.content)
        pd_data = pd_data.drop(columns=['Lat', 'Lon', 'City', 'CityCode'])
        return pd_data

    def getcountry_withoutprovinces_coviddata(self, country, startdate, enddate):
        import requests
        import json
        response = requests.get(
            "https://api.covid19api.com/country/" + country + "?from=" + startdate + "T00:00:00Z&to=" + enddate + "T00:00:00Z")
        # Print the status code of the response.
        data = json.loads(response.content)
        pd_data = pd.read_json(response.content)
        pd_data = pd_data.drop(columns=['Lat', 'Lon', 'City', 'CityCode'])
        pd_data = pd_data.loc[pd_data['Province'] == '']
        return pd_data

    def getworldcoviddata(self, startdate, enddate):
        import requests
        import json
        response = requests.get(
            "https://api.covid19api.com/world?from=" + startdate + "T00:00:00Z&to=" + enddate + "T00:00:00Z")
        # Print the status code of the response.
        data = json.loads(response.content)
        pd_data = pd.read_json(response.content)
        return pd_data

    def getallcoviddata(self):  # this function takes time because it download 10MB of data
        import requests
        import json
        response = requests.get("https://api.covid19api.com/all")
        # Print the status code of the response.
        data = json.loads(response.content)
        pd_data = pd.read_json(response.content)
        pd_data = pd_data.drop(columns=['Lat', 'Lon', 'City', 'CityCode'])
        return pd_data