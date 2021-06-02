import logging

import pygame
from pygame.locals import *

from . import image_loader

card_names = [
    'r1','r2','r3','r4','r5','r6','r7','r8','r9','r0','rs','rr','rp',
    'g1','g2','g3','g4','g5','g6','g7','g8','g9','g0','gs','gr','gp',
    'y1','y2','y3','y4','y5','y6','y7','y8','y9','y0','ys','yr','yp',
    'b1','b2','b3','b4','b5','b6','b7','b8','b9','b0','bs','br','bp',
    '_w','_p','_u'
]
card_sprites_1x = {card_name:None for card_name in card_names}
card_sprites_2x = {card_name:None for card_name in card_names}
card_sprites_4x = {card_name:None for card_name in card_names}

card_size = (29,44)

size_1x = (card_size[0]*1, card_size[1]*1)
offset_1x = (size_1x[0]+4, size_1x[1]+4)

size_2x = (card_size[0]*2, card_size[1]*2)
offset_2x = (size_2x[0]+4, size_2x[1]+4)

size_4x = (card_size[0]*4, card_size[1]*4)
offset_4x = (size_4x[0]+4, size_4x[1]+4)

def get_card(card_name, size='1x'):
    r_card_name = card_name[:2]
    from_dict = card_sprites_1x
    if size=='2x': from_dict = card_sprites_2x
    elif size=='4x': from_dict = card_sprites_4x
    return from_dict[r_card_name]

def load_cards():
    logging.debug('loading cards')
    sheet = image_loader.load_image('./resources/cards.png')
    index = -1
    for y in range(5):
        for x in range(13):
            pixel = (x*card_size[0], y*card_size[1])
            if sheet.get_at(pixel) == (88,88,88):
                index += 1
                rect = (pixel[0]+1, pixel[1]+1, card_size[0]-1, card_size[1]-1)
                individual_card_sprite = sheet.subsurface(rect)
                card_sprites_1x[card_names[index]] = individual_card_sprite.copy()
                card_sprites_2x[card_names[index]] = pygame.transform.scale(individual_card_sprite.copy(), ((card_size[0]-1)*2, (card_size[1]-1)*2))
                card_sprites_4x[card_names[index]] = pygame.transform.scale(individual_card_sprite.copy(), ((card_size[0]-1)*4, (card_size[1]-1)*4))