from . import card_logic
import random

def play(hand, stacked:int):
    playable_cards = hand.get_playable_cards(stacked)

    if len(playable_cards) == 0:
        return ('pickup',)

    else:

        plus_cards = [c for c in playable_cards if (c[1] == 'p' and c[0] != '_')]

        if len(plus_cards) > 0:
            return ('play', plus_cards[0])
        
        colour_counts = [[colour] for colour in 'rgyb']
        for index,colour in enumerate(colour_counts):
            this_colour = [c for c in playable_cards if c[0] == colour[0]]
            colour_counts[index].append(len(this_colour))
        
        sorted_colours = sorted(colour_counts, key=lambda x: x[1])
        most_colours = sorted_colours[-1][0]

        if '_w' in playable_cards:
            return ('play','_w'+most_colours)
        
        if '_p' in playable_cards:
            return ('play','_p'+most_colours)

        common_card = [c for c in playable_cards if c[0] == most_colours][0]

        return ('play', common_card)