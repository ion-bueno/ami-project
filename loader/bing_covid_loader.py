from loader.loader import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
from cartopy import crs as ccrs


class BingCovidLoader(Loader):
    def __init__(self):
        super().__init__()
        self.data: pd.DataFrame

    def load(self, online: bool = False):
        self.data = pd.read_csv(
            'https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv' if online else self.path + 'Covid19/bing_covid.csv')

        #relevant columns
        self.data = self.data.drop_duplicates(
            subset=['ISO2', 'ISO3', 'Country_Region', 'AdminRegion1', 'AdminRegion2'], keep='last')

        #only countries
        self.data = self.data.drop_duplicates(
            subset=['ISO3'], keep='first').iloc[1:]

        population_df = pd.read_csv(self.path + 'Covid19/pop.csv')[['ISO3', 'Population']]
        self.data = pd.merge(self.data, population_df, on='ISO3')

        self.data['death rate'] = self.data['Deaths'].astype('float') * 100000 / self.data['Population'].astype('float')
        self.data['case rate'] = self.data['Confirmed'].astype('float') * 100000 / self.data['Population'].astype('float')
        self.data['recovered rate'] = self.data['Recovered'].astype('float') * 100000 / self.data['Population'].astype('float')
        self.data['case increase rate'] = self.data['ConfirmedChange'].astype('float') * 100000 / self.data['Population'].astype('float')
        self.data['death increase rate'] = self.data['DeathsChange'].astype('float') * 100000 / self.data['Population'].astype('float')
        self.data['recovered increase rate'] = self.data['RecoveredChange'].astype('float') * 100000 / self.data['Population'].astype('float')

    def get_summary(self):
        pass
        #self.save_all_figures()
    
    def draw_world_map(self, data_to_draw: str = 'cases') -> plt.Figure:
        if data_to_draw not in ['cases', 'case rate', 'case change', 'deaths', 'death rate', 'death change', 'recovered', 'recovered rate', 'recovered change']:
            raise ValueError(
                'Unexpected value for data_to_draw: ' + str(data_to_draw))

        drawn_series = pd.Series(
            [0]*len(self.data['ISO3']), index=self.data['ISO3'])
        cmap = mpl.cm.cool

        # TODO add cases for rates (meaning per 100k people)
        # TODO change per capita instead of absolute change might make more sense
        # TODO some countries data are not up-to-date, change statistics belong to the last reported day
        if data_to_draw == 'cases':
            drawn_series = self.data.set_index('ISO3')['Confirmed']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'case rate':
            drawn_series = self.data.set_index('ISO3')['case rate']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'case change':
            drawn_series = self.data.set_index('ISO3')['ConfirmedChange']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'deaths':
            drawn_series = self.data.set_index('ISO3')['Deaths']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'death rate':
            drawn_series = self.data.set_index('ISO3')['death rate']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'death change':
            drawn_series = self.data.set_index('ISO3')['DeathsChange']
            cmap = mpl.cm.Reds
        elif data_to_draw == 'recovered':
            drawn_series = self.data.set_index('ISO3')['Recovered']
            cmap = mpl.cm.Blues
        elif data_to_draw == 'recovered rate':
            drawn_series = self.data.set_index('ISO3')['recovered rate']
            cmap = mpl.cm.Blues
        elif data_to_draw == 'recovered change':
            drawn_series = self.data.set_index('ISO3')['RecoveredChange']
            cmap = mpl.cm.Blues

        norm = mpl.colors.Normalize(
            vmin=drawn_series.min(), vmax=drawn_series.max())

        iso3_colors = drawn_series.map(lambda x: cmap(norm(x)))

        shapename = 'admin_0_countries'
        countries_shp = shpreader.natural_earth(resolution='110m',
                                                category='cultural', name=shapename)

        fig = plt.figure(figsize=(13,13))
        ax = plt.axes(projection=ccrs.PlateCarree())
        fig.add_axes(ax)
        ax.coastlines()
        label = {
            'cases': 'Number of cases',
            'case rate': 'Number of cases per 100k people',
            'case change': 'Number of new cases in the last day',
            'deaths': 'Number of deaths',
            'death rate': 'Number of deaths per 100k people',
            'death change': 'Number of deaths in the last day',
            'recovered': 'Number of recovered people',
            'recovered rate': 'Number of recovered people per 100k people',
            'recovered change': 'Number of recoveries in the last day'
        }[data_to_draw]

        fig.colorbar(mpl.cm.ScalarMappable(
            norm=norm, cmap=cmap), label=label, orientation='horizontal')

        for country in shpreader.Reader(countries_shp).records():
            try:
                ax.add_geometries([country.geometry], ccrs.PlateCarree(),
                                  facecolor=iso3_colors[country.attributes['ISO_A3']],
                                  label=country.attributes['NAME_LONG'])
            except:
                pass
        return fig

    def save_all_figures(self):
        
        for data in ['cases', 'case rate', 'case change', 'deaths', 'death rate', 'death change', 'recovered', 'recovered rate', 'recovered change']:
            self.draw_world_map(data).savefig('results/covid/' + data + '.png', bbox_inches='tight') 
            

    def get_data(self):
        return self.data
