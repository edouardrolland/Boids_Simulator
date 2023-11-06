import pygame
import math
import numpy as np

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 400, 400

# Création de la fenêtre
screen = pygame.display.set_mode((width, height))

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)

# Centre du triangle
center = (200, 200)

# Longueur des côtés du triangle
side_length = 50

# Angle de rotation en degrés (par exemple, 45 degrés)
angle_degrees = 180

# Convertir l'angle en radians
angle_radians = math.radians(angle_degrees)

# Sommets du triangle
triangle = np.array([
    [-side_length / 2, side_length / 2],
    [side_length / 2, side_length / 2],
    [0, -side_length / 2]
])

# Matrice de rotation
rotation_matrix = np.array([
    [math.cos(angle_radians), -math.sin(angle_radians)],
    [math.sin(angle_radians), math.cos(angle_radians)]
])

# Appliquer la rotation en utilisant la multiplication de matrices
rotated_triangle = np.dot(triangle, rotation_matrix.T) + center

triangle_points = [(int(point[0]), int(point[1])) for point in rotated_triangle]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Efface l'écran
    screen.fill(white)

    # Dessine le triangle
    pygame.draw.polygon(screen, black, triangle_points)

    # Met à jour l'écran
    pygame.display.flip()

# Quitte Pygame
pygame.quit()
