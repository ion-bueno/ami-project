import matplotlib.pyplot as plt
import os, sys
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import pickle
from sklearn import svm
from matplotlib.dates import DateFormatter
from sklearn import svm
from sklearn import model_selection
from matplotlib.dates import DateFormatter

# add path
if '../..' in sys.path:
    pass
else:
    sys.path.insert(0, '../..')

from loader.loader import *
from loader.greenhouse_loader import GreenhouseLoader

def load_co2_data():
    ghg_loader = GreenhouseLoader()
    cur_dir = os.getcwd()
    os.chdir("../..")
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    os.chdir(cur_dir)
    return df_ghg


def scale_and_split(df, is_co2=False):
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df))
    df_scaled.index = df.index
    df_scaled.columns = df.columns
    df_yearly_train = df_scaled.groupby(df_scaled.index.year).mean()
    df_yearly_train = df_yearly_train.loc['2004':'2018', :]
    yearly_train = df_yearly_train.values.reshape(-1, 1)

    if not is_co2:
        df_monthly_pred = df_scaled.loc['2004':'2020', :]
        monthly_pred = df_monthly_pred.values.reshape(-1, 1)
        return [yearly_train, monthly_pred, df_scaled]
    else:
        return [yearly_train.ravel(), scaler]


def get_emissions_per_country(country):
    gg_data = load_co2_data()
    co2_df = gg_data['co2_country_sector']['Buildings']
    co2_df.index = pd.to_datetime(co2_df.index)
    co2_df = co2_df.loc['2004':, :]
    co2_df = co2_df[country]
    # co2_sum = co2_sum.drop(['year'])
    co2_df.columns = ['CO2 Construction Sector']
    # co2_df.plot()
    co2_df.values.ravel()
    # plt.show()
    co2_df.iloc[-5:]
    return co2_df


class ConstructionLoader(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = "construction_industry/"
        self.keys = ['concrete_price', 'steel_iron_price', 'employment_rates', 'de-building-permits',
                     'de-construction-industry', 'de-new-orders-main-construction-industry',
                     'de-persons-employed', 'production_cement_concrete', 'total_construction_spending']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        for key in self.keys:
            self.dict[key] = pd.read_csv("../../"+self.path+self.my_path+key+".csv", low_memory=False)
        pass

    def get_summary(self):
        pass

    def get_data(self):
        return self.dict

    def load_construction_industry(self):
        self.load()
        df_construction = self.get_data()
        return df_construction

    def co2_demo_buildings(self):
        gg_data = load_co2_data()
        countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]
        co2_df = gg_data['co2_country_sector']['Buildings']
        co2_df.index = pd.to_datetime(co2_df.index)
        co2_df = co2_df.loc['2004':, :][countries]
        ax = co2_df.plot()
        plt.xticks(rotation=60)
        plt.title("CO2 emissions due to building sector")
        plt.ylabel("CO2 emissions in Mtons")
        return ax, co2_df

    def indicator_demo(self, indicator_name="steel_price"):
        df_const = self.load_construction_industry()
        if indicator_name == "steel_price":
            df_steel = df_const['steel_iron_price']
            df_steel.index = pd.to_datetime(df_steel['DATE'])
            df_steel = df_steel.loc['2004':, :]
            df_steel = df_steel.drop(['DATE'], axis=1)
            df_steel.columns = ['Steel price']
            ax = df_steel.plot(x_compat=True)
            plt.title("Steel price")
            plt.xticks(rotation=60)
            return ax, df_steel

        elif indicator_name == "concrete_price":
            df_concrete = df_const['concrete_price']
            df_concrete.index = pd.to_datetime(df_concrete['DATE'])
            df_concrete = df_concrete.loc['2004':, :]
            df_concrete = df_concrete.drop(['DATE'], axis=1)
            df_concrete.columns = ['Concrete price']
            ax = df_concrete.plot(x_compat=True)
            plt.title("Concrete price")
            plt.xticks(rotation=60)
            return ax, df_concrete

        elif indicator_name == "concrete_prod":
            df_prod_c = df_const['production_cement_concrete']
            df_prod_c.index = pd.to_datetime(df_prod_c['DATE'])
            df_prod_c = df_prod_c.drop(['DATE'], axis=1)
            df_prod_c.columns = ['Production concrete cement']
            ax = df_prod_c.plot(x_compat=True)
            plt.xticks(rotation=60)
            plt.title("Production cement and concrete")
            return ax, df_prod_c

        elif indicator_name == "const_spend":
            df_spend = df_const['total_construction_spending']
            df_spend.index = pd.to_datetime(df_spend['DATE'])
            df_spend = df_spend.drop(['DATE'], axis=1)
            df_spend.columns = ['Total construction spending']
            ax = df_spend.plot(x_compat=True)
            plt.xticks(rotation=60)
            plt.title("Total construction spending")
            return ax, df_spend

        else:
            return -1

    def prediction_demo(self, country):
        df_const = self.load_construction_industry()
        df_concrete = df_const['concrete_price']
        df_concrete.index = pd.to_datetime(df_concrete['DATE'])
        df_concrete = df_concrete.loc['2004':, :]
        df_concrete = df_concrete.drop(['DATE'], axis=1)
        df_concrete.columns = ['Concrete price']

        df_steel = df_const['steel_iron_price']
        df_steel.index = pd.to_datetime(df_steel['DATE'])
        df_steel = df_steel.loc['2004':, :]
        df_steel = df_steel.drop(['DATE'], axis=1)
        df_steel.columns = ['Steel price']

        df_spend = df_const['total_construction_spending']
        df_spend.index = pd.to_datetime(df_spend['DATE'])
        df_spend = df_spend.drop(['DATE'], axis=1)
        df_spend.columns = ['Total construction spending']

        df_prod_c = df_const['production_cement_concrete']
        df_prod_c.index = pd.to_datetime(df_prod_c['DATE'])
        df_prod_c = df_prod_c.drop(['DATE'], axis=1)
        df_prod_c.columns = ['Production concrete cement']

        f = open("../../results/buildings/estimators.pkl", "rb")
        estimates = pickle.load(f)
        f.close()

        f = open("../../results/buildings/scalers.pkl", "rb")
        scalers = pickle.load(f)
        f.close()

        indicators = dict()
        steel_train, steel_pred, steel_df = scale_and_split(df_steel)
        concrete_train, concrete_pred, concrete_df = scale_and_split(df_concrete)
        prod_train, prod_pred, prod_df = scale_and_split(df_prod_c)
        spend_train, spend_pred, spend_df = scale_and_split(df_spend)

        indicators["generic"] = dict()
        indicators["generic"]["pred"] = np.hstack((steel_pred, concrete_pred, prod_pred, spend_pred))

        plt.figure()
        features_pred = indicators["generic"]["pred"]
        df_co2 = get_emissions_per_country(country)
        co2_train, scaler = scale_and_split(pd.DataFrame(df_co2), is_co2=True)
        best_est = estimates[country]
        pred = best_est.predict(features_pred)
        plt.title(country)
        plt.plot(steel_df.index, scalers[country].inverse_transform(pred), label='predicted emissions')
        plt.plot(df_co2.index, scalers[country].inverse_transform(co2_train), label='observed emissions')
        plt.legend()
        date_form = DateFormatter("%Y-%m")
        plt.gca().xaxis.set_major_formatter(date_form)
        plt.gca().set_ylabel("Emissions in Mton")
        plt.xticks(rotation=60)
        plt.xlabel("date")
        return plt.gca()


    def train_and_predict(self):
        const_load = ConstructionLoader()
        df_const = const_load.load_construction_industry()
        df_concrete = df_const['concrete_price']
        df_concrete.index = pd.to_datetime(df_concrete['DATE'])
        df_concrete = df_concrete.loc['2004':, :]
        df_concrete = df_concrete.drop(['DATE'], axis=1)
        df_concrete.columns = ['Concrete price']

        df_steel = df_const['steel_iron_price']
        df_steel.index = pd.to_datetime(df_steel['DATE'])
        df_steel = df_steel.loc['2004':, :]
        df_steel = df_steel.drop(['DATE'], axis=1)
        df_steel.columns = ['Steel price']

        df_spend = df_const['total_construction_spending']
        df_spend.index = pd.to_datetime(df_spend['DATE'])
        df_spend = df_spend.drop(['DATE'], axis=1)
        df_spend.columns = ['Total construction spending']

        df_prod_c = df_const['production_cement_concrete']
        df_prod_c.index = pd.to_datetime(df_prod_c['DATE'])
        df_prod_c = df_prod_c.drop(['DATE'], axis=1)
        df_prod_c.columns = ['Production concrete cement']
        # X_train, X_test, y_train, y_test = model_selection.train_test_split(features, co2_, test_size=0.33, random_state=42, shuffle=True)
        # , 'epsilon': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10],'gamma': [0.001, 0.005, 0.1, 1]
        indicators = dict()
        steel_train, steel_pred, steel_df = scale_and_split(df_steel)
        concrete_train, concrete_pred, concrete_df = scale_and_split(df_concrete)
        prod_train, prod_pred, prod_df = scale_and_split(df_prod_c)
        spend_train, spend_pred, spend_df = scale_and_split(df_spend)

        indicators["generic"] = dict()
        indicators["generic"]["train"] = np.hstack((steel_train, concrete_train, prod_train, spend_train))
        indicators["generic"]["pred"] = np.hstack((steel_pred, concrete_pred, prod_pred, spend_pred))
        indicators["Germany"] = None
        indicators["United States"] = None
        indicators["India"] = None
        indicators["China"] = None
        indicators["EU"] = None
        indicators["Brazil"] = None
        indicators["Russia"] = None
        indicators["Japan"] = None
        indicators["Canada"] = None

        estimators = dict()
        scalers = dict()

        results = pd.DataFrame(np.zeros((8, 6)))
        results.columns = steel_df.index[-6:]

        regr = svm.SVR()
        parameters = {'kernel': ['rbf', 'poly'], 'C': [10, 100, 1000, 10000], 'gamma': [
            'auto']}  # , 'epsilon':[1e-7, 1e-6, 1e-5]}#, 'gamma':[0.001, 0.1, 1, 10], 'epsilon':[0.1, 1]}
        grid_search = model_selection.GridSearchCV(regr, parameters, verbose=1, scoring='neg_root_mean_squared_error',
                                                   cv=15)

        countries = ["EU", "United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]
        # countries = ["Canada", "EU"]
        fig, axs = plt.subplots(len(countries), figsize=(10, 5 * len(countries)))
        for idx, country in enumerate(countries):
            if indicators[country]:
                features_train = np.hstack((indicators["generic"]["train"], indicators[country]))
                features_pred = np.hstack((indicators["generic"]["pred"], indicators[country]))
            else:
                features_train = indicators["generic"]["train"]
                features_pred = indicators["generic"]["pred"]
            df_co2 = get_emissions_per_country(country)
            co2_train, scaler = scale_and_split(pd.DataFrame(df_co2), is_co2=True)
            grid_search.fit(features_train, co2_train)
            best_est = grid_search.best_estimator_
            estimators[country] = best_est
            scalers[country] = scaler
            print(country)
            print(grid_search.best_params_)
            print(grid_search.best_score_)
            pred = best_est.predict(features_pred)
            axs[idx].title.set_text(country)
            axs[idx].plot(steel_df.index, scaler.inverse_transform(pred), label='predicted emissions')
            axs[idx].plot(df_co2.index, scaler.inverse_transform(co2_train), label='observed emissions')
            axs[idx].legend()
            date_form = DateFormatter("%Y-%m")
            axs[idx].xaxis.set_major_formatter(date_form)
            axs[idx].set_ylabel("Emissions in Mton")
            extent = axs[idx].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            country_camel_case = country.lower().replace(" ", "_")
            fig.savefig('../../results/buildings/{}.pdf'.format(country_camel_case), bbox_inches=extent.expanded(1.1, 1.2))
            results.loc[idx] = scaler.inverse_transform(pred)[-6:]
            results.rename(index={idx: country_camel_case}, inplace=True)
        plt.figure(figsize=(10, 5 * len(countries)))
        plt.tight_layout()
        plt.show()
        results.to_csv('../../results/buildings/emission_predictions.csv')

        f = open("../../results/buildings/estimators.pkl", "wb")
        pickle.dump(estimators, f)
        f.close()

        f = open("../../results/buildings/scalers.pkl", "wb")
        pickle.dump(scalers, f)
        f.close()

if __name__ == "__main__":
    const_load = ConstructionLoader()
    const_load.load()
    const_load.train_and_predict()