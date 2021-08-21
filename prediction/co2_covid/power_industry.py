import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
import itertools
import statsmodels.api as sm
import warnings
import os
import sys
import matplotlib.pyplot as plt
import pickle

# add path
if '../..' in sys.path:
    pass
else:
    sys.path.insert(0, '../..')
    

from loader.greenhouse_loader import GreenhouseLoader
from loader.power_industry_loader import PowerLoader

def load_co2_data():
    ghg_loader = GreenhouseLoader()
    cur_dir = os.getcwd()
    os.chdir('../../')
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    os.chdir(cur_dir)
    return df_ghg

def load_power_industry():
    power_loader = PowerLoader()
    cur_dir = os.getcwd()
    os.chdir('../../')
    power_loader.load()
    df_power = power_loader.get_data()
    os.chdir(cur_dir)
    return df_power

def scale(df):
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df))
    df_scaled.index = df.index
    df_scaled.columns = df.columns
    return df_scaled

class Power_Indicators():
    
    def __init__(self):
        self.covid_date = '2019-12-01'
        self.co2_df = pd.DataFrame()
        self.data_country_dict = {}
        self.indicator_country_dict = {}
        self.prediction_country_dict = {}
        self.models_dict = {}
        self.vector_df = pd.DataFrame()
        self.europeCountries = []
        self.country_big8 = ['United States', 'China', 'Russia', 'India', 'Brazil', 'Canada', 'Japan']
    
    def clean_co2(self):
        gg_data = load_co2_data()
        self.co2_df = gg_data['co2_country_sector']['Power Industry']
        self.co2_df.index = pd.to_datetime(self.co2_df.index)
        self.co2_df = self.co2_df.rename(columns={'Spain and Andorra': 'Spain',
                                        'France and Monaco': 'France',
                                        'Italy, San Marino and the Holy See': 'Italy',
                                        'Switzerland and Liechtenstein': 'Switzerland'})
        self.co2_df = self.co2_df.loc['2008':, :]
        self.co2_df = self.co2_df.astype('float64')
        

    def clean_power_industry(self):

        power_data = load_power_industry()

        EU_co2 = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
                            'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
                            'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
                            'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom']


        supply_df = power_data['supply']
        supply_df.name = 'Supply'
        supply_df['EU'] = supply_df.loc[:, EU_co2].sum(axis=1)
        supply_forecast = supply_df[self.covid_date:]
        self.europeCountries = supply_df.columns
        #supply_df = supply_df[:self.covid_date]

        oil_df = power_data['oil']
        oil_df.name = 'Oil'
        oil_forecast = oil_df['2019':'2020-04-01']
        oil_df['EU'] = oil_df.loc[:, EU_co2].sum(axis=1)
        oil_forecast = oil_df[self.covid_date:]
        #oil_df = oil_df[:self.covid_date]

        brent_df = power_data['brent']
        brent_df = brent_df.loc['2008':]
        brent_df = brent_df.rename(columns={'Price': 'Brent price'})
        brent_forecast = brent_df[self.covid_date:]
        #brent_df = brent_df[:self.covid_date]

        gas_df = power_data['natural_gas']
        gas_df = gas_df.loc['2008':]
        gas_df = gas_df.rename(columns={'Price': 'Natural gas price'})
        gas_forecast = gas_df[self.covid_date:]
        #gas_df = gas_df[:self.covid_date]
  
        for country in supply_df.columns:
            data = pd.concat([brent_df, gas_df, supply_df[country].rename('Supply'), oil_df[country].rename('Oil')], axis=1)
            forecast = pd.concat([brent_forecast, gas_forecast, supply_forecast[country].rename('Supply'), oil_forecast[country].rename('Oil')], axis=1)
            self.data_country_dict[country] = {'data': data, 'forecast': forecast}
        for country in self.country_big8:
            data = pd.concat([brent_df, gas_df], axis=1)
            forecast = pd.concat([brent_forecast, gas_forecast], axis=1)
            self.data_country_dict[country] = {'data': data, 'forecast': forecast}
            

    def select_indicator(self, show_best_indicator=False):
        for country in self.europeCountries:
            aux = []
            for i in range(4):
                aux.append(self.data_country_dict[country]['data'].iloc[:, i].corr(self.co2_df[country]))
            string = self.data_country_dict[country]['data'].columns[aux.index(max(aux))]
            if show_best_indicator:
                print(f'{country} -> \t{max(aux)}\t {string}')
            self.indicator_country_dict[country] = {'data': self.data_country_dict[country]['data'].iloc[:, aux.index(max(aux))],
                                                    'forecast': self.data_country_dict[country]['forecast'].iloc[:, aux.index(max(aux))]}
            
        for country in self.country_big8:
            aux = []
            for i in range(2):
                aux.append(self.data_country_dict[country]['data'].iloc[:, i].corr(self.co2_df[country]))
            string = self.data_country_dict[country]['data'].columns[aux.index(max(aux))]
            if show_best_indicator:
                print(f'{country} -> \t{max(aux)}\t {string}')
            self.indicator_country_dict[country] = {'data': self.data_country_dict[country]['data'].iloc[:, aux.index(max(aux))],
                                                    'forecast': self.data_country_dict[country]['forecast'].iloc[:, aux.index(max(aux))]}

        self.country_big8.append('EU')
        
    def get_demo(self, country):
        co2_norm = scale(pd.DataFrame(self.co2_df[country]))
        norm = scale(pd.DataFrame(self.data_country_dict[country]['data']))
        #co2_norm.append(norm)
        for indicator in norm.columns:
            co2_norm[indicator] = norm[indicator]
        plt.figure(figsize=(10,6))
        ax = co2_norm.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Power industry CO2 emissions and indicators in ' + country)
        plt.ylabel('CO2 emissions and indicators')
        plt.xlabel('date')
        return ax

    def sarima_model(self):

        # Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 2)

        # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        # Generate all different combinations of seasonal p, q and q triplets
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        warnings.filterwarnings("ignore") # specify to ignore warning messages

        for country in self.country_big8:
            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    try:
                        mod = sm.tsa.statespace.SARIMAX(self.indicator_country_dict[country]['data'],
                                                        order=param,
                                                        seasonal_order=param_seasonal,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
                        
                        results = mod.fit()
                        self.models_dict[country] = results
                        pred_dynamic = results.get_prediction(start=pd.to_datetime(self.covid_date), dynamic=True, full_results=True).predicted_mean
                        #prediction_dict = {'prediction': pred_dynamic}
                        #prediction_dict.update(self.indicator_country_dict[country]['prediction'])
                        self.prediction_country_dict[country] = pred_dynamic
                    except:
                        print('Error')
                        continue
        pd.DataFrame.from_dict(model.prediction_country_dict).to_csv("power_industry_predictions.csv")
        f = open('../../results/power_industry/estimators.pkl', 'wb')
        pickle.dump(self.models_dict, f)
        f.close()


    def plot_sarima(self, country):
        observed = self.indicator_country_dict[country]['data']['2019':]
        forecast = pd.read_csv('power_industry_predictions.csv', header=0, index_col = 0)
        forecast = forecast[country]
        forecast.index = pd.to_datetime(forecast.index)
        observed = observed.to_frame()
        forecast = forecast.to_frame()
        observed['forecast'] = forecast
        #observed.append(forecast)
        plt.figure(figsize=(10,6))
        ax = observed.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Predicted vs. observed CO2 emissions in ' + country)
        plt.ylabel('CO2 emissions')
        plt.xlabel('date')
        return ax

    def vector(self):
        countries = self.country_big8
        countries.append('EU')

        vector_df = pd.DataFrame(columns=countries, index=self.indicator_country_dict['Spain']['forecast'].index)

        for country in vector_df.columns:
            vector = []
            for month in self.indicator_country_dict[country]['forecast'].index:
                if(self.indicator_country_dict[country]['forecast'][month] is not None):
                    vector.append(self.indicator_country_dict[country]['forecast'][month] / self.prediction_country_dict[country][month])
                else:
                    vector.append(None)
            self.vector_df[country] = vector
        return self.vector_df

    

if __name__=="__main__":
    model = Power_Indicators()
    model.clean_co2()
    model.clean_power_industry()
    model.select_indicator(True)


    model.sarima_model()
    model.vector()

    for country in model.country_big8:
        ax_indicators = model.get_demo(country)
        fig = ax_indicators.get_figure()
        fig.savefig('../../results/power_industry/' + country + '_indicators.pdf', bbox_inches='tight')

        ax_pred = model.plot_sarima(country)
        fig = ax_pred.get_figure()
        fig.savefig('../../results/power_industry/' + country + '_prediction.pdf', bbox_inches='tight')

    model.vector_df.to_csv('../../results/power_industry/predicted_vector.csv')


