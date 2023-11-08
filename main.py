from boids import Boid
from simulation import Simulation

time = 50
visual_range = 0
projected_range = 20
separation_factor = 0
alignment_factor = 0
cohesion_factor = 0
turnfactor = 0

if __name__ == "__main__":
    window = (800, 800)
    margin = 100
    boids = [Boid(window,margin) for _ in range(500)]
    simulation = Simulation(window, margin, 100)
    simulation.graphic_interface()
    simulation.update_animation(boids)
