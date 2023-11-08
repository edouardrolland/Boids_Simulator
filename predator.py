import numpy as np

class Predator():

    def __init__(self, window):
        self.x = np.random.randint(0, window[0])
        self.y = np.random.randint(0, window[1])
        self.vx = 0.8
        self.vy = 0.8

    def random_walk(self):

        speed_norm = np.sqrt(self.vx**2 + self.vy**2)
        alpha = np.arctan2(self.vy, self.vx)
        new_alpha = alpha + np.random.uniform(-np.pi/4, np.pi/4)
        self.vx = np.cos(new_alpha) * speed_norm
        self.vy = np.sin(new_alpha) * speed_norm
    
    def potential_repulsion(self, window, turning_factor):

        if self.x != 0 and self.x != window[0]:
            self.ax = turning_factor*(1/(self.x**2) - 1/((self.x - window[0])**2))
        if self.y != 0 and self.y != window[1]:
            self.ay = turning_factor*(1/(self.y**2) - 1/((self.y - window[1])**2))

        if self.x < 0 or self.x > window[0]:
            self.vx = -self.vx
        if self.y < 0 or self.y > window[1]:
            self.vy = -self.vy

    def uptate(self, window, turnfactor):

        self.random_walk()
        self.potential_repulsion(window, turnfactor)
        
        self.vx += self.ax
        self.vy += self.ay

        self.x += self.vx
        self.y += self.vy


if __name__ == "__main__":
    predator = Predator((1000,1000))
