from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
from math import ceil, floor


def get_location(lon, lat):
    location = LocationInfo(latitude=lat, longitude=lon)
    return location


def get_sunshine_time(location, date):
    s = sun(location.observer, date=date)
    return s


# time_availability should be a list with a length of 24. That is 24 hours.
# if time_availability = 0, the load is not working, power = base_power
# if time_availability = 1, the load is working, power = working_power
class Load:
    def __init__(self, time_availability, base_power, working_power):
        self.time_availability = time_availability
        self.base_power = base_power
        self.working_power = working_power
        self.power = 0


# The Source get longitude and latitude, calculate the sunrise and sunset time in a certain given date
# Input variable loads is a list containing loads
# consumption_power is a list with a length of 24. It shows all the power the loads consuming in every hour
# source_power is a list with a length of 24. It shows all the power the solar panel producing in every hour
# injection_power is a list with a length of 24. It shows every hour how much power the system get from other grid
# supply_power is a list with a length of 24. It shows every hour how much extra power the system provides to other grid
class Source:
    def __init__(self, lon, lat, date_str, loads):
        self.consumption_power = []
        self.lon = lon
        self.lat = lat
        self.date_str = date_str
        self.loads = loads
        self.irradiance_def = 1000
        self.area = 10
        self.efficiency = 0.1
        self.source_power = []
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.loads_num = len(loads)
        self.injection_power = [0] * 24
        self.supply_power = [0] * 24

    # The function gets the power consumed by all loads in every hour
    # The result is a list stored in consumption_power
    def load_power(self):
        for j in range(24):
            temp_power = 0
            for _load in list(self.loads):
                if _load.time_availability[j] == 0:
                    _load.power = _load.base_power
                else:
                    _load.power = _load.working_power

                temp_power += _load.power

            self.consumption_power.append(temp_power)

    # The function gets the power produced by the source in every hour
    # The result is a list stored in source_power
    def generation_power(self):
        location = get_location(self.lon, self.lat)
        s = get_sunshine_time(location, self.date)
        for j in range(24):
            if ceil(s['sunrise'].hour) <= j <= floor(s['sunset'].hour):
                temp_power = self.irradiance_def * self.area * self.efficiency
            else:
                temp_power = 0

            self.source_power.append(temp_power)

    def get_consumption_power(self):
        return self.consumption_power

    def get_source_power(self):
        return self.source_power

    # The function calculates how much extra power the system need or how much extra the system provide in every hour
    # injection_power is a list with a length of 24, showing the power the system needs in every hour
    # supply_power is a list with a length of 24, showing the power the system provides in every hour
    def power_flow(self):
        for j in range(24):
            if self.source_power[j] <= self.consumption_power[j]:
                self.injection_power[j] = self.consumption_power[j] - self.source_power[j]
            else:
                self.supply_power[j] = self.source_power[j] - self.consumption_power[j]

    def get_injection_power(self):
        return self.injection_power

    def get_supply_power(self):
        return self.supply_power
