from boids import Boid
from simulation import Simulation

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

time = 50
visual_range = 0
projected_range = 20
separation_factor = 0
alignment_factor = 0
cohesion_factor = 0
turnfactor = 0

if __name__ == "__main__":
    
    window = (1000, 1000)
    margin = 200
    boids = [Boid(window,margin) for _ in range(30)]
    simulation = Simulation(window, margin, 100)
    simulation.graphic_interface()
    simulation.update_animation(boids)
