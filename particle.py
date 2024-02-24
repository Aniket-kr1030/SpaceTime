import math
import pygame
from numba import jit, njit

class Particle:
    def __init__(self, x, y, speed, mass, vx =0, vy =0):
        self.x = x
        self.y = y
        self.speed = speed
        self.mass = mass
        self.vx = vx  # Initial x velocity
        self.vy = vy  # Initial y velocity
        self.density = 100  # Average density of the sun in kg/m^3
        self.radius = self.calculate_radius()

    def calculate_radius(self):
        # Calculate volume from mass and density
        volume = self.mass / self.density
        # Calculate radius from volume of sphere
        radius = (3 * volume / (4 * math.pi)) ** (1/3)
        # Convert radius to pixels if necessary, for example, 1 meter = 1 pixel
        # You might need to scale this value to suit your simulation's visual scale
        return radius
    
    def check_collision(self, other):
        """Check if this particle collides with another."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Check if distance is less than sum of radii
        if distance < self.radius + other.radius:
            return True
        return False

    def resolve_collision(self, other):
        """Resolve collision between this particle and another by updating velocities for a perfectly elastic collision."""
        # Calculate the difference in positions
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normal vector
        nx = dx / distance
        ny = dy / distance
        
        # Tangent vector
        tx = -ny
        ty = nx
        
        # Dot Product Tangent
        dpTan1 = self.vx * tx + self.vy * ty
        dpTan2 = other.vx * tx + other.vy * ty
        
        # Dot Product Normal
        dpNorm1 = self.vx * nx + self.vy * ny
        dpNorm2 = other.vx * nx + other.vy * ny
        
        # Conservation of momentum in 1D
        m1 = (dpNorm1 * (self.mass - other.mass) + 2 * other.mass * dpNorm2) / (self.mass + other.mass)
        m2 = (dpNorm2 * (other.mass - self.mass) + 2 * self.mass * dpNorm1) / (self.mass + other.mass)
        
        m1 = 0.8 * m1
        m2 = 0.8* m2
        # Update velocities
        self.vx = tx * dpTan1 + nx * m1
        self.vy = ty * dpTan1 + ny * m1
        other.vx = tx * dpTan2 + nx * m2
        other.vy = ty * dpTan2 + ny * m2


    def update_velocity(self, particles, G=6.67430e-11, timestep=1):
        for particle in particles:
            if particle is not self:
                dx = particle.x - self.x
                dy = particle.y - self.y
                dx /= 100
                dy /= 100
                distance = math.sqrt(dx**2 + dy**2) + 1e-10  # Avoid division by zero
                force_direction = math.atan2(dy, dx)
                force = G * self.mass * particle.mass / distance**2
                # Update velocities based on this force
                self.vx += math.cos(force_direction) * force / self.mass * timestep
                self.vy += math.sin(force_direction) * force / self.mass * timestep

    def move(self):
        """Update particle position based on velocity."""
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen, color):
        # Draw the particle using its calculated radius
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.radius))
