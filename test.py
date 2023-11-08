import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

fig, ax = plt.subplots()


circle = Circle((0, 0), radius=30, fill=False, color='b')

ax.add_patch(circle)
plt.scatter(0, 0, color='b', label='predator')

ax.set_xlim(-40, 40)
ax.set_ylim(-40, 40)

preys_x = [np.random.uniform(-40, 40) for _ in range(100)]
preys_y = [np.random.uniform(-40, 40) for _ in range(100)]

plt.scatter(preys_x, preys_y, color='r', label='preys')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()