import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np  # pip install numpy
pygame.init()

time = 50
visual_range = 0
projected_range = 20

separation_factor = 0
alignment_factor = 0
cohesion_factor = 0

window = (1000, 1000)
margin = 100
turnfactor = 0


class Boid():

    def __init__(self):

        self.x = np.random.randint(0, window[0])
        self.y = np.random.randint(0, window[1])
        self.vx = float(round(np.random.uniform(-2, 2), 1))
        self.vy = float(round(np.random.uniform(-2, 2), 1))

        self.max_speed = 15
        self.min_speed = 1

    def avoid_edge(self):

        if self.x < 0 or self.x > window[0]:
            self.vx = -self.vx
        if self.y < 0 or self.y > window[1]:
            self.vy = -self.vy

        if self.x < margin:
            self.vx += turnfactor
        if self.x > window[0] - margin:
            self.vx -= turnfactor

        if self.y < margin:
            self.vy += turnfactor

        if self.y > window[1] - margin:
            self.vy -= turnfactor

    def distance_between_boids(self, boid):
        dx = self.x - boid.x
        dy = self.y - boid.y
        return np.sqrt(dx**2 + dy**2)

    def separation(self):

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

        for boid in boids:

            if self.distance_between_boids(boid) < projected_range:

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
            self.vx = np.sign(self.vy) * 0.8

        if np.abs(self.vy) < 0.5:
            self.vy = np.sign(self.vy) * 0.8

    def update(self, time):

        self.separation()
        self.avoid_edge()
        self.speed_limit()
        self.x = self.x + self.vx
        self.y = self.y + self.vy


screen = pygame.display.set_mode(window)
pygame.display.set_caption("Predator Prey Simulation")


boids = [Boid() for _ in range(200)]
clock = pygame.time.Clock()  # create pygame clock object

x_slider = 80 + margin



separation_slider = Slider(screen, x_slider, int(margin/6), int(window[0]/8), int(window[1]/120), min=0, max=0.5, step=0.001, color=(0, 0, 0), handleColour=(255, 0, 0), handleRadius=5, initial=0, handleThickness=0)
alignment_slider = Slider(screen, x_slider, int(margin/6) + int(window[1]/120) + 10, int(window[0]/8), int(
    window[1]/120), min=0, max=0.5, step=0.001, color=(0, 0, 0), handleColour=(255, 0, 0), handleRadius=5, initial=0, handleThickness=0)
cohesion_slider = Slider(screen, x_slider, int(margin/6) + 2*int(window[1]/120) + 20, int(window[0]/8), int(
    window[1]/120), min=0, max=0.5, step=0.001, color=(0, 0, 0), handleColour=(255, 0, 0), handleRadius=5, initial=0, handleThickness=0)
turning_slider = Slider(screen, x_slider, int(margin/6) + 3*int(window[1]/120) + 30, int(window[0]/8), int(
    window[1]/120), min=0, max=1, step=0.001, color=(0, 0, 0), handleColour=(255, 0, 0), handleRadius=5, initial=0, handleThickness=0)
visual_slider = Slider(screen, x_slider, int(margin/6) + 4*int(window[1]/120) + 40, int(window[0]/8), int(
    window[1]/120), min=0, max=200, step=1, color=(0, 0, 0), handleColour=(255, 0, 0), handleRadius=5, initial=0, handleThickness=0)

output_separation = TextBox(screen, int(margin/2) + int(window[0]/4) + 20, int(margin/6) - int(window[1]/120) + 2, 35, 20, fontSize=15, borderColour=(
    255, 255, 255), textColour=(0, 0, 0), radius=0, text=str(np.around(separation_slider.getValue(), 3)))

output_alignment = TextBox(screen, int(margin/2) + int(window[0]/4) + 20, int(margin/6) + int(window[1]/120) + 4, 35, 20, fontSize=15, borderColour=(
    255, 255, 255), textColour=(0, 0, 0), radius=0, text=str(np.around(alignment_slider.getValue(), 3)))

output_cohesion = TextBox(screen, int(margin/2) + int(window[0]/4) + 20, int(margin/6) + 2*int(window[1]/120) + 15, 35, 20, fontSize=15, borderColour=(
    255, 255, 255), textColour=(0, 0, 0), radius=0, text=str(np.around(cohesion_slider.getValue(), 3)))
output_turning = TextBox(screen, int(margin/2) + int(window[0]/4) + 20, int(margin/6) + 3*int(window[1]/120) + 24, 35, 20, fontSize=15, borderColour=(
    255, 255, 255), textColour=(0, 0, 0), radius=0, text=str(np.around(turning_slider.getValue(), 3)))
output_visual = TextBox(screen, int(margin/2) + int(window[0]/4) + 20, int(margin/6) + 4*int(window[1]/120) + 34, 35, 20, fontSize=15, borderColour=(
    255, 255, 255), textColour=(0, 0, 0), radius=0, text=str(np.around(visual_slider.getValue(), 3)))

output_separation.disable()  # Act as label instead of textbox
output_alignment.disable()  # Act as label instead of textbox
output_cohesion.disable()  # Act as label instead of textbox
output_turning.disable()  # Act as label instead of textbox
output_visual.disable()  # Act as label instead of textbox

font = pygame.font.Font(None, 18)  # Create a font object


while True:

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, 'black', (margin, margin,
                     window[0] - 2*margin, window[1] - 2*margin))
    pygame.draw.rect(screen, 'white', (margin + 2, margin + 2,
                     window[0] - 2*margin - 4, window[1] - 2*margin - 4))
    # Legends
    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color

    text = font.render("Separation", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6)-2))

    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color
    text = font.render("Separation", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6)-2))
    separation_factor = separation_slider.getValue()

    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color
    text = font.render("Alignment", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6)-2 + int(window[1]/120) + 10))
    alignment_factor = alignment_slider.getValue()

    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color
    text = font.render("Cohesion", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6) + 2*int(window[1]/120) + 18))
    cohesion_factor = cohesion_slider.getValue()

    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color
    text = font.render("Turning", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6) + 2*int(window[1]/120) + 36))
    turnfactor = turning_slider.getValue()

    # Replace "Your Text Here" with the text you want to display and (255, 255, 255) with the text color
    text = font.render("Visual", True, (0, 0, 0))
    screen.blit(text, (margin, int(margin/6) + 2*int(window[1]/120) + 54))
    visual_range = visual_slider.getValue()
    

    for boid in boids:
        pygame.draw.circle(screen, 'red', (boid.x, boid.y), 3)
        boid.update(time)

    for events in pygame.event.get():  # loop through all events
        if events.type == pygame.QUIT:
            pygame.quit()
            quit()

    output_separation.setText(np.around(separation_slider.getValue(),3))
    output_alignment.setText(np.around(alignment_slider.getValue(), 3))
    output_cohesion.setText(np.around(cohesion_slider.getValue(), 3))
    output_turning.setText(np.around(turning_slider.getValue(),3))
    output_visual.setText(np.around(visual_slider.getValue(),3))

    pygame_widgets.update(events)
    pygame.display.update()  # update display
    clock.tick(time)  # maintain 50 fps
