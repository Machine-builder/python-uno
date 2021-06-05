import pygame
from pygame.locals import *

from . import titles, button_sprites
from . import image_blit
from . import utility



def get_line(y=0,x=0):
    if x == 0:
        return (0,y), (800,y)
    return (x,0), (x,640)

def get_box(w=20,h=20,x=400,y=320):
    box = (x-w/2, y-h/2, w, h)
    return box



def draw_playing_screen(display):
    display.fill((245,245,245))

    # bottom gray box
    pygame.draw.rect(display,(210,210,210),(0,444,800,196))

    # top gray player box
    pygame.draw.rect(display,(210,210,210),(0,60,800,136))

    # titlebar line
    pygame.draw.line(display,(220,220,220),*get_line(y=60),3)

    # player area line
    pygame.draw.line(display,(220,220,220),*get_line(y=196),3)

    # card box
    pygame.draw.rect(display,(220,220,220),get_box(120,180,320,320),3)
    pygame.draw.rect(display,(220,220,220),get_box(120,180,480,320),3)

    pygame.draw.line(display,(220,220,220),*get_line(y=444),3)

    display.blit(titles.titles.main_title_uno, (365,11))



def draw_home_screen(display, mouse_pos:tuple=(-100,-100)):
    display.fill((245,245,245))

    # top gray player box
    pygame.draw.rect(display,(210,210,210),(0,60,800,240))

    # titlebar line
    pygame.draw.line(display,(220,220,220),*get_line(y=60),3)

    # player area line
    pygame.draw.line(display,(220,220,220),*get_line(y=300),3)

    # player sprite box
    # pygame.draw.rect(display,(220,220,220),get_box(120,180,y=180),3)

    display.blit(titles.titles.main_title_uno, (365,11))

    # if utility.point_in_box(mouse_pos, (285,319,515,361)):
    #     image_blit.blit_at_center(button_sprites.button_sprites.main_customise_A, display, (400,340))
    # else:
    #     image_blit.blit_at_center(button_sprites.button_sprites.main_customise, display, (400,340))
    
    if utility.point_in_box(mouse_pos, (285,319,515,361)):
        image_blit.blit_at_center(button_sprites.button_sprites.main_join_game_A, display, (400,340))
    else:
        image_blit.blit_at_center(button_sprites.button_sprites.main_join_game, display, (400,340))
    
    image_blit.blit_at_center(button_sprites.button_sprites.text_customise, display, (400,410))
    
    for y in (480,530,580):
        if utility.point_in_box(mouse_pos, (376-35,y-19,424-35,y+19)):
            image_blit.blit_at_center(button_sprites.button_sprites.button_left_A, display, (400-35,y))
        else:
            image_blit.blit_at_center(button_sprites.button_sprites.button_left, display, (400-35,y))
            
        if utility.point_in_box(mouse_pos, (376+35,y-19,424+35,y+19)):
            image_blit.blit_at_center(button_sprites.button_sprites.button_right_A, display, (400+35,y))
        else:
            image_blit.blit_at_center(button_sprites.button_sprites.button_right, display, (400+35,y))



def draw_ending_screen(display, mouse_pos:tuple=(-100,-100)):
    display.fill((245,245,245))

    # top gray player box
    pygame.draw.rect(display,(210,210,210),(0,60,800,-60 + 430))

    # titlebar line
    pygame.draw.line(display,(220,220,220),*get_line(y=60),3)

    # player area line
    pygame.draw.line(display,(220,220,220),*get_line(y=430),3)

    # player sprite box
    # pygame.draw.rect(display,(220,220,220),get_box(120,180,y=180),3)

    display.blit(titles.titles.main_title_uno, (365,11))