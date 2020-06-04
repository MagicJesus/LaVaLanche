from merge_predict import *
from weather_analysis import overall_weather_analysis

records = add_weather(add_season(load_topo_data()), overall_weather_analysis())
print(get_risks(records))
