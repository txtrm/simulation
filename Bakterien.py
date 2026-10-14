import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

x = 0
y = 0
initial_population = 100000
growth_rate = 1.0136
max_capacity = 1000000000
birth_rate = 0.02
death_rate = 0.01
nutrition = 23000000
nutrition_list = [nutrition]
nutrition_per_bacteria = 0.00001
nutrition_dep_rate = initial_population*nutrition_per_bacteria
p = initial_population

# Graph geht nach growth_rate > 1 nach unten, da (i=5) [5-1]*1=4

x = [0]
population = [initial_population]

growth_rate = birth_rate-death_rate+1

while p < max_capacity:
    p = population[len(population)-1]*growth_rate
    x.append(len(population)/110)
    population.append(p)
    nutrition_dep_rate = nutrition_per_bacteria*p
    nutrition -= nutrition_dep_rate
    nutrition_list.append(nutrition)

birth_rate = death_rate
growth_rate = birth_rate-death_rate+1

while nutrition > 0:
    p = population[len(population)-1]*growth_rate
    x.append(len(population)/110)
    population.append(p)
    nutrition_dep_rate = nutrition_per_bacteria*p
    nutrition -= nutrition_dep_rate
    nutrition_list.append(nutrition)

birth_rate = 0
death_rate = 0.001
growth_rate = birth_rate-death_rate+1

while p > 0.2:
    p = population[len(population)-1]*growth_rate
    x.append(len(population)/110)
    population.append(p)
    nutrition_list.append(nutrition)

plt.figure(figsize=(12, 5))
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
plt.xlabel("Zeit in Stunden")
plt.ylabel("Population")
plt.xlim(0, 50)
plt.ylim(0, max_capacity+100000000)
pop_line, = plt.plot(x, population, linestyle='--', marker='o', markersize=0.01)
ax2 = plt.gca().twinx()
ax2.plot(x, nutrition_list, color='green')
ax2.set_ylabel("Nutrition")
cursor_line = plt.axvline(x=0, color='red')
plt.grid()
plt.show(block=False)

from matplotlib.animation import FuncAnimation
import numpy as np

fig2, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

scatter = ax.scatter([], [], s=1)

# how many dots per frame (each dot represents many bacteria)
DOT_SCALE = 10000   # more dots to fill the screen

def update(frame):
    count = int(population[frame] // DOT_SCALE)
    # random positions for the dots
    dots = np.random.rand(count, 2) * 5
    scatter.set_offsets(dots)
    global ani
    if population[frame] >= 1_000_000_000:
        ani.event_source.interval = 5
    else:
        ani.event_source.interval = 10
    global cursor_line
    cursor_line.set_xdata([x[frame], x[frame]])
    cursor_line.figure.canvas.draw_idle()
    # Hide the population line if population reaches zero or below
    if population[frame] <= 0:
        pop_line.set_visible(False)
    else:
        pop_line.set_visible(True)
    pop_line.figure.canvas.draw_idle()
    ax.set_title(f"Population: {int(population[frame]):,}")
    return scatter,

ani = FuncAnimation(fig2, update, frames=len(population), interval=20, repeat=False)

plt.show()