import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import sys
import os

plt.style.use('fivethirtyeight')
result_path = '../../results/sarima_co2/'

if '../..' in sys.path:
    pass
else:
    sys.path.insert(0, '../..')

from loader.greenhouse_loader import GreenhouseLoader

# decomment these parts in case of unexpected import problems
def load_co2_data():
    ghg_loader = GreenhouseLoader()
    cur_dir = os.getcwd()
    os.chdir('../../')
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    os.chdir(cur_dir)
    return df_ghg


    
data = load_co2_data()
ghg_monthly = data['gg_global_monthly']
#print(ghg_monthly)
y = ghg_monthly.loc[:, 'co2 average (micro/mol)']
y.index = pd.to_datetime(y.index) # adjust type of index to datetime

plt.figure(1)
y.plot(figsize=(15, 6))
plt.show()
plt.gcf().savefig(result_path + 'allCO2data' +".pdf", bbox_inches='tight')

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]


warnings.filterwarnings("ignore") # specify to ignore warning messages

aics = []
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()
            aics.append([param, param_seasonal, results.aic])
            # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue
        
        

aics = np.array(aics)
optimal_params_index = np.argmin(aics[:,2])
optimal_params = aics[optimal_params_index,:]
print('ARIMA{}x{}12 - AIC:{}'.format(optimal_params[0], optimal_params[1], optimal_params[2]))            



mod = sm.tsa.statespace.SARIMAX(y,
                                order=optimal_params[0],
                                seasonal_order=optimal_params[1],
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

print(results.summary().tables[1])

results.plot_diagnostics(figsize=(15, 12))
plt.show()
plt.gcf().savefig(result_path + 'sarima_diagnostics' +".pdf", bbox_inches='tight')
pred_dynamic = results.get_prediction(start=pd.to_datetime('2020-01-01'), dynamic=True, full_results=True)
pred_dynamic_ci = pred_dynamic.conf_int()


plt.figure(3)
ax = y['2015':].plot(label='observed', figsize=(20, 15))
pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

ax.fill_between(pred_dynamic_ci.index,
                pred_dynamic_ci.iloc[:, 0],
                pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2020-01-01'), y.index[-1],
                 alpha=.1, zorder=-1)

ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')

plt.legend()
plt.show()
plt.gcf().savefig(result_path + 'dyn_pred_validation' +".pdf", bbox_inches='tight')


# %%

# Extract the predicted and true values of our time series
y_forecasted = pred_dynamic.predicted_mean
y_truth = y['2020':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

# %%

# Get forecast 12 steps ahead in future
pred_uc = results.get_forecast(steps=12)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()


plt.figure(4)
ax = y["2015":].plot(label='observed', figsize=(20, 15))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')

plt.legend()
plt.show()
plt.gcf().savefig(result_path + 'dyn_pred_forecast' +".pdf", bbox_inches='tight')

# %%

