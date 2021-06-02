from . import card_logic


class UnoPlayer():
    def __init__(self):
        self.hand = []


class UnoGame():
    def __init__(self):
        # create a shuffled uno deck
        self.deck = card_logic.make_deck()

        self.players = []
        self.players_turn = 0
        self.turn_direction = 1

        self.upfacing_card = None

        self.debug = False

        self.stacked_plus = 0

        self.winner = None
    
    def debug_msg(self, msg=''):
        if self.debug:
            print(msg)

    def start_game(self, players: int = 5, hand_size: int = 7):
        """start a game and deal hands"""
        _ = self.deal_hands(players, hand_size)
        while 1:
            if self.upfacing_card is not None:
                self.put_card(self.upfacing_card)
            self.upfacing_card = self.take_card()
            if self.upfacing_card is not None:
                if self.upfacing_card[0] != '_' and not self.upfacing_card[1] in 'srp':
                    break

    def deal_hands(self, players: int = 5, size: int = 7):
        """deals cards from the deck to players
        returns a list of lists representing each player's hand,
        also saves UnoPlayer instances in .players attribute"""
        if players*size > len(self.deck):
            size = int(len(self.deck)/players)
        hands = []
        for i in range(players):
            hand = []
            for j in range(size):
                hand.append(self.take_card())
            hands.append(hand)
            new_player = UnoPlayer()
            new_player.hand = hand
            self.players.append(new_player)
        return hands

    def take_card(self, card=None) -> str:
        """get the top card off the deck, or a specific card from the deck"""
        if card is None:
            return self.deck.pop(0)[:2]
        self.deck.remove(card)

    def put_card(self, card):
        """put a card into the end of the deck"""
        self.deck.append(card)
    
    def take_turn(self, player_index: int, turn: tuple) -> bool:
        """let a player take a turn
        turn[0] can be either 'play' or 'pickup'
        if turn[0] is 'play', turn[1] must be the card name"""

        if 0 > player_index >= len(self.players):
            # player does not exist
            return False
        if not turn[0] in ('play', 'pickup'):
            # turn not valid
            return False
        if turn[0] == 'play' and len(turn) != 2:
            # no card name provided with 'play' turn
            return False
        
        player_obj = self.players[player_index]

        print(f'[{player_index}] : {turn}')

        if turn[0] == 'play':
            card_name = card_logic.real_card_name(turn[1])
            if not card_name in player_obj.hand:
                # player doesn't have card
                return False
            if not card_logic.card_playable(card_name, self.upfacing_card):
                # card not playable
                return False

            card_type = card_logic.card_type(card_name)

            used_plus = False
            is_special = card_type == 'special'
            if is_special:
                if card_name[1] == 'p': # a plus card
                    plus_count = 2
                    if card_name[0] == '_':
                        plus_count = 4
                    self.stacked_plus += plus_count
                    used_plus = True
            
            if used_plus or self.stacked_plus==0:
                self.put_card(self.upfacing_card)
                self.upfacing_card = turn[1]
                player_obj.hand.remove(card_name)

                if is_special:
                    if card_name[1] == 's': # a skip card
                        self.players_turn += self.turn_direction
                    elif card_name[1] == 'r': # a reverse card
                        self.turn_direction *= -1

            else:
                for i in range(self.stacked_plus):
                    player_obj.hand.append(self.take_card())
                self.stacked_plus = 0
            
            self.players_turn += self.turn_direction
            self.players_turn %= len(self.players)

            return True
        
        elif turn[0] == 'pickup':
            if self.stacked_plus == 0:
                top_card = self.take_card()
                player_obj.hand.append(top_card)
            else:
                for i in range(self.stacked_plus):
                    player_obj.hand.append(self.take_card())
                self.stacked_plus = 0
            
            self.players_turn += self.turn_direction
            self.players_turn %= len(self.players)
            
            return True
        
    def check_winner(self):
        for player in self.players:
            if len(player.hand) == 0:
                self.winner = player
                return True
        return False