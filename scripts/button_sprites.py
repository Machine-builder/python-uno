import logging

import pygame
from pygame.locals import *

from . import image_loader

class button_sprites:
    arrow_left:pygame.Surface = None
    arrow_right:pygame.Surface = None

    main_customise:pygame.Surface = None
    main_join_game:pygame.Surface = None
    main_customise_A:pygame.Surface = None
    main_join_game_A:pygame.Surface = None

    text_customise:pygame.Surface = None

    button_left:pygame.Surface = None
    button_right:pygame.Surface = None
    button_left_A:pygame.Surface = None
    button_right_A:pygame.Surface = None

    pointer:pygame.Surface = None

    colour_r:pygame.Surface = None
    colour_g:pygame.Surface = None
    colour_y:pygame.Surface = None
    colour_b:pygame.Surface = None

    podium:pygame.Surface = None

    text_characters = []
    text_characters_2x = []

chars = 'abcdefghijklmnopqrstuvwxyz0123456789 +'

def draw_text(surface, top_left:tuple, text:str, size:str='1x', center_x:bool=False):
    xp = top_left[0]
    if center_x:
        xp -= get_text_width(text, size)/2
    from_l = button_sprites.text_characters
    if size == '2x':
        from_l = button_sprites.text_characters_2x
    for char in text.lower():
        if char in chars:
            text_char = from_l[chars.index(char)]
            surface.blit(text_char[1], (xp, top_left[1]))
            xp += text_char[0]+1

def get_text_width(text:str, size:str='1x'):
    from_l = button_sprites.text_characters
    if size == '2x':
        from_l = button_sprites.text_characters_2x
    text_width = 0
    for char in text.lower():
        if char in chars:
            text_char = from_l[chars.index(char)]
            text_width += text_char[0]+1
    text_width -= 1
    return text_width


def load_button_sprites():
    global button_sprites
    logging.debug('loading button sprites')
    sheet = image_loader.load_image('./resources/buttons.png')

    button_sprites.arrow_left = pygame.transform.scale(sheet.subsurface((1,1,28,43)), (56,86))
    button_sprites.arrow_right = pygame.transform.scale(sheet.subsurface((30,1,28,43)), (56,86))
    
    button_sprites.main_customise = pygame.transform.scale(sheet.subsurface((1,81,115,21)), (230,42))
    button_sprites.main_join_game = pygame.transform.scale(sheet.subsurface((1,103,115,21)),(230,42))
    button_sprites.main_customise_A = pygame.transform.scale(sheet.subsurface((117,81,115,21)), (230,42))
    button_sprites.main_join_game_A = pygame.transform.scale(sheet.subsurface((117,103,115,21)),(230,42))

    button_sprites.text_customise = pygame.transform.scale(sheet.subsurface((235,83,111,17)), (222,34))
    
    button_sprites.button_left = pygame.transform.scale(sheet.subsurface((105,1,24,19)), (48,38))
    button_sprites.button_right = pygame.transform.scale(sheet.subsurface((130,1,24,19)),(48,38))
    button_sprites.button_left_A = pygame.transform.scale(sheet.subsurface((105,21,24,19)), (48,38))
    button_sprites.button_right_A = pygame.transform.scale(sheet.subsurface((130,21,24,19)),(48,38))

    button_sprites.pointer = pygame.transform.scale(sheet.subsurface((59,18,15,21)),(60,84))
    
    button_sprites.colour_r = pygame.transform.scale(sheet.subsurface((164,59,16,21)),(64,84))
    button_sprites.colour_g = pygame.transform.scale(sheet.subsurface((181,59,16,21)),(64,84))
    button_sprites.colour_y = pygame.transform.scale(sheet.subsurface((198,59,16,21)),(64,84))
    button_sprites.colour_b = pygame.transform.scale(sheet.subsurface((215,59,16,21)),(64,84))
    
    button_sprites.podium = pygame.transform.scale(sheet.subsurface((1,125,34,31)),(136,124))

    # load text characters

    positions = []

    # letter bboxes

    # a, b, c, d, e, f, g, h
    for i in range(8):
        bbox = (1+12*i,45,11,17)
        positions.append(bbox)
    
    # i
    positions.append((97,45,9,17),)

    # j, k, l
    for i in range(3):
        bbox = (107+12*i,45,11,17)
        positions.append(bbox)

    # m
    positions.append((143,45,17,17),)

    # n, o, p
    for i in range(3):
        bbox = (1+12*i,63,11,17)
        positions.append(bbox)
    
    # q
    positions.append((37,63,12,17),)

    # r, s, t, u, v
    for i in range(5):
        bbox = (50+12*i,63,11,17)
        positions.append(bbox)

    # w
    positions.append((110,63,17,17),)

    # x, y, z
    for i in range(3):
        bbox = (128+12*i,63,11,17)
        positions.append(bbox)
    
    # number bboxes

    # 0
    positions.append((155,1,11,17),)
    # 1
    positions.append((167,1,5,17),)
    # 2, 3, 4, 5, 6, 7, 8, 9, space
    for i in range(9):
        positions.append((173+12*i,1,11,17),)
    
    # symbols

    # +
    positions.append((155,19,11,17),)


    for bbox in positions:
        letter_surf = sheet.subsurface(bbox)
        letter_size = letter_surf.get_size()
        sx, sy = letter_size
        button_sprites.text_characters.append((sx, letter_surf),)
        button_sprites.text_characters_2x.append((sx*2, pygame.transform.scale(letter_surf, (sx*2,sy*2))),)