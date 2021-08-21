import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
import itertools
import statsmodels.api as sm
import warnings
import os
import sys


# add path
if '../..' in sys.path:
    pass
else:
    sys.path.insert(0, '../..')

from loader.greenhouse_loader import GreenhouseLoader


def load_co2_data():
    ghg_loader = GreenhouseLoader()
    cur_dir = os.getcwd()
    os.chdir('../../')
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    os.chdir(cur_dir)
    return df_ghg


def get_demo(country_to_show):
    possible_countries = ["Brazil", "Canada", "EU", "India", "Japan", "Russia", "United States", "China"]
    fig, ax = plt.subplots(figsize=(6, 4))
    early_year = ["January", "February", "March", "April", "May", "June"]
    change_rates = pd.read_csv('../../results/predictions/overall_vector.csv')
    change_rates_country = change_rates[country_to_show].dropna()
    if country_to_show in possible_countries:
        ax.plot(early_year[0:change_rates_country.shape[0]], change_rates_country, label=country_to_show)
        ax.legend()
        plt.ylabel("Change Rate of CO2 Emissions")
        plt.xlabel("Months in Early 2020")
    else:
        print("Emission data for this country is not available")
        return
    return ax


if __name__ == "__main__":
    countries = ['EU', 'United States', 'India', 'China', 'Japan', 'Russia', 'Canada', 'Brazil']
    sectors = ['Power industry', 'Buildings', 'Transport', 'Other industrial combustion', 'Other sectors']
    construction_pred_emissions = pd.read_csv('../../results/buildings/emission_predictions.csv', header=0, index_col=[0])
    construction_pred_emissions.index = countries
    construction_pred_emissions = construction_pred_emissions.T

    power_industry_pred_vector = pd.read_csv('../../results/power_industry/predicted_vector.csv', index_col=[0])
    power_industry_pred_vector = power_industry_pred_vector.iloc[1:]
    power_industry_pred_vector.index = construction_pred_emissions.index

    mobility_pred_vector = pd.read_csv('../../results/mobility/predicted_vector.csv', index_col=[0])
    mobility_pred_vector = mobility_pred_vector.rename(columns={'European Union': 'EU'})
    mobility_pred_vector.index = construction_pred_emissions.index

    other_industries_pred_vector = pd.read_csv('../../results/other_industries/predicted_vector.csv', index_col=[0])
    other_industries_pred_vector = other_industries_pred_vector.rename(columns={'European Union': 'EU'})
    other_industries_pred_vector.index = construction_pred_emissions.index

    other_sectors_pred_vector = pd.DataFrame(1, columns=countries, index=construction_pred_emissions.index)


    # Normalization of constructions
    for country in construction_pred_emissions.columns:
        construction_pred_emissions[country] = construction_pred_emissions[country] / construction_pred_emissions[country][0]
    construction_pred_vector = construction_pred_emissions


    ghg_dict = load_co2_data()
    co2_country_sector = ghg_dict['co2_country_sector']
    co2_country = ghg_dict['co2_country'][countries].loc['2018']

    co2_power_industry = co2_country_sector['Power Industry'][countries].loc['2018']
    co2_buildings = co2_country_sector['Buildings'][countries].loc['2018']
    co2_transport = co2_country_sector['Transport'][countries].loc['2018']
    co2_other_industries = co2_country_sector['Other industrial combustion'][countries].loc['2018']
    co2_other_sectors = co2_country_sector['Other sectors'][countries].loc['2018']


    # Weight of each sector to overall emissions
    percentages = pd.DataFrame(columns = countries, index = sectors)
    for country in countries:
        percentages[country]['Power industry'] = co2_power_industry[country] / co2_country[country]
        percentages[country]['Buildings'] = co2_buildings[country] / co2_country[country]
        percentages[country]['Transport'] = co2_transport[country] / co2_country[country]
        percentages[country]['Other industrial combustion'] = co2_other_industries[country] / co2_country[country]
        percentages[country]['Other sectors'] = co2_other_sectors[country] / co2_country[country]

    percentages.to_csv('sectors_weights.csv')

    change_rate = pd.DataFrame(columns = countries, index = construction_pred_vector.index)
    for country in countries:
        change_rate[country] = percentages[country]['Power industry'] * power_industry_pred_vector[country] + percentages[country]['Buildings'] * construction_pred_vector[country] + percentages[country]['Transport'] * mobility_pred_vector[country] + percentages[country]['Other industrial combustion'] * other_industries_pred_vector[country] + percentages[country]['Other sectors'] * other_sectors_pred_vector[country]

    print(change_rate)

    change_rate.to_csv('../../results/predictions/overall_vector.csv')


