import logging

import pygame
from pygame.locals import *

import random

class Particle(object):
    def __init__(self):
        self.position = [0,0]
        self.velocity = [0,0]
        self.lifetime = random.uniform(1,2)
        self.max_lifetime = self.lifetime
        self.colour = random.choice([
            (242, 27, 27), (31, 240, 94), (27, 142, 242), (252, 249, 43)
        ])
    
    def update(self, dt:float):
        self.lifetime -= dt
        self.position[0] += self.velocity[0]*dt
        self.position[1] += self.velocity[1]*dt
        self.velocity[1] += 9.8*dt *25
        return self.lifetime > 0
    
    def draw(self, surface):
        radius = int(self.lifetime/self.max_lifetime * 8)+1
        pygame.draw.circle(surface, self.colour, tuple([int(i) for i in self.position]), int(radius))

class ParticleManager(object):
    def __init__(self):
        self.particles = []
    
    def update(self, dt:float):
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def draw(self, surface):
        draw_ret = [p.draw(surface) for p in self.particles]