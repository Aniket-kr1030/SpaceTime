import pygame
import math
from  particle import Particle
from button import Button
import random
class Simulation:
    def __init__(self, width, height, num_particles):
        pygame.init()
        self.width, self.height = width, height
        self.grid_color = (50, 50, 50)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Particle Simulation in Space-Time")
        self.background_color = (0, 0, 0)
        self.particle_color = (255, 255, 255)
        # Assuming a default mass for simplicity. Update this line to include mass.
        self.particles = [Particle(400+random.randrange(10,100), 300, 2, 1e+8) for i in range(num_particles)]  # Added mass=1
        self.speed_factor = 1  # Default speed factor
        self.buttons = [
            Button(650, 10, 100, 30, 'Speed x5'),
            Button(650, 50, 100, 30, 'Speed x10'),
            Button(650, 90, 100, 30, 'Speed x100')
        ]
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        grid_spacing = 50  # Space between grid lines
        for x in range(0, self.width, grid_spacing):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, grid_spacing):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

    def spawn_particle(self, x, y, mass=1e+3):
        # For simplicity, all particles have the same speed and mass
        self.particles.append(Particle(x, y, speed=0, mass=mass, vx = 0.5))

    def handle_button_click(self, pos):
        if self.buttons[0].is_over(pos):
            self.speed_factor = 5
        elif self.buttons[1].is_over(pos):
            self.speed_factor = 10
        elif self.buttons[2].is_over(pos):
            self.speed_factor = 100


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x < self.width - 150: 
                        self.spawn_particle(x, y)
                    else:
                        self.handle_button_click((x, y))

            self.screen.fill(self.background_color)
            self.draw_grid()

            # Update velocities based on gravitational effects
            for particle in self.particles:
                particle.update_velocity(self.particles)

            for button in self.buttons:
                button.draw(self.screen, self.font)

            # Check for and resolve collisions
            for i, particle in enumerate(self.particles):
                for other in self.particles[i+1:]:
                    if particle.check_collision(other):
                        particle.resolve_collision(other)

            # Move particles and draw them
            for particle in self.particles:
                particle.move()
                particle.draw(self.screen, self.particle_color)

            for _ in range(self.speed_factor):
                for particle in self.particles:
                    particle.update_velocity(self.particles, timestep=1 / self.speed_factor)
                for i, particle in enumerate(self.particles):
                    for other in self.particles[i+1:]:
                        if particle.check_collision(other):
                            particle.resolve_collision(other)
                for particle in self.particles:
                    particle.move()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


  