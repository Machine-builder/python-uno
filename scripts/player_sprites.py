import logging

import pygame
from pygame.locals import *

from . import image_loader

sprites = {}

def load_player_sprites():
    logging.debug('loading player sprites')
    sheet_surf = image_loader.load_image('./resources/player.png')

    sub_sheets = [
        ('faces', (32,4), (18,22), (10,3), (-1,-1,-1,-3)),
        ('bodies', (32,77), (18,16), (10,1), (0,0,-3,0)),
        ('cards', (33,98), (29,44), (6,1), (0,0,-1,-1))
    ]

    for sheet in sub_sheets:
        name, top_left, step, size, adjust = sheet
        index = 0
        sprites[name] = []
        for y in range(size[1]):
            for x in range(size[0]):
                index += 1
                index_str = str(index).rjust(2,'0')
                px = top_left[0] + x*step[0]
                py = top_left[1] + y*step[1]
                surf = sheet_surf.subsurface(
                    (px+adjust[0],
                     py+adjust[1],
                     step[0]+adjust[2],
                     step[1]+adjust[3]))
                cursize = surf.get_size()
                sprites[name].append(pygame.transform.scale(surf, (cursize[0]*2, cursize[1]*2)))

def create_player_card(face:int, body:int, card:int):
    main_surf = sprites['cards'][card].copy()
    main_surf.blit(sprites['faces'][face], (11,8))
    main_surf.blit(sprites['bodies'][body], (13,42))
    return main_surf