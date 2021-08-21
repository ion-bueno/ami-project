from loader import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


class Weather(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = self.path + "/weather/GMP/"
        self.keys = ['trend.V06A.GPM_IP.2AKA.HS-SLV-precipRate.precip.0',
                     'trend.V06A.GPM_IP.2AKA.HS-SLV-precipRate.precip.8']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        for key in self.keys:
            # read in only the columns we want to have (usecols[])
            self.dict[key] = pd.read_csv(self.my_path + key + ".csv", delimiter=r"\s+", low_memory=False)
        pass

    def get_summary(self):
        # for all keys
        for key in self.keys:
            # save all data in temporary variable data
            data = self.dict[key]

            print(data)

    def get_data(self):
        return self.dict  