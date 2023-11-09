import numpy as np

class Predator():

    def __init__(self, window):
        self.x = np.random.randint(0, window[0])
        self.y = np.random.randint(0, window[1])
        self.vx = 0.8
        self.vy = 0.8
        self.visual_predation = 100
        self.direction = np.arctan2(self.vy, self.vx)

    def tracking_behaviour(self, kdtree, preys):
        speed_norm = np.sqrt(self.vx**2 + self.vy**2)
        
        visual_indices = kdtree.query_ball_point((self.x, self.y), self.visual_predation)
        
        if not visual_indices:
            # Aucune proie visible, déplacement aléatoire
            self.vx = self.vx + np.random.uniform(-0.1, 0.1)
            self.vy = self.vy + np.random.uniform(-0.1, 0.1)
        else:
            # Trouver la proie la plus proche
            closest_prey_index = min(visual_indices, key=lambda i: np.linalg.norm(np.array([preys[i].x, preys[i].y]) - np.array([self.x, self.y])))
            closest_prey = preys[closest_prey_index]
            
            # Calculer la direction vers la proie la plus proche
            direction = np.arctan2(closest_prey.y - self.y, closest_prey.x - self.x)

            # Mettre à jour la vitesse et la direction du prédateur
            self.vx = speed_norm * np.cos(direction)
            self.vy = speed_norm * np.sin(direction)

            self.direction = direction
            self.closest_prey = closest_prey

            self.centroid = [closest_prey.x, closest_prey.y]

    def potential_repulsion(self, window, turning_factor):
        
        if self.x != 0 and self.x != window[0]:
            self.ax = turning_factor*(1/(self.x**2) - 1/((self.x - window[0])**2))
        if self.y != 0 and self.y != window[1]:
            self.ay = turning_factor*(1/(self.y**2) - 1/((self.y - window[1])**2))
        if self.x < 0 or self.x > window[0]:
            self.vx = -self.vx
        if self.y < 0 or self.y > window[1]:
            self.vy = -self.vy


    def draw_triangle(self):
        center = (self.x, self.y)
        side_length = 8
        angle_radians = np.arctan2(self.vy, self.vx) + np.pi/2
        triangle = np.array([
            [-side_length / 2, side_length / 2],
            [side_length / 2, side_length / 2],
            [0, -side_length / 1]])
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]])
        rotated_triangle = np.dot(triangle, rotation_matrix.T) + center
        return [(int(point[0]), int(point[1])) for point in rotated_triangle]
    
    def speed_limit(self):
        v_max = 1
        v_min = 0.5
        vel_norm = np.sqrt(self.vx**2 + self.vy**2)        
        if vel_norm > v_max:
            self.vx = (self.vx/vel_norm)*v_max
            self.vy = (self.vy/vel_norm)*v_max
        if vel_norm < v_min:
            self.vx = (self.vx/vel_norm)*v_min
            self.vy = (self.vy/vel_norm)*v_min
        
    def uptate(self, window, turnfactor, kdtree, boids):

        self.tracking_behaviour(kdtree, boids)
        self.potential_repulsion(window, turnfactor)
        self.speed_limit()
        
        self.vx += self.ax
        self.vy += self.ay

        self.x += self.vx
        self.y += self.vy


if __name__ == "__main__":
    predator = Predator((1000,1000))
