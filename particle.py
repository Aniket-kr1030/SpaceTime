import math
import pygame
import numpy as np
from numba import jit

@jit(nopython=True)
def calculate_radius(mass, density, size):
    volume = mass / density
    radius = (3 * volume / (4 * math.pi)) ** (1/3)
    return radius * size

@jit(nopython=True)
def check_collision(pos1, pos2, radius1, radius2):
    dr = pos1 - pos2
    distance = np.sqrt(np.sum(dr**2))
    return distance < radius1 + radius2

@jit(nopython=True)
def resolve_collision(pos1, pos2, vel1, vel2, mass1, mass2):
    dr = pos1 - pos2
    distance = np.sqrt(np.sum(dr**2))
    n = dr / distance
    t = np.array([-n[1], n[0]])

    dpTan1 = vel1[0] * t[0] + vel1[1] * t[1]
    dpTan2 = vel2[0] * t[0] + vel2[1] * t[1]

    dpNorm1 = vel1[0] * n[0] + vel1[1] * n[1]
    dpNorm2 = vel2[0] * n[0] + vel2[1] * n[1]

    m1 = (dpNorm1 * (mass1 - mass2) + 2 * mass2 * dpNorm2) / (mass1 + mass2)
    m2 = (dpNorm2 * (mass2 - mass1) + 2 * mass1 * dpNorm1) / (mass1 + mass2)

    m1 = m1 * 0.7
    m2 = m2 * 0.7

    dpTan1 = dpTan1 * 0.7
    dpTan1 = dpTan1 * 0.7

    vel1 = t * dpTan1 + n * m1
    vel2 = t * dpTan2 + n * m2

    return vel1, vel2

@jit(nopython=True)
def update_velocity(pos, vel, mass, particles, G, timestep):
    force = np.zeros(2)
    for particle in particles:
        if not np.array_equal(particle[0], pos):
            dr = particle[0] - pos
            distance = np.sqrt(np.sum(dr**2))
            force += G * mass * particle[1] / (distance**2) * dr / distance
    vel += force / mass * timestep
    return vel

class Particle:
    def __init__(self, x, y, speed, mass, density, color, size, vx=0, vy=0):
        self.pos = np.array([x, y], dtype=float)
        self.speed = speed
        self.mass = mass
        self.density = density
        self.color = color
        self.size = size
        self.vel = np.array([vx, vy], dtype=float)
        self.radius = calculate_radius(self.mass, self.density, self.size)

    def move(self, width, height):
        self.pos += self.vel
        if self.pos[0] <= self.radius or self.pos[0] >= width - self.radius:
            self.vel[0] = -self.vel[0]
        if self.pos[1] <= self.radius or self.pos[1] >= height - self.radius:
            self.vel[1] = -self.vel[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), int(self.radius))