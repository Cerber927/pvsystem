from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
from math import ceil, floor


def get_location(lon, lat):
    """

    :param lon:
    :param lat:
    :return: location
    """
    location = LocationInfo(latitude=lat, longitude=lon)
    return location


def get_sunshine_time(location, date):
    """

    :param location:
    :param date:
    :return: s is a dictionary. Here we get the sunrise time and sunset time.
    """
    s = sun(location.observer, date=date)
    return s


class Load:
    """
    This class describes a load in electrical system. It has 4 attributes.

    time_availability: a list with a length of 24, representing working state in 24 hours.
        0: load not working, power = base_power
        1: load working, power = working_power
    base_power: float. When load not works, the consumption of the load
    working_power: float. When load works, the consumption of the load
    power: float. The real consumption of the load regardless of working or not

    """
    def __init__(self, time_availability, base_power, working_power):
        self.time_availability = time_availability
        self.base_power = base_power
        self.working_power = working_power
        self.power = 0


class Source:
    """
    This class describes a solar panel in electrical system. It has 12 attributes.

    lon: float. longitude
    lat: float. latitude
    data_str: string, with format of "YYYY-MM-DD", for example "2024-01-01"
    loads: a list, containing all the loads connecting the source
    irradiance_def: float. 1000 means 1000W/m^2
    area: float. The area of the solar panel. 10 means 10m^2
    efficiency: float. The ratio of how much solar power can be transferred into electrical power
    consumption_power: a list with a length of 24, representing the power consumed by loads in 24 hours.
    source_power: a list with a length of 24, representing the power produced by source in 24 hours.
    date: date
    injection_power: a list with a length of 24. If produced power is higher than the consumed power,
        the extra power will be transferred into other grid.
    supply_power: a list with a length of 24. If produced power is lower than the consumed power,
        the power from other grid will be transferred into this grid.
    """
    def __init__(self, lon, lat, date_str, area, loads):
        self.consumption_power = []
        self.lon = lon
        self.lat = lat
        self.date_str = date_str
        self.loads = loads
        self.irradiance_def = 1000
        self.area = area
        self.efficiency = 0.1
        self.source_power = []
        self.date = datetime.strptime(date_str, "%Y-%m-%d")
        self.injection_power = [0] * 24
        self.supply_power = [0] * 24

    def load_power(self):
        """
        This function gets the power consumed by all loads in every hour
        The result is a list stored in consumption_power
        """
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
        """
        This function gets the power produced by the source in every hour.
        The result is a list stored in source_power.
        """
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

    def power_flow(self):
        """
        This function calculates how much extra power the system need
            or how much extra the system provide in every hour
        injection_power is a list with a length of 24, representing the power the system needs in every hour
        supply_power is a list with a length of 24, representing the power the system provides in every hour
        """
        for j in range(24):
            if self.source_power[j] <= self.consumption_power[j]:
                self.injection_power[j] = self.consumption_power[j] - self.source_power[j]
            else:
                self.supply_power[j] = self.source_power[j] - self.consumption_power[j]

    def get_injection_power(self):
        return self.injection_power

    def get_supply_power(self):
        return self.supply_power
