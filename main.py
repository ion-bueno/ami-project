from loader.mobility_loader import MobilityLoader
from loader.greenhouse_loader import GreenhouseLoader
from loader.co2goals_loader import Co2Goals
from loader.covid_loader import CovidLoader
from loader.bing_covid_loader import BingCovidLoader
from loader.gdp_loader import GDPLoader
from loader.power_industry_loader import PowerLoader
from loader.results_loader import ResultsLoader


def test_loader(loader_class):
	loader = loader_class()
	print("Checking class: " + loader.__class__.__name__)
	loader.load()
	df = loader.get_data()
	print(loader.__class__.__name__+" keys: ", df.keys())
	loader.get_summary()
	pass


if __name__ == "__main__":
	loader_list = [MobilityLoader
		, GreenhouseLoader
		, Co2Goals
		, BingCovidLoader
		, CovidLoader
		, GDPLoader
		, PowerLoader
		, ResultsLoader]
	for loader_class in loader_list:
		test_loader(loader_class)
