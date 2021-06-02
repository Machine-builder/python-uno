import pygame
from pygame.locals import *

def blit_at_center(image, background, position=(400,320)):
    w,h = image.get_size()
    top_left = (position[0]-w/2, position[1]-h/2)
    background.blit(image, top_left)