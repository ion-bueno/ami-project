from abc import ABC, abstractmethod
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from loader.loader import *

class OtherIndustryLoader(Loader):
    def __init__(self):
        super().__init__()
        self.data: pd.DataFrame

    def load(self):
        self.us_data = pd.read_csv(self.path + "other_industry/steel_USA.csv", sep =";", low_memory=False, thousands='.', decimal=",")
        self.us_data['DATE'] = pd.to_datetime(self.us_data['DATE'])

        self.ww_data = pd.read_csv(self.path + "other_industry/steel_all_countries.csv", sep =";", low_memory=False, usecols = ["Date", "United States", "Brazil", "India", "Japan", "EU", "World", "Russia", "Canada", "China"], thousands='.', decimal=",")
        self.ww_data['Date'] = pd.to_datetime(self.ww_data['Date'], format="%Y%m")


        dfUS = self.us_data
        yearly_means = np.array([dfUS['Steel production'].to_numpy()[x-6:x+6].mean() for x in range(6, len(dfUS)-6)]) / dfUS['Steel production'][6:-6].to_numpy()
        yearly_means = yearly_means[:len(yearly_means) - (len(yearly_means)%12)]
        seasonality = [x.mean() for x in yearly_means.reshape((12, -1), order='F')]
        starting_month = self.us_data['DATE'][6].month
        jan_index = (1 - starting_month) % 12
        self.seasonality = seasonality[jan_index:] + seasonality[:jan_index]
        self.adjust_seasonality(self.seasonality, self.us_data)
        self.adjust_seasonality(self.seasonality, self.ww_data)

    def adjust_seasonality(self, seasonality, data):
        start_index = data.iloc[:,0][0].month - 1
        s = seasonality[start_index:] + seasonality[:start_index]
        s = np.array(((len(data) // 12 + 1) * s)[:len(data)])
        for col in data.columns[1:]:
            data[col] = data[col].to_numpy() * s

    def get_data(self):
        return (self.ww_data, self.us_data)

    def us_ax(self):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(self.us_data['DATE'], self.us_data["Steel production"]/np.mean(self.us_data["Steel production"]))
        plt.ylabel("Seasonally Adjusted Steel Production of the US Normalized by Mean")
        plt.xlabel("Year")
        return ax

    def ww_ax(self):
        countries = self.ww_data.columns[1:-1].to_numpy()

        fig, ax = plt.subplots(figsize=(6, 4))
        diff = dict()
        perc = dict()
        for country in countries:
            #fig, ax = plt.subplots(figsize=(10, 10))
            ax.plot(self.ww_data['Date'].dt.strftime('%m') + "-" + self.ww_data['Date'].dt.strftime('%y'), self.ww_data[country]/np.max( self.ww_data[country]), label = country)

        plt.ylabel("Seasonally Adjusted Steel \nProduction Normalized by Maximum")
        plt.xlabel("Month - Year")
        plt.setp(ax.get_xticklabels()[1::2], visible=False)
        ax.legend()

        return ax

    def get_summary(self):
        pass

    def ww_demo(self):
        return self.ww_data, self.ww_ax()

    def us_demo(self):
        return self.us_data, self.us_ax()