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

preys_x = [np.random.uniform(0, 40) for _ in range(100)]
preys_y = [np.random.uniform(0, 40) for _ in range(100)]

preys = [[preys_x[k], preys_y[k]] for k in range(len(preys_x))]

kdtree = KDTree(preys)

close_indices = kdtree.query_ball_point((0, 0), 30)
close_neighbours = [[preys_x[k], preys_y[k]] for k in close_indices]

centroid = np.mean(close_neighbours, axis=0)
direction = np.arctan2(centroid[1], centroid[0])

print("Direction to target: ", np.degrees(direction))

plt.scatter(preys_x, preys_y, color='r', label='preys')
plt.scatter(centroid[0], centroid[1], color='g', label='centroid')
plt.quiver(0, 0, 10*np.cos(direction), 10*np.sin(direction), angles='xy', scale_units='xy', scale=1, color='m', width=0.01)

plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.show()
