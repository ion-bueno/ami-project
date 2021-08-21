## Setup

1. Download the repository.
2. We highly recommend using a conda environment to avoid installation problems with the GEOS and Proj package.
To create a new conda environment based on python 3.7.7 and to install all required packages run ```conda create --name <your-env-name> python=3.7.7 --file requirements_local.txt -c conda-forge```.
(```-c conda-forge``` is required in order to add the additional required channel)

## Replicate Preprocessing and Visualizations

Our datasets cover in essence five different measurements: 
* International agreements on climate goals (co2goals)
* COVID-19 cases (covid19)
* Greenhouse gas data (greenhouse)
* Mobility data (mobility)
* Weather data (weather)

An interactive visualization can be accessed by running ```index.py```, 
and opening the provided port in the console, e.g. [127.0.0.1:8050](http://127.0.0.1:8050/). More easily, this visualization can be accessed by using the following link https://ami-group1-dashboard.herokuapp.com.

To replicate the preprocessing steps to retrieve the figures used in the report, run ```main.py```, there we call all the loaders that are located in ```/loader```.

You can find the raw datasets in ```/datasets```.
From there, the data gets loaded in a ready to use pandas dataframe. 
Afterwards, a selection of plots demonstrate insights from these datasets. 
These figures can be found in ```/results``` in the respective folders (co2goals, covid19, greenhouse, mobility, weather).

## Replicate Predictions

We have divided our CO2 emissions predictions in two types, with and without corona:
* Without corona: can be found in ```prediction/co2_no_covid```, there you can find some proposed models by some of the group members: in ```model_maxl.py``` we used sarima and in ```RNN_seasonal_co2_prediction.py``` we used recurrent neural networks. Furthermore, by accesing ```/zied``` there you can find co2 emissions predictions for every country using polynomial regression and we also computed correlations between the co2 emissions of every country, which can be found in ```corr.csv```.
* With corona: by accesing ```prediction/co2_covid``` you can find our predictions for every sector (power industry, construction, mobility and other industries).
  * Power industry: all the needed code for the power industry prediction is located in the ```power_industry.py``` file. The code there is divided in the necessary functions and a main that calls these functions. If you want to repeat the process you just have to call the functions that are in the main which are: ```model = Power_Indicators()```, to create the necessary object; ```model.clean_co2()``` and ```model.clean_power_industry()```, to get the data ready; ```model.select_indicator()```; ```model.sarima_model()```, here you really train the model but the model is already saved in ```/results/power_industry``` and finally ```model.vector()``` where we save our results in a csv file.
  * Mobility: all the related functions are in ```mobility.py```. For this sector we didn't need to predict anything because the dataset we are using (provided by apple) already gives us the change rate with respect to the mobility without covid, that it's in the end the data we want.
  * Other industries: the code can be found in ```loader/other_industry_loader.py``. In this case, as our datasets were limited, we couldn't perform an ML model se there you can find the functions used to get our result adjusting the seasonalities.
  * Construction: the code is in the ```construction_industry.py``` file, there you can find the necessary methods to load the data and train model. These methods are called from the main: ```const_load = ConstructionLoader()``` to declare the loader object, ```const_load.load()``` to load the data and const_load.train_and_predict()``` to train and predict the regression model.
  * Sectors combination: we combine all the sectors in ```sectors_combination.py```, that it's basically a main where we collect the results of each sector and combine them in a matrix taking each corresponding weight into account, later it's saved in ```/results/predictions/overall_vector.csv```.

Then, in ```/results```, there is a folder for each sector where we stored the plots and the trained models to save computation time.

## Team

    Bayrakceken, Kudret Aras
    Belkhiria, Zied
    Bueno Ulacia, Ion
    Egger, Maximilian
    Kern, Max-Emanuel
    Krüger, Philipp
    Martín Cruz, Daniel
    Tarasewicz, Damian