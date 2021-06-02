import random


def sort_cards(cards_list):
    cards_r = sorted([c for c in cards_list if c[0] == 'r'])
    cards_g = sorted([c for c in cards_list if c[0] == 'g'])
    cards_y = sorted([c for c in cards_list if c[0] == 'y'])
    cards_b = sorted([c for c in cards_list if c[0] == 'b'])
    cards__ = sorted([c for c in cards_list if c[0] == '_'])

    return cards_r+cards_g+cards_y+cards_b+cards__


def card_playable(card, upcard, plus_stack: int = 0) -> bool:
    if plus_stack == 0:
        if card[0] == upcard[0] != '_':
            return True
        if card[1] == upcard[1] and upcard[0] != '_':
            return True
        if len(upcard) == 3:
            # card was a wild or +4 and the colour was picked to be [2]
            if card[0] == upcard[2]:
                return True
        if card[0] == '_':
            # card is colour pick, so they can do whatever
            return True
    else:
        if card[1] == 'p' and card[0] != '_' and upcard[0] != '_':
            return True
        if card[1] == 'p' and card[0] == upcard[0] == '_':
            return True
    return False


def card_type(card):
    if card[1] in 'prs':
        return 'special'
    return 'normal'


def real_card_name(card):
    return card[:2]


def playable_cards(cards_list, upcard, plus_stack: int = 0):
    return [card for card in cards_list if card_playable(card, upcard, plus_stack)]


def random_card():
    return random.choice('rgyb')+random.choice('1234567890rsp')


def make_deck():
    base_deck = [
        'r0', 'r1', 'r1', 'r2', 'r2', 'r3', 'r3', 'r4', 'r4', 'r5', 'r5', 'r6', 'r6', 'r7', 'r7', 'r8', 'r8', 'r9', 'r9', 'rp', 'rp', 'rr', 'rr', 'rs', 'rs',
        'g0', 'g1', 'g1', 'g2', 'g2', 'g3', 'g3', 'g4', 'g4', 'g5', 'g5', 'g6', 'g6', 'g7', 'g7', 'g8', 'g8', 'g9', 'g9', 'gp', 'gp', 'gr', 'gr', 'gs', 'gs',
        'y0', 'y1', 'y1', 'y2', 'y2', 'y3', 'y3', 'y4', 'y4', 'y5', 'y5', 'y6', 'y6', 'y7', 'y7', 'y8', 'y8', 'y9', 'y9', 'yp', 'yp', 'yr', 'yr', 'ys', 'ys',
        'b0', 'b1', 'b1', 'b2', 'b2', 'b3', 'b3', 'b4', 'b4', 'b5', 'b5', 'b6', 'b6', 'b7', 'b7', 'b8', 'b8', 'b9', 'b9', 'bp', 'bp', 'br', 'br', 'bs', 'bs',
        '_w', '_w', '_w', '_w', '_p', '_p', '_p', '_p'
    ]
    random.shuffle(base_deck)
    return base_deck
