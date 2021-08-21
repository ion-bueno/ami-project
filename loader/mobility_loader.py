from loader.loader import *
import matplotlib.pyplot as plt


class MobilityLoader(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = "mobility/"
        self.keys = ['apple', 'google', 'opensky_flight_hours', 'flightradar']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        for key in self.keys:
            self.dict[key] = pd.read_csv(self.path+self.my_path+key+".csv", low_memory=False)
        pass

    def get_summary(self):
        #todo: nice key summary
        self.write_html(self.result_path + self.my_path, "mobility_summary", self.dict['apple'])
        axes = [self.apple_demo(transportation_type="transit")[0], self.google_demo()[0], self.opensky_demo()[0], self.flightradar_demo()[0]]
        names = ["apple_demo", "google_demo", "opensky_demo", "flightradar_demo"]
        for name, ax in zip(names, axes):
            self.save_figure(ax, self.result_path + self.my_path, name)
        pass

    def get_data(self):
        return self.dict

    def flightradar_demo(self):
        df_flightradar = self.dict['flightradar']
        ax = df_flightradar.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title("Flightradar datasets")
        plt.ylabel("Number of flights")
        plt.xlabel("Time in [d] starting from 1/1/2020")
        return ax, df_flightradar

    def opensky_demo(self):
        df_opensky = self.dict['opensky_flight_hours']
        ax = df_opensky.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title("Open Sky datasets")
        plt.ylabel("Flight hours in [h]")
        plt.xlabel("Time in [d] starting from 1/1/2020")
        return ax, df_opensky

    def apple_demo(self, transportation_type="transit"):
        #select keys
        country = ["United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]
        # load dataset
        df_apple = self.dict['apple']
        # filtering
        df_filtered_apple = df_apple[(df_apple.transportation_type == transportation_type) & (
                    df_apple.geo_type == "country/region") & df_apple.region.isin(country)]
        df_filtered_apple = df_filtered_apple.drop(
            ["geo_type", "transportation_type", "alternative_name", "sub-region", "country"], axis=1)
        df_filtered_apple = df_filtered_apple.pivot_table(columns='region')
        df_filtered_apple = df_filtered_apple.fillna(method="ffill")
        # plotting
        ax = df_filtered_apple.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title("Transportation Type: %s" % transportation_type)
        plt.ylabel("Percentage from baseline 2020-01-13")
        return ax, df_filtered_apple

    def google_demo(self, information_type="workplaces_percent_change_from_baseline"):
        # define keys
        country = ["United States", "India", "China", "Japan", "Russia", "Canada", "Brazil"]
        # load dataset
        df_google = self.dict['google']
        # filter
        df_filtered_google = df_google[df_google.country_region.isin(country)]
        df_filtered_google = df_filtered_google.drop(["country_region_code", "sub_region_1", "sub_region_2"], axis=1)
        df_filtered_google = df_filtered_google[["country_region", "date", information_type]]
        df_filtered_google = df_filtered_google.pivot_table(values=information_type, index='date',
                                                            columns='country_region')
        df_filtered_google = df_filtered_google.fillna(method="ffill")
        # plotting
        ax = df_filtered_google.plot(x_compat=True)
        plt.xticks(rotation=60)
        plt.title(information_type)
        plt.ylabel("Percentage from baseline 2020-02-15")
        return ax, df_filtered_google

