from loader.loader import *
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os


class ResultsLoader(Loader):

    def __init__(self):
        super().__init__()
        self.data = pd.read_csv(self.path + 'Covid19/bing_covid.csv', index_col='Updated')
        self.population_df = pd.read_csv(self.path + 'Covid19/pop.csv', usecols=['Country Name', 'Population'], index_col='Country Name')
        self.data.index = pd.to_datetime(self.data.index)
        self.countries = ['China (mainland)', 'United States', 'India', 'Brazil', 'Russia', 'Japan', 'Canada']
        self.EU_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
                        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland',
                        'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland',
                        'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom']
        self.keys = ['cases', 'deaths', 'emissions', 'daily_cases', 'daily_active', 'daily_deaths']
        self.dict = dict.fromkeys(self.keys)
        self.emissions = pd.DataFrame()




    def load(self):
        EU_daily_dict, EU_monthly_dict = self.countries_dict(self.EU_countries)
        country_daily_dict, country_monthly_dict = self.countries_dict(self.countries)
        country_daily_dict['EU'] = pd.DataFrame(index=country_daily_dict['China'].index, columns=country_daily_dict['China'].columns)
        country_monthly_dict['EU'] = pd.DataFrame(index=country_monthly_dict['China'].index, columns=country_monthly_dict['China'].columns)

        for EU_country in self.EU_countries:
            country_daily_dict['EU'] = country_daily_dict['EU'].add(EU_daily_dict[EU_country], fill_value=0)
            country_monthly_dict['EU'] = country_monthly_dict['EU'].add(EU_monthly_dict[EU_country], fill_value=0)

        cases_df = pd.DataFrame(index=country_monthly_dict['China'].index, columns=country_monthly_dict.keys())
        deaths_df = pd.DataFrame(index=country_monthly_dict['China'].index, columns=country_monthly_dict.keys())
        daily_cases_df = pd.DataFrame(columns=country_daily_dict.keys())
        daily_active_df = pd.DataFrame(columns=country_daily_dict.keys())
        daily_deaths_df = pd.DataFrame(columns=country_daily_dict.keys())
        daily_recovered_df = pd.DataFrame(columns=country_daily_dict.keys())

        for country in country_monthly_dict.keys():
            if country == 'Russia':
                country_monthly_dict[country] = country_monthly_dict[country].astype('float') * 100000 / float(self.population_df.loc['Russian Federation'])
            elif country == 'EU':
                country_monthly_dict[country] = country_monthly_dict[country].astype('float') * 100000 / float(self.population_df.loc['European Union'])
            else:
                country_monthly_dict[country] = country_monthly_dict[country].astype('float') * 100000 / float(self.population_df.loc[country])
                
            cases_df[country] = country_monthly_dict[country]['ConfirmedChange']
            deaths_df[country] = country_monthly_dict[country]['DeathsChange']
            
            daily_cases_df[country] = country_daily_dict[country]['Confirmed']
            daily_active_df[country] = country_daily_dict[country]['Confirmed'] - country_daily_dict[country]['Recovered']
            daily_deaths_df[country] = country_daily_dict[country]['Deaths']
            daily_recovered_df[country] = country_daily_dict[country]['Recovered']

        self.dict['cases'] = cases_df
        self.dict['deaths'] = deaths_df
        self.dict['emissions'] = pd.read_csv('results/predictions/overall_vector.csv')
        self.dict['daily_cases'] = daily_cases_df
        self.dict['daily_active'] = daily_active_df
        self.dict['daily_deaths'] = daily_deaths_df
        self.dict['daily_recovered'] = daily_recovered_df

        self.countries = ['EU', 'United States', 'India', 'China', 'Japan', 'Russia', 'Canada', 'Brazil']
        self.sectors = ['Power industry', 'Buildings', 'Transport', 'Other industrial combustion', 'Other sectors']
        self.dict['construction'] = pd.read_csv('results/buildings/emission_predictions.csv', header=0,
                                                  index_col=[0])
        self.dict['construction'].index = self.countries
        self.dict['construction'] = self.dict['construction'].T

        for country in self.dict['construction'].columns:
            self.dict['construction'][country] = self.dict['construction'][country] / \
                                                   self.dict['construction'][country][0]
        self.dict['construction'] = self.dict['construction']
        self.dict['construction']

        self.dict['power'] = pd.read_csv('results/power_industry/predicted_vector.csv', index_col=[0])
        self.dict['power'] = self.dict['power'].iloc[1:]
        self.dict['power'].index = self.dict['construction'].index

        self.dict['transport'] = pd.read_csv('results/mobility/predicted_vector.csv', index_col=[0])
        self.dict['transport'] = self.dict['transport'].rename(columns={'European Union': 'EU'})
        self.dict['transport'].index = self.dict['construction'].index

        self.dict['other_ind'] = pd.read_csv('results/other_industries/predicted_vector.csv', index_col=[0])
        self.dict['other_ind'] = self.dict['other_ind'].rename(columns={'European Union': 'EU'})
        self.dict['other_ind'].index = self.dict['construction'].index

        self.dict['other_sectors'] = pd.DataFrame(1, columns=self.countries, index=self.dict['construction'].index)

        self.percentages = pd.read_csv('prediction/co2_covid/sectors_weights.csv',index_col=[0])

    def get_summary(self):
        """
        should provide descriptive plots of the data to console or better, to the result path.
        """
        pass

    def get_data(self):
        return self.dict
        
    def countries_dict(self, countries):
        daily_dic = {}
        monthly_dic = {}
        for country in countries:
            conditions = (self.data['Country_Region']==country) & (self.data['AdminRegion1'].isna())
            df = self.data[conditions]
            df = df['2020-01-01':'2020-06-30']  
            df = df.drop(columns=['RecoveredChange', 'Latitude', 'Longitude', 'ISO2', 'ISO3', 'ID',
                                  'AdminRegion1', 'AdminRegion2', 'Country_Region'])
    
            daily_df = df.drop(columns=['ConfirmedChange', 'DeathsChange'])
            monthly_df = df.drop(columns=['Confirmed', 'Deaths', 'Recovered'])
            monthly_df = monthly_df.resample('M').sum()
            monthly_df.index = monthly_df.index.map(lambda t: t.replace(day=1))
            if country == 'China (mainland)':
                daily_dic['China'] = daily_df
                monthly_dic['China'] = monthly_df
            else:
                daily_dic[country] = daily_df
                monthly_dic[country] = monthly_df
        return daily_dic, monthly_dic


    def get_result_plots(self, save=False):
        # Obtain and normalize emissions
        emissions = self.dict['emissions'].drop('Unnamed: 0', axis=1)
        emission_sum = emissions.sum(axis=0)
        emission_sum_normalized = emission_sum/6
        emission_drop = 1-emission_sum_normalized
        countries = emission_sum_normalized.index

        # Summarize case numbers (per 100 000 inhabitants)
        cases_sum = self.dict['cases'].sum(axis=0)
        deaths_sum = self.dict['deaths'].sum(axis=0)

        # Store information for all countries except Japan and India
        emission_train = []
        case_train = []
        death_train = []

        # Plot for cases
        plt.figure()
        plt.title("Emission drop in relation to Covid-19 case numbers")
        for country in countries:
            plt.plot(cases_sum[country], emission_drop[country], label=country, marker='x')
            if not ((country == "Japan") or (country == "India")):
                case_train.append(cases_sum[country])
                emission_train.append(emission_drop[country])
        #coef = np.polyfit(case_train, emission_train, 1)
        #poly = np.poly1d(coef)
        #x = np.linspace(min(case_train), max(case_train))
        #plt.plot(x, poly(x), '--', label="Linear regression excluding Japan and India")
        plt.xlabel('Cases from January to June 2020 per 100000 inhabitants')
        plt.ylabel('Average emission drop in percent between January and June 2020')
        plt.legend()
        if save:
            plt.savefig('results/final_results/emission_drop_over_normalized_cases.pdf')
        ax_cases = plt.gca()

        # Plot for deaths
        plt.figure()
        plt.title("Emission drop in relation to Covid-19 deaths")
        for country in countries:
            plt.plot(deaths_sum[country], emission_drop[country], label=country, marker='x')
            if not ((country == "Japan") or (country == "India")):
                death_train.append(deaths_sum[country])
        #coef = np.polyfit(death_train, emission_train, 1)
        #poly = np.poly1d(coef)
        #x = np.linspace(min(death_train), max(death_train))
        #plt.plot(x, poly(x), '--', label="Linear regression excluding Japan and India")
        plt.xlabel('Deaths from January to June 2020 per 100000 inhabitants')
        plt.ylabel('Average emission drop in percent between January and June 2020')
        plt.legend()
        if save:
            plt.savefig('results/final_results/emission_drop_over_normalized_deaths.pdf')
        ax_deaths = plt.gca()

        return [ax_cases, ax_deaths]

    def get_time_series_cases(self, country):
        plt.figure()
        plt.title("Time series Covid-19 statistics in {}".format(country))
        self.dict['daily_cases'][country].plot(label="Confirmed Cases")
        self.dict['daily_active'][country].plot(label="Active Cases")
        self.dict['daily_deaths'][country].plot(label="Deaths")
        self.dict['daily_recovered'][country].plot(label="Recoveries")
        plt.xlabel("Date")
        plt.ylabel("Number of cases")
        plt.legend()
        ax = plt.gca()
        return ax

    def get_bar_plot(self, country):
        construction = 1 - self.dict['construction'][country].values.sum()/6
        power = 1 - self.dict['power'][country].values.sum()/6
        transport = 1 - self.dict['transport'][country].values.sum()/6
        other_ind = 1 - self.dict['other_ind'][country].values.sum()/6
        other_sectors = 1 - self.dict['other_sectors'][country].values.sum()/6
        drops = [100*power, 100*construction, 100*transport, 100*other_ind]
        text = []
        for drop in drops:
            text.append(str(drop.round(1))+"%")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=self.sectors[0:4], y=drops, text=text, textposition='outside', name='CO2 Emission drop per sector'.format(country)))
        fig.update_layout(
            title={
                'text': 'CO2 Emission drop per sector averaged from January to June 2020 in {}'.format(country),
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.update_layout(autosize=True, xaxis_tickfont_size=14,
            yaxis = dict(title='Emission drop in percent', titlefont_size=16, tickfont_size=14,),
            legend = dict(x=0, y=1.0, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'), margin=dict(t=70),
)
        #fig.update_yaxes(automargin=True)
        #fig.write_image('results/sector_overview/bar_plot_{}.pdf'.format(country))
        return fig

    def get_pie_plot(self, country):
        percentages = self.percentages.rename(columns={country: "Contribution"})["Contribution"].round(3)
        fig = px.pie(percentages, values="Contribution", names=self.percentages.index, color_discrete_sequence=px.colors.diverging.balance)
        fig.update_layout(
            title={
                'text': 'CO2 Emission by sector in percentage for {}'.format(country),
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            legend = dict(x=0.8, y=0.95, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'))
        fig.update_layout(autosize=True)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        #fig.write_image('results/sector_overview/pie_plot_{}.pdf'.format(country))
        return fig