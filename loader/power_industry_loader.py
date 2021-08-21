from loader.loader import *

class PowerLoader(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = "power_industry/"
        self.keys = ['brent', 'natural_gas', 'supply', 'oil']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        # Price Brent
        df = pd.read_csv(self.path + self.my_path + 'brent.csv', header = 0, index_col = ['Date'])
        df.index = pd.to_datetime(df.index)
        df.index = df.index.map(lambda t: t.replace(day=1))
        self.dict['brent'] = df
        
        # Price natural gas
        df = pd.read_csv(self.path + self.my_path + 'natural_gas.csv', header = 0, index_col = ['Month'])
        df.index = pd.to_datetime(df.index)
        df.index.names = ['Date']
        self.dict['natural_gas'] = df
        
        # Supply and oil
        for file in ['supply', 'oil']:
            df = pd.read_csv(self.path + self.my_path + file + '.csv', index_col=['GEO/TIME'], decimal=',')
            df = df.T
            df.columns.names = ['']
            df.index = pd.to_datetime(df.index)
            df = df.astype('float64')
            self.dict[file] = df
        
        
    def get_summary(self):
        #HTML
        self.write_html(self.result_path + self.my_path, "brent_summary", self.dict['brent'])

        #PLOTS
        
        # Price brent
        df_brent = self.dict['brent']
        ax = df_brent.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Brent spot prices')
        plt.ylabel('Dollars per barrel')
        plt.xlabel('Date')
        self.save_figure(ax, self.result_path + self.my_path, "brent_demo")

        # Price natural gas
        df_natural_gas = self.dict['natural_gas']
        ax = df_natural_gas.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Price of natural gas')
        plt.ylabel('US($)')
        plt.xlabel('Date')
        self.save_figure(ax, self.result_path + self.my_path, "natural_gas_demo")
        
        # Supply
        df = self.dict['supply']
        countries = ['Germany', 'France', 'Spain']
        ax = df[countries].plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Electricity, gas, steam and air conditioning supply')
        plt.ylabel('Index, 2015=100')
        plt.xlabel('Date')
        self.save_figure(ax, self.result_path + self.my_path, "supply_demo")
        
        # Petroleum
        df = self.dict['oil']
        countries = ['Germany', 'France', 'Spain']
        ax = df[countries].plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Supply oil ')
        plt.ylabel('Thousand tonnes')
        plt.xlabel('Date')
        self.save_figure(ax, self.result_path + self.my_path, "oil_demo")
        

    def get_data(self):
        return self.dict