from loader.loader import *
import pandas as pd
import pickle


class GermanyCovidLoader(Loader):

    def __init__(self):
        super().__init__()
        self.covid_data: pd.DataFrame
        self.geo_data: pd.DataFrame
        self.covid_geo_data: pd.DataFrame

    def load(self):
        # read number of cases in germany
        self.covid_data = pd.read_csv(
            self.path + '/Covid19/covid_germany.csv', converters={'AGS': lambda x: str(x)})

        # read the preprocessed geo data
        self.geo_data = pd.read_csv(
            self.path + '/Covid19/germany_geo_data.csv', converters={'AGS': lambda x: str(x)})

        # merge covid_data with coordinates
        self.covid_geo_data = pd.merge(
            self.covid_data, self.geo_data, on='AGS')

        # filter important data TODO: change later
        self.covid_geo_data = self.covid_geo_data[['AGS', 'death_rate', 'cases', 'deaths', 'cases_per_100k',
                                                   'cases_per_population', 'county', 'last_update', 'recovered', 'longitude', 'latitude']]

    def get_summary(self):
        # TODO
        pass

    def get_data(self):
        return self.covid_geo_data
