import pygame
import math
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from particle import Particle, update_velocity, check_collision, resolve_collision
from button import Button

class Simulation:
    def __init__(self, width, height, num_particles):
        pygame.init()
        self.width, self.height = width, height
        self.grid_color = (50, 50, 50)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Particle Simulation in Space-Time")
        self.background_color = (0, 0, 0)
        self.particles = [Particle(400 + random.randrange(10, 100), 300, 2, 1e+13, 1e+9, (255, 255, 255), 1) for _ in range(num_particles)]
        self.speed_factor = 1
        self.buttons = [
            Button(650, 10, 100, 30, 'Speed x5'),
            # Other buttons...
        ]
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.paused = False
        self.show_grid = True
        self.executor = ThreadPoolExecutor()

    def draw_grid(self):
        if self.show_grid:
            grid_spacing = 50
            for x in range(0, self.width, grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
            for y in range(0, self.height, grid_spacing):
                pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

    def spawn_particle(self, x, y, mass=1e+10, density=1e+7, color=(255, 255, 255), size=1):
        self.particles.append(Particle(x, y, speed=0, mass=mass, density=density, color=color, size=size, vx=0.5))

    def remove_particle(self):
        if self.particles:
            self.particles.pop()

    def handle_button_click(self, pos):
        for button in self.buttons:
            if button.is_over(pos):
                if button.text == 'Speed x5':
                    self.speed_factor = 5
                elif button.text == 'Speed x10':
                    self.speed_factor = 10
                elif button.text == 'Speed x100':
                    self.speed_factor = 100
                elif button.text == 'Pause':
                    self.paused = True
                elif button.text == 'Resume':
                    self.paused = False
                elif button.text == 'Add Particle':
                    x, y = pygame.mouse.get_pos()
                    self.spawn_particle(x, y)
                elif button.text == 'Remove Particle':
                    self.remove_particle()
                elif button.text == 'Change Background':
                    self.background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif button.text == 'Toggle Grid':
                    self.show_grid = not self.show_grid
                break

    def update_particles(self):
        positions = np.array([particle.pos for particle in self.particles])
        velocities = np.array([particle.vel for particle in self.particles])
        masses = np.array([particle.mass for particle in self.particles])

        def update_particle(i):
            other_particles = [(positions[j], masses[j]) for j in range(len(self.particles)) if j != i]
            if len(other_particles) > 0:
                velocities[i] = update_velocity(positions[i], velocities[i], masses[i], other_particles, G=6.67430e-11, timestep=1)

        def resolve_collisions(i, j):
            if check_collision(positions[i], positions[j], self.particles[i].radius, self.particles[j].radius):
                velocities[i], velocities[j] = resolve_collision(positions[i], positions[j], velocities[i], velocities[j], masses[i], masses[j])

        futures = [self.executor.submit(update_particle, i) for i in range(len(self.particles))]
        [future.result() for future in futures]

        futures = [self.executor.submit(resolve_collisions, i, j) for i in range(len(self.particles)) for j in range(i + 1, len(self.particles))]
        [future.result() for future in futures]

        for i, particle in enumerate(self.particles):
            particle.pos = positions[i]
            particle.vel = velocities[i]
            particle.move(self.width, self.height)

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

            if not self.paused and len(self.particles) > 0:
                self.update_particles()

            for particle in self.particles:
                particle.draw(self.screen)

            for button in self.buttons:
                button.draw(self.screen, self.font)

            num_particles_text = self.font.render(f"Particles: {len(self.particles)}", True, (255, 255, 255))
            speed_text = self.font.render(f"Speed: x{self.speed_factor}", True, (255, 255, 255))
            self.screen.blit(num_particles_text, (10, 10))
            self.screen.blit(speed_text, (10, 40))

            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()