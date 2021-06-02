import logging

import pygame
from pygame.locals import *

from . import image_loader

class titles:
    main_title_uno:pygame.Surface = None

def load_titles():
    global titles
    logging.debug('loading titles')
    sheet = image_loader.load_image('./resources/titles.png')

    titles.main_title_uno = pygame.transform.scale(sheet.subsurface((1,1,35,17)), (70,34))