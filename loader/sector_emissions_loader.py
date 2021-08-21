from loader.greenhouse_loader import GreenhouseLoader
import pandas as pd
import matplotlib.pyplot as plt


def load_co2_data():
    ghg_loader = GreenhouseLoader()
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    return df_ghg


def co2_demo(sector):
    gg_data = load_co2_data()
    countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]
    co2_df = gg_data['co2_country_sector'][sector]
    co2_df.index = pd.to_datetime(co2_df.index)
    co2_df = co2_df.loc['2004':, :][countries]
    plt.figure(figsize=(10,6))
    ax = co2_df.plot(kind='line', x_compat=True)
    plt.xticks(rotation=60)
    if sector == "Buildings":
        plt.title("CO2 emissions due to construction industry")
    elif sector == "Transport":
        plt.title("CO2 emissions due to transport industry")
    else:
        plt.title("CO2 emissions due to {}".format(sector.lower()))
    plt.ylabel("CO2 emissions in Mtons")
    return ax
