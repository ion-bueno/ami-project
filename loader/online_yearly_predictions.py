import pandas as pd
import os
from matplotlib.pyplot import plot
import numpy as np
import math
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from operator import truediv
from scipy.stats import pearsonr

def predict(y,level):
    x = np.linspace(0, 49, num=49)
    x2 = np.linspace(0, 51, num=51)
    poly = PolynomialFeatures(level, include_bias=False)
    poly.fit_transform(x[:, None])
    poly_model = make_pipeline(PolynomialFeatures(level),
                               LinearRegression())
    poly_model.fit(x[:, np.newaxis], y)
    y_predicted = poly_model.predict(x2[:, np.newaxis])
    return y_predicted

def predict_from_country(y_predicted,y,x,level):
    poly = PolynomialFeatures(level, include_bias=False)
    poly.fit_transform(x[:, None])
    poly_model = make_pipeline(PolynomialFeatures(level),
                               LinearRegression())
    poly_model.fit(x[:, np.newaxis], y)
    return poly_model.predict(y_predicted[:, np.newaxis])

def distortion(y,y_predicted):
    mean = np.mean(y)
    max_value = max(y)
    error = sum(pow(y_predicted[:49]-y, 2))
    return (error/mean)/(math.log10(max_value))

    def predictresults(data, countrytopredict):
        df_CO2 = data

        best_predictions =['Australia', 'Bangladesch', 'Burkina Faso', 'Central Africa Republic', 'Egypt', 'Finland', 'Iceland', 'India', 'Indonesia', 'Malaysia',
                       'Mauritus', 'Morocco', 'Philippines', 'Qatar', 'Sweden', 'Turkey', 'United Arab Emirates', 'Vietnam', 'Greece', 'North Korea', 'Netherlands']
        data_co2 =[None] * 213
        y_predicted =[None] * 213
        x = np.linspace(0, 49, num=49)
        x2 = np.linspace(0, 51, num=51)
        for i in range (np.size(df_CO2['country_name'])):
            data_co2[i] = df_CO2.loc[df_CO2['country_name'] == df_CO2['country_name'][i]]

        for i in range (np.size(df_CO2['country_name'])-3):
            y = (data_co2[i].iloc[0][1:].str.replace(',', '.', regex=True).astype(float))
            name = (data_co2[i].iloc[0][0])
            predicted = predict(y,9)
            error = distortion(y, predicted)
            y_predicted[i] = np.append(np.append(name, predicted), error)

            co2_country = data
        for i in range (np.shape(co2_country)[0]):
            co2_country.iloc[i][2:] = (co2_country.iloc[i][2:].str.replace(',', '.', regex=True).astype(float))

        list =[[],[]]
        to_predict = {}
        for i in range (np.size(co2_country['country_name'])):
            if i != 210:
                if data_co2[i].iloc[0][0] in best_predictions:
                    y = (co2_country.iloc[i][2:])
                    for ii in range (i, np.size(co2_country['country_name'])):
                        if ii != 210:
                            if (i != ii):
                                yy = (co2_country.iloc[ii][2:])
                                list[0].append(co2_country.iloc[i][0]+' '+co2_country.iloc[ii][0])
                                cov = np.cov([y.astype(float),yy.astype(float)])[0][1]
                                corr = pearsonr(y.astype(float),yy.astype(float))[0]
                                list[1].append(cov)
                                if (abs(corr) > 0.9):
                                    if ((co2_country.iloc[ii][0] in best_predictions) == False):
                                        if co2_country.iloc[ii][0] in to_predict.keys():
                                            to_predict[co2_country.iloc[ii][0]] = to_predict[co2_country.iloc[ii][0]] + [co2_country.iloc[i][0]]
                                        else:
                                            to_predict[co2_country.iloc[ii][0]] = [co2_country.iloc[i][0]]
        df_CO2 = data
        if countrytopredict == 'India':
            data = df_CO2.loc[df_CO2['country_name'] == countrytopredict]
            data.iloc[0][1] = data.iloc[0][1].replace(',', '.')
            yy = (data.iloc[0][1:])
            mean = predict(yy,9)
            mean
            ax = plt.plot(mean)
            return ax
        else:
            for country in to_predict:
                if (country == countrytopredict):
                    result = np.zeros((20,51))
                    data = df_CO2.loc[df_CO2['country_name'] == country]
                    y = (data.iloc[0][1:])
                    y[0] = y[0].replace(',', '.')
                    maxvalue = np.zeros((51))
                    minvalue = np.zeros((51))
                    mean = np.zeros((51))
                    fig = plt.figure(figsize=(27, 12))
                    for ii in range(len(to_predict[country])):
                        data = df_CO2.loc[df_CO2['country_name'] == to_predict[country][ii]]
                        data.iloc[0][1] = data.iloc[0][1].replace(',', '.')
                        yy = (data.iloc[0][1:])
                        yy_predicted = predict(yy,9)
                        result[ii] = predict_from_country(yy_predicted, np.array(y), np.array(yy), 1)
                    for i in range (51):
                        maxvalue[i] = np.max(result[:ii+1,i])
                        minvalue[i] = np.min(result[:ii+1,i])
                        mean[i] = np.mean(result[:ii+1,i])
                    ax = plt.plot(mean)
                    return ax


path = "/Users/ziedbk/Desktop/group01/datasets"
df_CO2 = pd.read_csv(path+'/greenhouse/co2_country_edgar.csv')

predictresults(df_CO2, 'Brazil')
