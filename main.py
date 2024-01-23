from model import Load, Source
import matplotlib.pyplot as plt
import numpy as np

# Initialize 3 loads, motor1 doesn't work, motor2 and motors works from 9am to 5pm
motor1_time = [0] * 24
motor2_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
motor3_time = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
motor1 = Load(motor1_time, 100, 300)
motor2 = Load(motor2_time, 150, 450)
motor3 = Load(motor3_time, 200, 600)
load_list = [motor1, motor2, motor3]

battery = Source(6.953101, 50.935173, "2024-01-01", 10, load_list)
print(battery.date)

battery.load_power()
load_power = battery.get_consumption_power()
print(load_power)

battery.generation_power()
source_power = battery.get_source_power()
print(source_power)

battery.power_flow()

injection = battery.get_injection_power()
print(injection)
supply = battery.get_supply_power()
print(supply)

# get the plot of all the powers
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
