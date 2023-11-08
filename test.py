import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from scipy.spatial import KDTree

fig, ax = plt.subplots()


circle = Circle((0, 0), radius=30, fill=False, color='b')

ax.add_patch(circle)
plt.scatter(0, 0, color='b', label='predator')

ax.set_xlim(-40, 40)
ax.set_ylim(-40, 40)

preys_x = [np.random.uniform(-40, 40) for _ in range(10)]
preys_y = [np.random.uniform(-40, 40) for _ in range(10)]

preys = [[preys_x[k], preys_y[k]] for k in range(len(preys_x))]

kdtree = KDTree(preys)

close_indices = kdtree.query_ball_point((0, 0), 30)
close_neighbours = [[preys_x[k], preys_y[k]] for k in close_indices]

print(len(close_neighbours))

plt.scatter(preys_x, preys_y, color='r', label='preys')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()