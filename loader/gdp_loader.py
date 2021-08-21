from loader.loader import *


class GDPLoader(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = "gdp/"
        self.keys = ['gdp']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        df_gdp = pd.read_csv(self.path + self.my_path + 'gdp_country.csv', header = 2, index_col=['Country Name'])
        df_gdp = df_gdp.drop(columns = ['Country Code', 'Indicator Name', 'Indicator Code'])
        df_gdp = df_gdp.T
        df_gdp.index.names = ['year']
        self.dict['gdp'] = df_gdp

    def get_summary(self):
        #html
        self.write_html(self.result_path + self.my_path, "gdp_summary", self.dict['gdp'])
        #plot
        country = ['China', 'United States', 'European Union', 'India', 'Brazil', 'Russian Federation', 'Japan', 'Canada']
        df_gdp = self.dict['gdp']
        df_gdp = df_gdp[country]
        ax = df_gdp.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('GDP by country')
        plt.ylabel('US($)')
        plt.xlabel('year')
        self.save_figure(ax, self.result_path + self.my_path, "gdp_demo")

    def get_data(self):
        return self.dict