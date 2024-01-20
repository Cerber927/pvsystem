from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
from math import ceil, floor
import matplotlib.pyplot as plt
import numpy as np


def get_location(lon, lat):
    location = LocationInfo(latitude=lat, longitude=lon)
    return location


def get_sunshine_time(location, date):
    s = sun(location.observer, date=date)
    return s


class load:
    def __init__(self, time_availability, base_power, working_power):
        self.time_availability = time_availability
        self.base_power = base_power
        self.working_power = working_power
        self.power = 0


motor1_time = [0] * 24
motor2_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
motor3_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
motor1 = load(motor1_time, 100, 300)
motor2 = load(motor2_time, 150, 450)
motor3 = load(motor3_time, 200, 600)
load_list = [motor1, motor2, motor3]


class source:
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

        return self.consumption_power

    def generation_power(self):
        location = get_location(self.lon, self.lat)
        s = get_sunshine_time(location, self.date)
        for j in range(24):
            if ceil(s['sunrise'].hour) <= j <= floor(s['sunset'].hour):
                temp_power = self.irradiance_def * self.area * self.efficiency
            else:
                temp_power = 0

            self.source_power.append(temp_power)

        return self.source_power

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


battery = source(6.953101, 50.935173, "2024-01-01", load_list)
print(battery.date)

load_power = battery.load_power()
print(load_power)

source_power = battery.generation_power()
print(source_power)

battery.power_flow()

injection = battery.get_injection_power()
print(injection)
supply = battery.get_supply_power()
print(supply)

x = np.arange(24)
y1 = source_power
y2 = load_power
y3 = injection
y4 = supply

fig, ax = plt.subplots()
ax.set(title='PV System', xlabel='Time(Hour)', ylabel='Power(Kw)')

ax.plot(x, y1, label='Source Power', color='green')
ax.plot(x, y2, label='Load Power', color='red')
ax.plot(x, y3, label='Injection Power', color='blue')
ax.plot(x, y4, label='Supply Power', color='yellow')
ax.legend()
plt.show()
