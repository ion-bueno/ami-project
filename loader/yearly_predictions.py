from loader import *
import pandas as pd

class Predictions(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = self.path + "../prediction/co2_no_covid/zied/"
        self.keys = ['predictions',
                     'EU_predictions']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        for key in self.keys:
            # read in only the columns we want to have (usecols[])
            self.dict[key] = pd.read_csv(self.my_path + key + ".csv")
        pass

    def get_summary(self):
        # for all keys
        for key in self.keys:
            # save all data in temporary variable data
            data = self.dict[key]
            print(data)

    def get_data(self):
        return self.dict
    def demo(self, country):
        if country == "EU":
            data = pd.read_csv("../prediction/co2_no_covid/zied/predictions" + ".csv")
            co2_df = data
            ax = co2_df.iloc[2][1:].plot()
            return ax
        else:
            data = pd.read_csv(self.my_path + "predictions" + ".csv")
            co2_df = data
            countries = ["United States", "India", "China", "Japan", "Canada", "Brazil"]
            if country in countries:
                for i in range (len(data)):
                    if co2_df.iloc[i][0] == country:
                        ax = co2_df.iloc[i][1:].plot()
            return ax
            else:
                print('error: this country is not in the list')

