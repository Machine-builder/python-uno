import pygame
from pygame.locals import *
from . import card_sprites, card_logic, utility


class hand(object):
    def __init__(self, cards: list = []):
        self.cards = cards
        self.current_upcard = 'y6'
        self.reset_card_offsets()

        self.display_y = 455

        self.action_queue = []
    
    def get_queue(self):
        aqc = self.action_queue.copy()
        self.action_queue = []
        return aqc

    def sort_cards(self):
        self.cards = card_logic.sort_cards(self.cards)

    def append_card(self, card_name):
        self.cards.append(card_name)
        self.reset_card_offsets()
        self.sort_cards()
    
    def set_cards(self, cards):
        self.cards = cards
        self.reset_card_offsets()
        self.sort_cards()

    def remove_card(self, card_name):
        self.cards.remove(card_name)
        self.reset_card_offsets()
        self.sort_cards()
    
    def set_upcard(self, upcard):
        self.current_upcard = upcard
        self.reset_card_offsets()

    def reset_card_offsets(self):
        self.lower_all_cards()
        self.card_offsets_real = [0]*len(self.get_playable_cards())
        self.scroll_x = 0
        self.scroll_x_real = 0

    def lower_all_cards(self):
        self.card_offsets = [0]*len(self.get_playable_cards())
    
    def get_playable_cards(self, stacked=0):
        return card_logic.playable_cards(self.cards,self.current_upcard,stacked)

    def get_card_positions(self, stacked=0):
        self.playable_cards = self.get_playable_cards(stacked)

        card_count = len(self.playable_cards)
        display_width = card_count*card_sprites.offset_2x[0]
        positions = []

        start_x = 400-display_width/2 + self.scroll_x_real
        for i, _ in enumerate(self.playable_cards):
            blit_x = start_x + card_sprites.offset_2x[0]*i
            positions.append(blit_x)

        return positions

    def mouse_click(self, position: tuple, button: int, stacked: int = 0):
        positions = self.get_card_positions(stacked)

        if button == 1:  # LMB
            clicked_index = -1
            for i, card_left in enumerate(positions):
                if position[0]>card_left and position[0]<card_left+card_sprites.size_2x[0]:
                    if position[1] > 458 and position[1] < 540:
                        clicked_index = i
                        break
            if clicked_index != -1:
                card_clicked=  self.playable_cards[clicked_index]
                self.action_queue.append(('click_card', card_clicked),)

    def update(self, deltatime: float, mouse_pos: tuple, keys_down: dict, stacked: int = 0):
        positions = self.get_card_positions(stacked)
        self.lower_all_cards()

        mouse_on_cards = mouse_pos[1] > self.display_y and mouse_pos[1] < self.display_y+card_sprites.size_2x[1]

        if len(positions) > 0:
            if mouse_on_cards:
                if mouse_pos[0] > positions[0] and mouse_pos[0] < positions[-1]+card_sprites.offset_2x[0]:
                    card_index = int(
                        (mouse_pos[0]-positions[0]) / card_sprites.offset_2x[0])
                    self.card_offsets[card_index] = 20

        for i, target_offset in enumerate(self.card_offsets):
            real_offset = self.card_offsets_real[i]
            diff = target_offset-real_offset
            self.card_offsets_real[i] += diff*deltatime*8
            if self.card_offsets_real[i] < 0.2:
                self.card_offsets_real[i] = 0
        
        if keys_down[K_a] or keys_down[K_LEFT]:
            self.scroll_x += 250*deltatime
        if keys_down[K_d] or keys_down[K_RIGHT]:
            self.scroll_x -= 250*deltatime

        if mouse_on_cards:
            scroll_area = 290
            scroll_left = (scroll_area - min(mouse_pos[0],scroll_area)) / scroll_area
            scroll_right = (max(mouse_pos[0]-(800-scroll_area),0)) / scroll_area
            mouse_scroll = scroll_left - scroll_right
            scroll_by = mouse_scroll*deltatime*700
            self.scroll_x += scroll_by
        
        scroll_min = -len(self.playable_cards)/2*card_sprites.offset_2x[0]+card_sprites.offset_2x[0]/2
        scroll_max = -scroll_min

        self.scroll_x = max(scroll_min, min(self.scroll_x, scroll_max))
        
        diff = self.scroll_x - self.scroll_x_real
        self.scroll_x_real += diff*deltatime*7

    def draw(self, display, your_turn=True, stacked=0):
        positions = self.get_card_positions(stacked)
        display_cards = self.get_playable_cards(stacked)

        display_at_y = 555
        other_cards = [card for card in self.cards if not card in display_cards]

        if your_turn:

            if len(display_cards) > 0:
                for i, card in enumerate(display_cards):
                    display.blit(
                        card_sprites.get_card(card, '2x'),
                        (positions[i], self.display_y-self.card_offsets_real[i])
                    )
            else:
                display_at_y = 450
        
        else:

            other_cards = self.cards
            display_at_y = 450
        
        rows = utility.chunks(other_cards, 23)
        for row_i, row in enumerate(rows):
            start_x = - len(row) / 2 * card_sprites.offset_1x[0]
            for i,card in enumerate(row):
                x_pos = 400 + start_x + i * card_sprites.offset_1x[0]
                display.blit(card_sprites.get_card(card, '1x'), (x_pos, display_at_y+row_i*10))

