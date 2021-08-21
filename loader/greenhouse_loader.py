from loader.loader import *


class GreenhouseLoader(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = "greenhouse/"
        self.keys = ['gg_global_monthly', 'gg_global_annual', 'gg_global_ann_increase', 'co2_global_weekly',   # gml
                     'co2_country', 'co2_country_sector',
                     'ch4_country',
                     'n2o_country']  # edgar
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        aux_gml = self.global_monitoring_laboratory()
        aux_ed = self.edgar()

        for i in range(len(self.keys)):
            if (i < len(aux_gml)):
                self.dict[self.keys[i]] = aux_gml[i]
            else:
                self.dict[self.keys[i]] = aux_ed[i - len(aux_gml)]

    def get_summary(self):

        self.write_html(self.result_path + self.my_path, "greenhouse_summary", self.dict['co2_country'])
        axes = [self.gg_global_monthly_demo()[0], self.gg_global_annual_demo()[0], self.gg_global_ann_increase_demo()[0], self.co2_global_weekly_demo()[0],
                self.co2_country_demo()[0], self.co2_country_sector_demo()[0],
                self.ch4_country_demo()[0],
                self.n2o_country_demo()[0]]
        names = ["gg_global_monthly_demo", "gg_global_annual_demo", "gg_global_ann_increase_demo", "co2_global_weekly_demo",
                 "co2_country_demo", "co2_country_sector_demo",
                 "ch4_country_demo",
                 "n2o_country_demo"]
        for name, ax in zip(names, axes):
            self.save_figure(ax, self.result_path + self.my_path, name)
        pass

    def get_data(self):
        # todo implement
        return self.dict



    def global_monitoring_laboratory(self):
        # Units:

        # CO2: units micro/mol
        co2_norm = 1

        # CH4: units nano/mol
        #ch4_norm = 10**(-3) #to micro/mol
        ch4_norm = 1

        # N2O: units nano/mol
        #n2o_norm = 10**(-3) #to micro/mol
        n2o_norm = 1

        # SF6: units pico/mol
        #sf6_norm = 10**(-6) #to micro/mol
        sf6_norm = 1

        # CO2
        # Weekly
        df = pd.read_csv(self.path + self.my_path + 'co2_weekly_mlo.csv',
                                header=47, usecols=['average', 'year', 'month', 'day'])
        df = df.rename(columns={'average': 'co2 average (micro/mol)'})
        df = df.set_index(df['year'].map(str) + '-' + df['month'].map(str) + '-' + df['day'].map(str))
        df = df.drop(columns=['year', 'month', 'day'])
        co2_weekly = pd.DataFrame(df['co2 average (micro/mol)'] * co2_norm)

        # Monthly: use of interpolated to fill miss data
        df = pd.read_csv(self.path + self.my_path + 'co2_mm_mlo.csv',
                                header=70, usecols=['interpolated', 'year', 'month'])
        df = df.rename(columns={'interpolated': 'co2 average (micro/mol)'})
        df = df.set_index(df['year'].map(str) + '-' + df['month'].map(str))
        df = df.drop(columns=['year', 'month'])
        co2_monthly = pd.DataFrame(df['co2 average (micro/mol)'] * co2_norm)

        # Annual
        df = pd.read_csv(self.path + self.my_path + 'co2_annmean_mlo.csv',
                                header=55, index_col=['year'],
                                usecols=['year', 'co2 average (micro/mol)'], names=['year','co2 average (micro/mol)'])
        co2_annual = pd.DataFrame(df['co2 average (micro/mol)'] * co2_norm)

        # Annual increase
        df = pd.read_csv(self.path + self.my_path + 'co2_gr_mlo.csv',
                                header=58, index_col=['year'],
                                usecols=['year', 'co2 increase'], names = ['year', 'co2 increase'])
        co2_ann_increase = pd.DataFrame(df['co2 increase'] * co2_norm)

        ############ Missing values ########################################################
        null_term_weekly = -999.99
        co2_weekly = co2_weekly.where(co2_weekly!=null_term_weekly)
        #print(co2_weekly.isnull().sum().sum())
        co2_weekly = co2_weekly.fillna(method='ffill') # it uses last value
        # There are not missing values due to the use of interpolated as average:
        # look into the csv to see the details
        null_term_monthly = -99.99
        co2_monthly = co2_monthly.where(co2_monthly!=null_term_monthly)
        #print(co2_monthly.isnull().sum().sum())

        # CH4
        # Monthly
        df = pd.read_csv(self.path + self.my_path + 'ch4_mm_gl.txt',
                                header = 62, delim_whitespace=True,
                                usecols = ['year', 'month', 'average'])
        df = df.rename(columns={'average': 'ch4 average (nano/mol)'})
        df = df.set_index(df['year'].map(str) + '-' + df['month'].map(str))
        df = df.drop(columns=['year', 'month'])
        ch4_monthly = pd.DataFrame(df['ch4 average (nano/mol)'] * ch4_norm)

        # Annual
        df = pd.read_csv(self.path + self.my_path + 'ch4_annmean_gl.txt',
                                header = 62, delim_whitespace=True, usecols = ['year', 'ch4 average (nano/mol)'],
                                index_col = ['year'], names = ['year', 'ch4 average (nano/mol)'])
        ch4_annual = pd.DataFrame(df['ch4 average (nano/mol)'] * ch4_norm)

        # Annual increase
        df = pd.read_csv(self.path + self.my_path + 'ch4_gr_gl.txt',
                                header = 64, delim_whitespace=True, usecols = ['year', 'ch4 increase'],
                                index_col = ['year'], names = ['year', 'ch4 increase'])
        ch4_ann_increase = pd.DataFrame(df['ch4 increase'] * ch4_norm)

        # N2O
        # Monthly
        df = pd.read_csv(self.path + self.my_path + 'n2o_mm_gl.txt',
                                header=60, delim_whitespace=True,
                                usecols=['average', 'year', 'month'])
        df = df.rename(columns={'average': 'n2o average (nano/mol)'})
        df = df.set_index(df['year'].map(str) + '-' + df['month'].map(str))
        df = df.drop(columns=['year', 'month'])
        n2o_monthly = pd.DataFrame(df['n2o average (nano/mol)'] * n2o_norm)

        # Annual
        df = pd.read_csv(self.path + self.my_path + 'n2o_annmean_gl.txt',
                                header=60, delim_whitespace=True,
                                index_col=['year'],
                                usecols=['year', 'n2o average (nano/mol)'], names=['year', 'n2o average (nano/mol)'])
        n2o_annual = pd.DataFrame(df['n2o average (nano/mol)'] * n2o_norm)

        # Annual increase
        df = pd.read_csv(self.path + self.my_path + 'n2o_gr_gl.txt',
                                header=62, delim_whitespace=True,
                                index_col=['year'],
                                usecols=['year', 'n2o increase'], names=['year', 'n2o increase'])
        n2o_ann_increase = pd.DataFrame(df['n2o increase'] * n2o_norm)

        # SF6
        # Monthly
        df = pd.read_csv(self.path + self.my_path + 'sf6_mm_gl.txt', header = 60,
                                delim_whitespace=True, usecols = ['year', 'month', 'average'])
        df = df.rename(columns={'average': 'sf6 average (pico/mol)'})
        df = df.set_index(df['year'].map(str) + '-' + df['month'].map(str))
        df = df.drop(columns=['year', 'month'])
        sf6_monthly = pd.DataFrame(df['sf6 average (pico/mol)'] * sf6_norm)

        # Annual
        df = pd.read_csv(self.path + self.my_path + 'sf6_annmean_gl.txt', header = 60,
                                delim_whitespace=True, usecols = ['year', 'sf6 average (pico/mol)'],
                                index_col = ['year'], names = ['year', 'sf6 average (pico/mol)'])
        sf6_annual = pd.DataFrame(df['sf6 average (pico/mol)'] * sf6_norm)

        # Annual increase
        df = pd.read_csv(self.path + self.my_path + 'sf6_gr_gl.txt', header = 62,
                                delim_whitespace=True, usecols = ['year', 'sf6 increase'],
                                index_col = ['year'], names = ['year', 'sf6 increase'])
        sf6_ann_increase = pd.DataFrame(df['sf6 increase'] * sf6_norm)

        # Complete datasets
        monthly_df = pd.concat([co2_monthly, ch4_monthly, n2o_monthly, sf6_monthly], axis=1, sort=False)
        annual_df = pd.concat([co2_annual, ch4_annual, n2o_annual, sf6_annual], axis=1, sort=False)
        ann_increase_df = pd.concat([co2_ann_increase, ch4_ann_increase, n2o_ann_increase, sf6_ann_increase], axis=1, sort=False)

        return [monthly_df, annual_df, ann_increase_df, co2_weekly]


    def edgar(self):
        # CO2 by country
        co2_country = pd.read_csv(self.path + self.my_path + 'co2_country_edgar.csv', index_col='country_name', decimal=',')
        co2_country = co2_country.dropna()
        co2_country = co2_country.T
        co2_country.index.names = ['year']
        # CO2 by sector and by country
        co2_country_sector = pd.read_csv(self.path + self.my_path + 'co2_country_sector_edgar.csv', index_col=[0, 1], decimal=',')
        sectors = list(set(co2_country_sector.index.get_level_values('Sector')))

        # CH4 by country
        ch4_country = pd.read_csv(self.path + self.my_path + 'ch4_country_edgar.csv', index_col='Name', decimal='.', header = 9)
        ch4_country = ch4_country.drop(['IPCC-Annex', 'World Region', 'ISO_A3', 'Unnamed: 50', 'Unnamed: 51'], axis = 1)
        ch4_country = ch4_country.T
        ch4_country.index.names = ['year']

        # N2O by country
        n2o_country = pd.read_csv(self.path + self.my_path + 'n2o_country_edgar.csv', index_col='Name', decimal='.', header = 9)
        n2o_country = n2o_country.drop(['IPCC-Annex', 'World Region', 'ISO_A3', 'Unnamed: 50', 'Unnamed: 51'], axis = 1)
        n2o_country = n2o_country.T
        n2o_country.index.names = ['year']

        # EU countries
        EU_co2 = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
                    'Estonia', 'Finland', 'France and Monaco', 'Germany', 'Greece', 'Hungary', 'Ireland',
                    'Italy, San Marino and the Holy See', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
                    'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain and Andorra', 'Sweden', 'United Kingdom']

        EU_ch4 = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark',
                    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
                    'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland',
                    'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom']

        co2_country['EU'] = pd.Series(name='EU')
        arrays = [sectors, ['EU' for i in range(5)]]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples, names=['Sector', 'country_name'])
        EU_df = pd.DataFrame(index=index, columns=co2_country_sector.columns)

        ch4_country['EU'] = pd.Series(name='EU')
        n2o_country['EU'] = pd.Series(name='EU')

        for country_co2, country_ch4 in zip(EU_co2, EU_ch4):
            co2_country['EU'] = co2_country['EU'].add(co2_country[country_co2], fill_value=0)
            ch4_country['EU'] = ch4_country['EU'].add(ch4_country[country_ch4], fill_value=0)
            n2o_country['EU'] = n2o_country['EU'].add(n2o_country[country_ch4], fill_value=0)
            # sectors in CO2
            for sector in sectors:
                EU_df.loc[(sector, 'EU')] = EU_df.loc[(sector, 'EU')].add(co2_country_sector.loc[(sector, country_co2)], fill_value=0)

        co2_country_sector = pd.concat([co2_country_sector, EU_df])
        co2_country_sector = co2_country_sector.T
        co2_country_sector.index.names = ['year']

        # Change names in CH4 and N2O
        ch4_country = ch4_country.rename(columns={'Russian Federation': 'Russia'})
        n2o_country = n2o_country.rename(columns={'Russian Federation': 'Russia'})

        return [co2_country, co2_country_sector, ch4_country, n2o_country]

    def gg_global_monthly_demo(self):
        df_gg_global_monthly = self.dict['gg_global_monthly']
        ax = df_gg_global_monthly.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Monthly greenhouse gases concentration')
        plt.ylabel('Mole fraction')
        plt.xlabel('date')
        return ax, df_gg_global_monthly

    def gg_global_annual_demo(self):
        df_gg_global_annual = self.dict['gg_global_annual']
        ax = df_gg_global_annual.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Annual greenhouse gases concentration')
        plt.ylabel('Mole fraction')
        plt.xlabel('year')
        return ax, df_gg_global_annual

    def gg_global_ann_increase_demo(self):
        df_gg_global_ann_increase = self.dict['gg_global_ann_increase']
        ax = df_gg_global_ann_increase.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Annual greenhouse gases concentration increase')
        plt.ylabel('Increase')
        plt.xlabel('year')
        return ax, df_gg_global_ann_increase

    def co2_global_weekly_demo(self):
        df_co2_global_weekly = self.dict['co2_global_weekly']
        ax = df_co2_global_weekly.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Weekly CO2 concentration')
        plt.ylabel('Mole fraction of CO2')
        plt.xlabel('date from 19/5/1974')
        return ax, df_co2_global_weekly

    def co2_country_demo(self):
        df_co2_country = self.dict['co2_country']
        country = ['China', 'United States', 'EU', 'India', 'Brazil', 'Russia', 'Japan', 'Canada']
        df_co2_country_filtered = df_co2_country[country]
        df_co2_country_filtered = df_co2_country_filtered.astype(float)
        ax = df_co2_country_filtered.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Annual CO2 emissions by country')
        plt.ylabel('Mt CO2/year')
        plt.xlabel('year')
        return ax, df_co2_country

    def co2_country_sector_demo(self):
        df_co2_country_sector = self.dict['co2_country_sector']
        country = ['Spain and Andorra', 'Germany']
        # print(sectors)
        # ['Power Industry', 'Other industrial combustion', 'Other sectors', 'Buildings', 'Transport']
        sector = 'Power Industry'
        df_co2_country_sector_filtered = df_co2_country_sector[sector]
        df_co2_country_sector_filtered = df_co2_country_sector_filtered[country]
        ax = df_co2_country_sector_filtered.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title(f'Annual CO2 emissions by country due to {sector} sector')
        plt.ylabel('Mt_CO2/year')
        plt.xlabel('year')
        return ax, df_co2_country_sector_filtered

    def ch4_country_demo(self):
        df_ch4_country = self.dict['ch4_country']
        country = ['China', 'United States', 'EU', 'India', 'Brazil', 'Russia', 'Japan', 'Canada']
        df_ch4_country_filtered = df_ch4_country[country]
        df_ch4_country_filtered = df_ch4_country_filtered.astype(float)
        ax = df_ch4_country_filtered.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Annual CH4 emissions by country')
        plt.ylabel('CH4 emissions')
        plt.xlabel('year')
        return ax, df_ch4_country

    def n2o_country_demo(self):
        df_n2o_country = self.dict['n2o_country']
        country = ['China', 'United States', 'EU', 'India', 'Brazil', 'Russia', 'Japan', 'Canada']
        df_n2o_country_filtered = df_n2o_country[country]
        df_n2o_country_filtered = df_n2o_country_filtered.astype(float)
        ax = df_n2o_country_filtered.plot(kind='line', x_compat=True)
        plt.xticks(rotation=60)
        plt.title('Annual N2O emissions by country')
        plt.ylabel('N2O emissions')
        plt.xlabel('year')
        return ax, df_n2o_country
