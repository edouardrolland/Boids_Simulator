from scipy.spatial import KDTree

# Sample data
data_points = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
data_objects = ['A', 'B', 'C', 'D', 'E']  # Corresponding objects in the same order

# Convert data_points to a 2D array of coordinates
data_array = [list(point) for point in data_points]

# Create a KD-tree
kdtree = KDTree(data_array)

# Query for a single nearest neighbor
query_point = (9, 10)
nearest_neighbor_distance, nearest_neighbor_index = kdtree.query(query_point, k=1)

# Access the object corresponding to the nearest neighbor
nearest_neighbor_object = data_objects[nearest_neighbor_index]

# Print the result
print("Nearest neighbor distance:", nearest_neighbor_distance)
print("Nearest neighbor object:", nearest_neighbor_object)

print(data_array)
