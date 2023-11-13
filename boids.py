import numpy as np
from predator import Predator
import matplotlib.pyplot as plt

class Boid():

    def __init__(self, window, margin):

        angle = np.random.uniform(0, 2 * np.pi)
        r = np.random.randint(0, (margin)*0.2)
        self.x, self.y = (
            window[0]//2 + int(r * np.cos(angle)),
            window[0]//2 + int(r * np.sin(angle))
        )

        self.vx = 0.0
        self.vy = 0.05
        self.vx_prev = 0
        self.vy_prev = 0
        self.ax = 0
        self.ay = 0


    def potential_repulsion(self, window, turning_factor):

        if self.x != 0 and self.x != window[0]:
            self.ax = turning_factor*(1/(self.x**2) - 1/((self.x - window[0])**2))
        if self.y != 0 and self.y != window[1]:
            self.ay = turning_factor*(1/(self.y**2) - 1/((self.y - window[1])**2))
        if self.x < 0 or self.x > window[0]:
            self.vx = -self.vx
        if self.y < 0 or self.y > window[1]:
            self.vy = -self.vy

    def separation(self, close_neighbours):
        
        self.close_dx, self.close_dy = 0, 0
        total_close = 0

        for boid in close_neighbours:
            self.close_dx +=  - boid.x + self.x
            self.close_dy += - boid.y + self.y
            total_close += 1

        if total_close == 0:
            return np.array((0, 0))
        
        return np.array((self.close_dx, self.close_dy))/total_close
    
    def cohesion(self, visual_neighbours):
        x_avg, y_avg, total = 0, 0, 0

        for boid in visual_neighbours:
            x_avg += boid.x
            y_avg += boid.y
            total += 1
        
        if total > 0:
        
            x_avg /= total
            y_avg /= total
        else :
            return np.array((0, 0))
        return np.array((x_avg - self.x, y_avg - self.y))
    
    def alignment(self, visual_neighbours):
        vx_avg, vy_avg, total = 0, 0, 0

        for boid in visual_neighbours:
            vx_avg += boid.vx
            vy_avg += boid.vy
            total += 1
        if total > 0:
            vx_avg /= total
            vy_avg /= total
        else :
            return np.array((0, 0))
        return np.array((vx_avg - self.vx, vy_avg - self.vy))
    
    def random_vector(self):
        random_factor = 0.1
        ax = np.random.uniform(-random_factor, random_factor)
        ay = np.random.uniform(-random_factor, random_factor)
        return np.array((ax, ay))
    
    def predator_interaction(self, predator):

        predator_dx = predator.x - self.x #Positif si au dessus
        predator_dy = predator.y - self.y #Positif si à droite

        predator_dist = np.sqrt(predator_dx**2 + predator_dy**2)
        predatorturnfactor = 0.2

        if predator_dist < 50 : 
            if predator_dy > 0:  # predator above boid
                self.vy -= predatorturnfactor

            if predator_dy < 0:  # predator below boid
                self.vy += predatorturnfactor

            if predator_dx > 0:  # predator left of boid
                self.vx -= predatorturnfactor

            if predator_dx < 0:  # predator right of boid
                self.vx += predatorturnfactor

    def speed_limit(self):
        v_max = 1.32 #Based on the Impala's max speed, and scale calculations from the lenght of an impala.
        v_min = 0.1
        vel_norm = np.sqrt(self.vx**2 + self.vy**2)        
        if vel_norm > v_max:
            self.vx = (self.vx/vel_norm)*v_max
            self.vy = (self.vy/vel_norm)*v_max
        if vel_norm < v_min:
            self.vx = (self.vx/vel_norm)*v_min
            self.vy = (self.vy/vel_norm)*v_min

    def draw_triangle(self):

        center = (self.x, self.y)
        side_length = 6
        angle_radians = np.arctan2(self.vy, self.vx) + np.pi/2
        triangle = np.array([
            [-side_length / 2, side_length / 2],
            [side_length / 2, side_length / 2],
            [0, -side_length / 1]
        ])
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]
        ])
        rotated_triangle = np.dot(triangle, rotation_matrix.T) + center
        return [(int(point[0]), int(point[1])) for point in rotated_triangle]

    def update(self, window, turning_factor, separation_factor, cohesion_factor, alignment_factor,kd_tree, boids, visual_range, predator):
        
        self.potential_repulsion(window, turning_factor)
        close_indices = kd_tree.query_ball_point((self.x, self.y), 15)
        close_neighbours = [boids[i] for i in close_indices]

        self.ax += separation_factor * self.separation(close_neighbours)[0]
        self.ay += separation_factor * self.separation(close_neighbours)[1]

        visual_indices = kd_tree.query_ball_point((self.x, self.y), visual_range)
        visual_neighbours = [boids[i] for i in visual_indices]

        self.ax += cohesion_factor * self.cohesion(visual_neighbours)[0]
        self.ay += cohesion_factor * self.cohesion(visual_neighbours)[1]

        self.ax += alignment_factor * self.alignment(visual_neighbours)[0]
        self.ay += alignment_factor * self.alignment(visual_neighbours)[1]

        self.ax = self.ax + self.random_vector()[0]
        self.ay = self.ay + self.random_vector()[1]

        self.predator_interaction(predator)

        self.x += self.vx
        self.y += self.vy
        self.vx += self.ax
        self.vy += self.ay

        #Low pass filter to make the animals moving smoothlys
        alpha = 0.1
        self.vx = alpha * self.vx + (1-alpha)*self.vx_prev
        self.vy = alpha * self.vy + (1-alpha)*self.vy_prev
        self.vx_prev = self.vx
        self.vy_prev = self.vy

        self.speed_limit()

        