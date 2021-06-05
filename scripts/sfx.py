
import pygame
from pygame.locals import *
pygame.init()
pygame.mixer.init()

click_down = pygame.mixer.Sound('./resources/sfx/click_down.mp3')
click_up = pygame.mixer.Sound('./resources/sfx/click_up.mp3')

end_win = pygame.mixer.Sound('./resources/sfx/end_win.mp3')
end_lose = pygame.mixer.Sound('./resources/sfx/end_lose.mp3')

clapping = pygame.mixer.Sound('./resources/sfx/clapping.mp3')