from loader.loader import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


class Co2Goals(Loader):

    def __init__(self):
        super().__init__()
        self.my_path = self.path + "co2goals/"
        self.keys = ['paris_goals_big8']
        self.dict = dict.fromkeys(self.keys)

    def load(self):
        for key in self.keys:
            # read in only the columns we want to have (usecols[])
            self.dict[key] = pd.read_csv(self.my_path + key + ".csv", sep =";", low_memory=False)
        pass

    def get_summary(self):
        # todo plot Year vs Percentage goal
        # todo print Dataframe head
        for key in self.keys:
            # save all data in temporary variable data
            data = self.dict[key].to_numpy()
            countries = data[:,0]
            
            # plot the goals
            fig1 = plt.figure()
            for i in range(len(countries)):
                # every line starts at 100%=1 and ends at the goal
                y = [100, 100-data[i,4]] #goal_mean is in %
                # the step in x-direction will be different though
                x = [data[i,5], data[i,6]] # compared to, by year
                # all data is in this range
                plt.plot(x, y, label = data[i,0], marker = "o")
            plt.xlabel('Year')
            plt.ylabel('Percentage of Total CO2 Emissions')
            plt.title('Paris Agreement Greenhouse Gas Emission Reduction:\nGoals of the 8 Biggest Contributors Compared to Referenced Year')
            plt.legend()
            #plt.show()
            fig1.savefig(self.result_path + "co2goals/co2goals_lines" +".pdf", bbox_inches='tight')

            
            
            fig2 = plt.figure()
            for i in range(len(countries)):
                # every line starts at 100%=1 and ends at the goal
                y = data[i,4] #goal_mean is in %
                # the step in x-direction will be different though
                x = data[i,6] # compared to, by year
                # all data is in this range
                plt.scatter(x, y, label = data[i,0], s=20*data[i,1])
            plt.plot([2015, 2030], [0, 45], "k", label = "1.5°C goal")
            plt.xlabel('Year')
            plt.ylabel('CO2 Emission Reduction in Percent')
            plt.title('Paris Agreement Greenhouse Gas Emission Reduction:\nGoals of the 8 Biggest Contributors Compared to the 1.5°C Goal')
            plt.legend()
            #plt.show()
            fig2.savefig(self.result_path + "co2goals/co2goals_bubbles" +".pdf", bbox_inches='tight')
        pass

    def get_data(self):
        return self.dict

    def demo(self, plot_type="lines"):
        for key in self.keys:
            # save all data in temporary variable data
            data = self.dict[key].to_numpy()
            countries = data[:,0]
            # plot
            plt.figure()

            if plot_type == "lines":
                for i in range(len(countries)):
                    # every line starts at 100%=1 and ends at the goal
                    y = [100, 100-data[i,4]] #goal_mean is in %
                    # the step in x-direction will be different though
                    x = [data[i,5], data[i,6]] # compared to, by year
                    # all data is in this range
                    plt.plot(x, y, label = data[i,0], marker = "o")
                plt.ylabel('Percentage of CO2 Emissions')
                plt.title('Paris Agreement Greenhouse Gas Emission Reduction:\nGoals of the 8 Biggest Contributors')
            else:
                for i in range(len(countries)):
                    # every line starts at 100%=1 and ends at the goal
                    y = data[i, 4]  # goal_mean is in %
                    # the step in x-direction will be different though
                    x = data[i, 6]  # compared to, by year
                    # all data is in this range
                    plt.scatter(x, y, label=data[i, 0], s=20 * data[i, 1])
                plt.plot([2015, 2030], [0, 55], "k", label = "1.5°C goal")
                plt.ylabel('CO2 Emission Reduction in Percent')
                plt.title('Paris Agreement Greenhouse Gas Emission Reduction:\nGoals of the 8 Biggest Contributors Compared to the 1.5°C Goal')

            plt.xlabel('Year')
            plt.legend()

        return plt.gca()



