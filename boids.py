import numpy as np
import pygame
from scipy.spatial import KDTree


class Boid():

    def __init__(self, window, margin):
        
        self.prev_vx = 0
        self.prev_vy = 0

        self.x = np.random.randint(0, window[0])
        self.y = np.random.randint(0, window[1])
        self.vx = float(round(np.random.uniform(-2, 2), 1))
        self.vy = float(round(np.random.uniform(-2, 2), 1))
        self.max_speed = 15
        self.min_speed = 1
        self.window = window
        self.margin = margin

    def avoid_edge(self, turnfactor):

        # Bouncing Behaviour
        if self.x < 0 or self.x > self.window[0]:
            self.vx = -self.vx
        if self.y < 0 or self.y > self.window[1]:
            self.vy = -self.vy

        # Repulsive Behaviour
        if self.x < self.margin:
            self.vx = self.vx + turnfactor

        if self.x > self.window[0] - self.margin:
            self.vx = self.vx - turnfactor

        if self.y < self.margin:
            self.vy += turnfactor

        if self.y > self.window[1] - self.margin:
            self.vy -= turnfactor
        
    def distance_between_boids(self, boid):
        dx = self.x - boid.x
        dy = self.y - boid.y
        return np.sqrt(dx**2 + dy**2)

    def behaviour(self, boids, separation_factor, alignment_factor, cohesion_factor, visual_range, kdtree):
        # Separation
        self.close_dx = 0
        self.close_dy = 0

        # Alignment
        self.xvel_avg = 0
        self.yvel_avg = 0
        self.neighboring_boids = 0

        # Cohesion
        self.xpos_avg = 0
        self.ypos_avg = 0
        
        within_radius_indices = kdtree.query_ball_point((self.x, self.y), visual_range)
        close_boids = [boids[i] for i in within_radius_indices]

        for boid in close_boids:

            if self.distance_between_boids(boid) < 8:
                self.close_dx += self.x - boid.x
                self.close_dy += self.y - boid.y

            if self.distance_between_boids(boid) < visual_range:
                self.xvel_avg += boid.vx
                self.yvel_avg += boid.vy
                self.neighboring_boids += 1
                self.xpos_avg += boid.x
                self.ypos_avg += boid.y

        if self.neighboring_boids > 0:

            self.xpos_avg = self.xpos_avg/self.neighboring_boids
            self.ypos_avg = self.ypos_avg/self.neighboring_boids
            self.xvel_avg = self.xvel_avg/self.neighboring_boids
            self.yvel_avg = self.yvel_avg/self.neighboring_boids

        else:
            self.xpos_avg = self.x
            self.ypos_avg = self.y
            self.xvel_avg = self.vx
            self.yvel_avg = self.vy

        self.vx += self.close_dx * separation_factor + \
            (self.xvel_avg - self.vx) * alignment_factor + \
            (self.xpos_avg - self.x) * cohesion_factor
        self.vy += self.close_dy * separation_factor + \
            (self.yvel_avg - self.vy) * alignment_factor + \
            (self.ypos_avg - self.y) * cohesion_factor

    def speed_limit(self):

        if np.abs(self.vx) > 2.5:
            self.vx = self.vx/np.abs(self.vx) * 2.5

        if np.abs(self.vy) > 2.5:
            self.vy = self.vy/np.abs(self.vy) * 2.5

        if np.abs(self.vx) < 0.5:
            self.vx = np.sign(self.vx) * 0.8

        if np.abs(self.vy) < 0.5:
            self.vy = np.sign(self.vy) * 0.8

    def update_velocity(self):
        
        self.current_angle = np.arctan2(self.prev_vy, self.prev_vx)
        self.new_angle = np.arctan2(self.vy, self.vx)
        
        self.angle_diff = self.new_angle - self.current_angle

        max_val = 0.2

        if self.angle_diff > max_val:
            print("coucou")
            self.vx = self.prev_vx * np.cos(max_val)
            self.vy = self.prev_vy * np.sin(max_val)
        else:
            None


    def update(self, boids, separation_factor, alignment_factor, cohesion_factor, visual_range, turnfactor, kdtree):

        self.behaviour(boids, separation_factor, alignment_factor, cohesion_factor, visual_range, kdtree)
        self.avoid_edge(turnfactor)
        self.update_velocity()
        self.speed_limit()
        

        self.x = self.x + self.vx*0.5
        self.y = self.y + self.vy*0.5

        self.prev_vx = self.vx
        self.prev_vy = self.vy

if __name__ == "__main__":

    window = (1000, 1000)
    visual_range = 20
    projected_range = 10
    boid = Boid(window, visual_range)

    boids = [Boid(window, visual_range) for _ in range(100)]
    data_points = [(boid.x, boid.y) for boid in boids]

    boids_array = [list(point) for point in data_points]

    kdtree = KDTree(data_array)

    points_within_radius_indices = kdtree.query_ball_point(query_point, radius)

    # Access the objects corresponding to the indices
    objects_within_radius = [data_objects[i] for i in points_within_radius_indices]