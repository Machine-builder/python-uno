import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import logging

logging.basicConfig(
    filename='./data/player.log',
    filemode='w',
    format='%(levelname)s %(message)s',
    level=logging.INFO)

logging.debug("importing pygame")

import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

logging.debug("importing scripts")

from scripts import image_blit
from scripts import card_sprites
from scripts import interfaces
from scripts import hand_display
from scripts import card_logic
from scripts import utility
from scripts import player_sprites
from scripts import button_sprites
from scripts import cosmetics
from scripts import sfx

import math
import time
import random

logging.debug("import ebsocket connections")
from ebsockets import connections
ebs_event = connections.ebsocket_event


logging.debug("running connection init")
client = connections.ebsocket_client()

ip = input("ip >>> ") or connections.utility.get_local_ip()
port = int(input("port >>> ") or 7982)

print(f"Connecting to {ip}:{port}")
client.connect_to((ip, port))

logging.debug(f"connected to {ip}:{port}")


colour_x_positions = (299,366,434,501)

screen_size = (800, 640)
display_size = (600, 440)
screen = pygame.Surface(screen_size)
display = pygame.display.set_mode(display_size, pygame.RESIZABLE)
pygame.display.set_caption('Uno')

screen_ratio = [screen_size[x]/display_size[x] for x in (0,1)]

clock = pygame.time.Clock()

particle_manager = cosmetics.ParticleManager()


menu_state = 'home'
menu_timer = -1

your_hand = hand_display.hand([],)
upcard = '_u'
your_hand.set_upcard(upcard)
your_turn = False
stacked_plus = 0

playing_wild = None
colour_offsets = [0,0,0,0]
colour_offsets_t = [0,0,0,0]

winner_was_you = False
winner_index = 0

class player_settings:
    sprite = None
    ftc = [0,0,0]

def update_player_sprite():
    global player_settings
    f,t,c = player_settings.ftc
    sprite = pygame.transform.scale(player_sprites.create_player_card(f,t,c), (112,172))
    player_settings.sprite = sprite
    with open('./data/player_ftc.txt', 'w') as ftc_file:
        ftc_file.write(f'{f} {t} {c}')

class other_player_sprites:
    sprites = []
    ftcs = []
    card_counts = []

def update_other_player_sprites(all_ftcs, own_index):
    global other_player_sprites
    indices_list = list(range(len(all_ftcs)))
    top_order = [all_ftcs[own_index]] + all_ftcs[own_index+1:] + all_ftcs[:own_index]
    top_order_i = [indices_list[own_index]] + indices_list[own_index+1:] + indices_list[:own_index]
    other_player_sprites.sprites = []
    other_player_sprites.ftcs = all_ftcs
    for i,ftc in enumerate(top_order):
        sprite = player_sprites.create_player_card(*ftc)
        other_player_sprites.sprites.append((top_order_i[i], sprite),)
    
def update_card_counts(counts):
    global other_player_sprites
    other_player_sprites.card_counts = counts

players_turn = 0

def reset_all_globals():
    global your_hand, upcard, your_turn
    global stacked_plus, playing_wild
    global other_player_sprites, players_turn
    global winner_was_you, winner_index
    global particle_manager, play_delay
    your_hand = hand_display.hand([],)
    upcard = '_u'
    your_hand.set_upcard(upcard)
    your_turn = False
    stacked_plus = 0
    playing_wild = None
    other_player_sprites.sprites = []
    other_player_sprites.ftcs = []
    other_player_sprites.card_counts = []
    players_turn = 0
    winner_was_you = False
    winner_index = 0
    particle_manager.particles = []


try:
    with open('./data/player_ftc.txt', 'r') as ftc_file:
        f,t,c = [int(x) for x in ftc_file.readline().strip().split(' ',2)]
except:
    with open('./data/player_ftc.txt', 'w') as ftc_file:
        ftc_file.write('0 0 0')
    f,t,c = 0,0,0

player_settings.ftc = [f,t,c]
update_player_sprite()


running = True
while running:

    dt = clock.tick(66)/1000
    mouse_pos_display = pygame.mouse.get_pos()
    mouse_pos = (
        mouse_pos_display[0] * screen_ratio[0],
        mouse_pos_display[1] * screen_ratio[1]
    )

    ct = time.time()
    ct_sin = math.sin(ct*6)

    new_events, connected = client.pump()
    if not connected: break


    pygame_events = pygame.event.get()

    for event in pygame_events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            display_size = (event.w, event.h)
            display = pygame.display.set_mode(display_size, pygame.RESIZABLE)
            screen_ratio = [screen_size[x]/display_size[x] for x in (0,1)]
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Channel(0).play(sfx.click_down)

            for i in range(random.randint(8,10)):
                new_particle = cosmetics.Particle()
                new_particle.velocity[0] = random.uniform(-1,1)*65
                new_particle.velocity[1] = random.uniform(-1,-0.1)*95
                new_particle.position = list(mouse_pos)
                new_particle.colour = [random.randint(125,190)]*3
                particle_manager.particles.append(new_particle)
            
        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.mixer.Channel(0).play(sfx.click_up)


    # run different event loops based on what menu is open


    if menu_state == 'home':
        for event in pygame_events:            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_settings.ftc[0] = random.randint(1,len(player_sprites.sprites['faces']))-1
                    player_settings.ftc[1] = random.randint(1,len(player_sprites.sprites['bodies']))-1
                    player_settings.ftc[2] = random.randint(1,len(player_sprites.sprites['cards']))-1
                    update_player_sprite()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicks = []
                    for y in (480,530,580):
                        clicks.append((
                            utility.point_in_box(mouse_pos, (376-35,y-19,424-35,y+19)),
                            utility.point_in_box(mouse_pos, (376+35,y-19,424+35,y+19))
                        ),)
                    if len([x for x in clicks if True in x]) > 0:
                        for i in range(3):
                            if clicks[i][0]: player_settings.ftc[i] -= 1
                            if clicks[i][1]: player_settings.ftc[i] += 1
                        player_settings.ftc[0] %= len(player_sprites.sprites['faces'])
                        player_settings.ftc[1] %= len(player_sprites.sprites['bodies'])
                        player_settings.ftc[2] %= len(player_sprites.sprites['cards'])
                        update_player_sprite()

                    if utility.point_in_box(mouse_pos, (285,319,515,361)):
                        client.send_event(ebs_event('join', player_ftc=player_settings.ftc))
                        menu_state = 'playing'

        interfaces.draw_home_screen(screen, mouse_pos)
        image_blit.blit_at_center(player_settings.sprite, screen, (400,180))


    elif menu_state == 'playing':
        turn_taken = (None,)

        hover_card_stack = utility.point_in_box(mouse_pos, (420,230,540,410))

        for event in pygame_events:            
            if event.type == pygame.MOUSEBUTTONUP:
                your_hand.mouse_click(mouse_pos, event.button, stacked_plus)
                
                if your_turn:
                    if playing_wild is None:
                        if hover_card_stack:
                            turn_taken = ('pickup',)
                
                    else:
                        for i,x in enumerate(colour_x_positions,):
                            if x-32<mouse_pos[0]<x+32 and 410-42<mouse_pos[1]<410+42:
                                card = playing_wild+'rgyb'[i]
                                turn = ('play', card)
                                client.send_event(ebs_event('play', turn=turn))
                                playing_wild = None
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if playing_wild is not None:
                        playing_wild = None
        
        keys_down = pygame.key.get_pressed()

        if your_turn and playing_wild is None:
            your_hand.update(dt, mouse_pos, keys_down, stacked_plus)
        
        if not your_hand and playing_wild is not None:
            playing_wild = None

        for action in your_hand.get_queue():
            if action[0] == 'click_card':
                turn_taken = ('play', action[1])
        
        if turn_taken[0] is not None:
            if turn_taken[0] == 'play':
                if turn_taken[1][0] == '_':
                    playing_wild = turn_taken[1]
                    print(f'playing wild : {playing_wild}')
            if playing_wild is None:
                print('send turn to server :', turn_taken)
                client.send_event(ebs_event('play', turn=turn_taken))
                if turn_taken[0] == 'play':
                    card_name = card_logic.real_card_name(turn_taken[1])
                    your_hand.remove_card(card_name)
                your_turn = False

        for event in new_events:
            print(event, event.__dict__)
            if event.event == 'set_player_sprites':
                own_index = event.own_index
                all_ftcs = event.all_ftcs
                update_other_player_sprites(all_ftcs, own_index)
            if event.event == 'update_hand':
                cards = event.cards
                your_hand.set_cards(cards)
            if event.event == 'set_upcard':
                upcard = event.card
                your_hand.set_upcard(upcard)
            if event.event == 'your_turn':
                your_turn = event.value
            if event.event == 'set_stacked':
                stacked_plus = event.stacked
            if event.event == 'set_player_turn':
                players_turn = event.turn
            if event.event == 'set_card_counts':
                card_counts = event.counts
                update_card_counts(card_counts)
            if event.event == 'winner':
                winner_index = event.index
                winner_was_you = event.is_you
                print(f'A player has won the game: {winner_index}')
                menu_state = 'podium'
                menu_timer = 6
                if winner_was_you:
                    pygame.mixer.Channel(1).play(sfx.end_win)
                    pygame.mixer.Channel(2).play(sfx.clapping)
                else:
                    pygame.mixer.Channel(1).play(sfx.end_lose)
            if event.event == 'force_menu':
                menu_state = 'force_menu'
        
        interfaces.draw_playing_screen(screen)
        image_blit.blit_at_center(card_sprites.card_sprites_4x[card_logic.real_card_name(upcard)], screen, (320,320))
        image_blit.blit_at_center(card_sprites.card_sprites_4x['_u'], screen, (480,320))

        if your_turn and playing_wild is None:
            # draw a pointer hand telling player to pick up card
            playable_count = len(card_logic.playable_cards(your_hand.cards,
                your_hand.current_upcard, stacked_plus))
            if playable_count == 0 or hover_card_stack:
                image_blit.blit_at_center(button_sprites.button_sprites.pointer, screen, (480,390+ct_sin*6))
        
        if stacked_plus > 0:
            button_sprites.draw_text(screen, (261,375), f'+{stacked_plus}', '2x')

        # draw other player sprites
        # and evenly space them in the top bar
        spacing = 100
        center_x = 400
        xp = center_x - (len(other_player_sprites.sprites)-1)/2*spacing
        for index, sprite in other_player_sprites.sprites:
            yp = 120
            if index == players_turn:
                yp += ct_sin*5
            # blit their sprite surface
            image_blit.blit_at_center(sprite, screen, (xp,yp))

            # calculate how to display their card count
            card_count = min(other_player_sprites.card_counts[index],10)
            a = 14 if card_count>1 else 28
            b = (28/(card_count-1)) if card_count > 1 else 0
            card_xp = xp-28+a
            card_yp = yp+56
            for i in range(card_count):
                image_blit.blit_at_center(card_sprites.get_card('_u'),
                screen, (card_xp,card_yp))
                card_xp += b

            xp += spacing

        if playing_wild is None:
            your_hand.draw(screen, your_turn, stacked_plus)

        if playing_wild is not None:
            your_hand.draw(screen, your_turn, stacked_plus)
            # draw colour buttons
            image_blit.blit_at_center(card_sprites.card_sprites_4x[card_logic.real_card_name(playing_wild)], screen, (400,270))

            for i,x in enumerate(colour_x_positions,):
                colour_sprite = button_sprites.button_sprites.colour_r
                if i == 1: colour_sprite = button_sprites.button_sprites.colour_g
                elif i == 2: colour_sprite = button_sprites.button_sprites.colour_y
                elif i == 3: colour_sprite = button_sprites.button_sprites.colour_b

                image_blit.blit_at_center(colour_sprite, screen, (x,410-colour_offsets[i]))

                colour_offsets_t[i] = 0
                if x-32<mouse_pos[0]<x+32 and 410-42<mouse_pos[1]<410+42:
                    colour_offsets_t[i] = 15
                
                diff = colour_offsets_t[i] - colour_offsets[i]
                colour_offsets[i] += diff*dt*10

    elif menu_state == 'podium':
        menu_timer -= dt
        
        interfaces.draw_ending_screen(screen, mouse_pos)

        image_blit.blit_at_center(button_sprites.button_sprites.podium, screen, (400,340))
        winner_sprite = [s[1] for s in other_player_sprites.sprites if s[0]==winner_index][0]
        image_blit.blit_at_center(
            pygame.transform.scale(winner_sprite, (112,172)),
            screen, (400,180))
        
        button_sprites.draw_text(screen,
            (400,450), 'you won' if winner_was_you else 'you lost', '2x', True)
        
        button_sprites.draw_text(screen,
            (400,520), f'continuing in {int(menu_timer)} seconds', '2x', True)
        
        if random.random() < 0.3:
            new_particle = cosmetics.Particle()
            new_particle.velocity[0] = random.uniform(0.7,1) * 350
            new_particle.velocity[1] = random.uniform(-1,0) * 100
            new_particle.position[0] = -15
            new_particle.position[1] = random.randint(25,85)
            particle_manager.particles.append(new_particle)
        if random.random() < 0.3:
            new_particle = cosmetics.Particle()
            new_particle.velocity[0] = -random.uniform(0.7,1) * 350
            new_particle.velocity[1] = random.uniform(-1,0) * 100
            new_particle.position[0] = 815
            new_particle.position[1] = random.randint(25,85)
            particle_manager.particles.append(new_particle)

        if menu_timer <= 0:
            menu_state = 'home'
            menu_timer = -1
            reset_all_globals()
    

    elif menu_state == 'force_menu':
        reset_all_globals()
        menu_state = 'home'
    
    particle_manager.update(dt)
    particle_manager.draw(screen)

    display.blit(pygame.transform.smoothscale(screen, display_size), (0,0))
    pygame.display.flip()


pygame.quit()
print("Connection closed by server or disconnect")