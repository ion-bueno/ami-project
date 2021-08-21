import sys

if '../..' in sys.path:
    pass
else:
    sys.path.insert(0, '../..')

from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
import keras.models
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.metrics import mean_squared_error
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import math


def load_co2_data():
    ghg_loader = GreenhouseLoader()
    cur_dir = os.getcwd()
    os.chdir('../../')
    ghg_loader.load()
    df_ghg = ghg_loader.get_data()
    os.chdir(cur_dir)
    return df_ghg['co2_global_weekly']


def preprocess_data(df):
    len_data = len(df)
    yearly_avg = np.array([df.to_numpy()[i - 26:i + 26].mean() for i in range(26, len_data - 27)])
    #diff = df.to_numpy()[26:len_data - 27].ravel() - yearly_avg
    #dataset = df.values.astype('float32')
    dataset = np.flip(yearly_avg)
    dataset = dataset.reshape(-1, 1)

    scaler = StandardScaler()
    dataset = scaler.fit_transform(dataset)
    return dataset, scaler


def plot_df(df):
    df.plot()
    plt.show()


def split_train_test(dataset, train_ratio):
    train_data_size = int(len(dataset)*train_ratio)
    test_data_size = len(dataset)-train_data_size
    return dataset[0:train_data_size], dataset[train_data_size:len(dataset)]


def dataset_split_into_x_and_y(dataset, nr_look_back, nr_predict=1):
    data_x = []
    data_y = []
    for i in range(len(dataset)-nr_look_back-nr_predict-1):
        data_x.append(dataset[i:(nr_look_back+i)])
        data_y.append(dataset[i+nr_look_back:i+nr_look_back+nr_predict])
    #print(data_x[1], data_y[1])
    data_x = np.reshape(data_x, (len(data_x), 1, nr_look_back))
    data_y = np.reshape(data_y, (len(data_y), 1, nr_predict))
    return np.array(data_x), np.array(data_y)


def create_rnn(nr_look_back):
    rnn = Sequential()
    rnn.add(LSTM(500, input_shape=(1, nr_look_back)))
    rnn.add(Dense(1))
    rnn.compile(loss='mean_squared_error', optimizer='adam')
    return rnn


def create_and_train_model(X_train, y_train, epochs=30, batch_size=16, nr_look_back=10, output_size=1):
    rnn = Sequential()
    rnn.add(LSTM(2000, input_shape=(1, nr_look_back), return_sequences=True))
    rnn.add(Dense(output_size))
    rnn.compile(loss='mean_squared_error', optimizer='adam')
    rnn.summary()
    early_stopping = EarlyStopping(monitor='val_loss', mode='min', patience=10, restore_best_weights=True)
    history = rnn.fit(X_train, y_train, validation_split=0.2, epochs=epochs, batch_size=batch_size,
                      callbacks=[early_stopping])
    fig, ax = plt.subplots()
    plot_model_history(history, ax)
    return rnn


def plot_model_history(history, ax=None, metric='loss', ep_start=1, ep_stop=None,monitor='val_loss', mode='min',plttitle=None):
    if ax is None:
        fig,ax = plt.subplots()
    if ep_stop is None:
        ep_stop = len(history.epoch)
    if plttitle is None:
        plttitle = metric[0].swapcase() + metric[1:] + ' During Training'
    ax.plot(np.arange(ep_start,ep_stop+1, dtype='int'),history.history[metric][ep_start-1:ep_stop])
    ax.plot(np.arange(ep_start,ep_stop+1, dtype='int'),history.history['val_' + metric][ep_start-1:ep_stop])
    ax.set(title=plttitle)
    ax.set(ylabel=metric[0].swapcase() + metric[1:])
    ax.set(xlabel='Epoch')
    ax.legend(['train', 'val'], loc='upper right')
    plt.show()


def generate_predictions(model, nr_samples_to_generate, nr_look_back, latest_data, nr_predict=1):
    predictions = []
    latest_data = latest_data.reshape(-1)
    for i in range(nr_look_back):
        predictions.append(latest_data[-nr_look_back+i])
    for i in range(nr_samples_to_generate):
        x = predictions[-nr_look_back:]
        #print(x)
        x = np.reshape(x, (1, 1, nr_look_back))
        pred = model.predict(x)[0][0]
        predictions.append(pred)
    return predictions[nr_look_back:]


def plot_results(y_train_pred, y_test_pred, future_predictions, true_values):
    plt.plot(range(len(y_train_pred)), y_train_pred, label='Predictions on the training set')
    plt.plot(range(len(y_train_pred) + 1, len(y_train_pred) + len(y_test_pred) + 1), y_test_pred,
             label='Predictions on the testing set')
    plt.plot(range(len(true_values) + 1, len(true_values) + len(future_predictions) + 1),
             future_predictions, label='Future predictions')
    plt.plot(range(len(true_values)), true_values, label='Real values')
    #plt.xticks(list(range(len(true_values))), indices)
    plt.title("CO2 predictions")
    #plt.legend()
    plt.show()


def store_model(model, name='trained_model'):
    model.save(name)


def load_model(name='trained_model'):
    return keras.models.load_model(name)


if __name__ == "__main__":
    df_co2 = load_co2_data()
    indices = df_co2.index
    dataset, scaler = preprocess_data(df_co2)
    print(dataset[-10:])
    train_data, test_data = split_train_test(dataset, 0.7)
    nr_look_back = 5   # 50 was quite good with 500 neurons
    to_predict = 50
    x_train, y_train = dataset_split_into_x_and_y(train_data, nr_look_back, nr_predict=to_predict)
    x_test, y_test = dataset_split_into_x_and_y(test_data, nr_look_back, nr_predict=to_predict)

    rnn = create_and_train_model(x_train, y_train, nr_look_back=nr_look_back, output_size=to_predict, epochs=5)
    store_model(rnn, name='trained_average')
    rnn = load_model('trained_average')
    y_train_pred = rnn.predict(x_train)
    print(y_train_pred[0,0,:])
    y_test_pred = rnn.predict(x_test)
    print(y_test_pred.shape)
    y_train_pred_concat = np.empty(y_train.shape[0])
    y_test_pred_concat = np.empty(y_test.shape[0])
    y_train_pred = y_train_pred[:,0,:]
    y_test_pred = y_test_pred[:,0,:]
    """if to_predict > 1:
        for i in range(y_train_pred.shape[0]-to_predict):
            print(y_train_pred_concat.shape, y_train_pred.shape)
            y_train_pred_concat[i:i+to_predict] += y_train_pred[i,0,:]
            #print(y_train_pred_concat[0:2])
            #y_test_pred_concat[i:i + to_predict, 0] += y_test_pred[i, :, :] / to_predict
            #y_test_pred_concat = y_test_pred[:,:,-1]
        print(y_train_pred_concat[0:2])
        y_train_pred_concat = y_train_pred_concat.reshape(-1, 1)"""
        #y_train_pred = y_train_pred_concat.mean(axis=2)

    """if to_predict > 1:
        for i in range(y_test_pred.shape[0]-to_predict):
            #y_train_pred_concat[i:i+to_predict,0] += y_train_pred[i,:,:]/to_predict
            y_test_pred_concat[i:i + to_predict] += y_test_pred[i, 0, :]
            #y_test_pred_concat = y_test_pred[:,:,-1]
        #y_test_pred = y_test_pred_concat.mean(axis=2)
        y_test_pred_concat = y_test_pred_concat.reshape(-1, 1)"""

    y_train_pred = scaler.inverse_transform(y_train_pred)
    y_test_pred = scaler.inverse_transform(y_test_pred)

    #train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

    predictions = generate_predictions(rnn, 1, nr_look_back, test_data, nr_predict=to_predict)
    #print(predictions[:5])
    predictions = scaler.inverse_transform(np.reshape(predictions, (-1, 1)))

    plot_results(y_train_pred, y_test_pred, predictions, scaler.inverse_transform(dataset))