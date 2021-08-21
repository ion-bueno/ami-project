from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt


class Loader(ABC):

    def __init__(self):
        self.path = "datasets/"
        self.result_path = "results/"

    @abstractmethod
    def load(self):
        """
        loads csv into a dataframe, which is a member variable of the class.
        """
        pass

    @abstractmethod
    def get_summary(self):
        """
        should provide descriptive plots of the data to console or better, to the result path.
        """
        pass

    @abstractmethod
    def get_data(self):
        """
        provides access to the full dataframe.
        """
        pass

    def write_html(self, result_path, filename, dataframe):
        """
        saves head of dataframe to path

        :param result_path: e.g. self.result_path + self.my_path (results/mobility)
        :param filename: mobility_summary
        :param dataframe:
        """
        pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>
        html_string = '''
	            <html>
	              <head><title>HTML Pandas Dataframe with CSS</title></head>
	              <link rel="stylesheet" type="text/css" href="../df_style.css"/>
	              <body>
	                {table}
	              </body>
	            </html>.
	            '''
        with open(result_path + filename +".html", "w") as f:
            f.write(html_string.format(table=dataframe.head().to_html(classes='mystyle')))
        pass

    def save_figure(self, axis, result_path, filename):
        """
        saves plot to path

        :param axis: ax = df.plot(...)
        :param result_path: e.g. self.result_path + self.my_path (results/mobility)
        :param filename: e.g. google_plot
        :return:
        """
        fig = axis.get_figure()
        fig.savefig(result_path + filename +".pdf", bbox_inches='tight')
        pass

    def get_keys(self, df):
        """
        get key tree from supplied dict/dataframe
        """
        #todo implement
        pass




