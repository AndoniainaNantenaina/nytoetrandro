from datetime import datetime
import pytz

class Weather:
    def __init__(self, city_name, dt, main_tmp, main_tmp_min, main_tmp_max, weather_id, weather_main, weather_desc, weather_icon, timezone):

        #   Nom de la ville
        self.city_name=city_name

        #   Date
        time_zone = pytz.FixedOffset(timezone / 60)
        self.dt = datetime.fromtimestamp(dt, time_zone).strftime("%a")
        self.hour = datetime.fromtimestamp(dt, time_zone).strftime("%H:%M")

        #   Les températures
        self.main_tmp = round(main_tmp - 273.15, 0)
        self.main_tmp_min = round(main_tmp_min - 273.15, 0)
        self.main_tmp_max = round(main_tmp_max - 273.15, 0)

        #   Les météos
        self.weather_id = weather_id
        self.weather_main = weather_main
        self.weather_desc = weather_desc
        self.weather_icon = weather_icon