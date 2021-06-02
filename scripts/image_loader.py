import logging
import pygame

def load_image(filepath:str):
    try:
        return pygame.image.load(filepath)
    except:
        logging.error(f'failed to load image from {filepath}')
        return None