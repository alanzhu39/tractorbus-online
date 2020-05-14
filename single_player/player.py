"""
Keep track of:
player's hand
"""


class Player(object):
    """
    name = Player's name (string)
    trump_rank = trump rank (string)
    trump_suit = trump suit (string)
    is_zhuang_jia = (True if player is zhuang jia, False otherwise) (boolean)
    is_attacker = (True if player is an attacker, False otherwise) (boolean)
    hand = list of cards in player's hand (list of Card objects)
    """
    def __init__(self, name, trump_rank, trump_suit='spades', is_zhuang_jia=False, is_attacker=False, hand=[]):
        self.name = name
        self.is_zhuang_jia = is_zhuang_jia
        self.hand = hand[:]
        self.trump_suit = trump_suit
        self.is_attacker = is_attacker
        self.trump_rank = trump_rank

    def __str__(self):
        return self.name + " " + str(self.is_zhuang_jia) + " " + str(self.hand)

    def get_name(self):
        return self.name

    def get_trump_suit(self):
        return self.trump_suit

    def get_trump_rank(self):
        return self.trump_rank

    def get_hand(self):
        return self.hand

    def set_name(self, name):
        self.name = name

    def set_trump_suit(self, trump_suit):
        self.trump_suit = trump_suit

    def set_trump_rank(self, trump_rank):
        self.trump_rank = trump_rank

    def set_is_zhuang_jia(self, is_zhuang_jia):
        self.is_zhuang_jia = is_zhuang_jia

    def set_hand(self, hand):
        self.hand = hand

    def set_is_attacker(self, is_attacker):
        self.is_attacker = is_attacker

    def get_hand_size(self):
        return len(self.hand)

    def print_hand(self):
        for i in range(len(self.hand)):
            print(str(i) + ':' + str(self.hand[i]), end=' ')
        print()


    def draw(self, card):
        # draws a card and inserts into hand
        inserted = False
        for i in range(len(self.hand)):
            if card_cmp(card, self.hand[i], self.trump_suit, self.trump_rank) >= 0:
                self.hand.insert(i, card)
                inserted = True
                break
        if not inserted:
            self.hand.append(card)

    def sort(self):
        new_hand = []
        for card in self.hand:
            for i in range(len(new_hand)):
                if card_cmp(card, new_hand[i], self.trump_suit, self.trump_rank) >= 0:
                    new_hand.insert(i, card)
                    break
        self.hand = new_hand[:]

    # number of occurrences of the given card in hand
    def card_count(self, card):
        res = 0
        for c in self.hand:
            if c == card:
                res += 1
        return res

    def play(self, card):
        self.hand.remove(card)


# comparator for cards in the player's hand. This compares cards based on suit to order them in the player's hand.
def card_cmp(card1, card2, trump_suit, trump_rank):
    if card1 == card2:
        return 0
    if card1.is_big_joker:
        return 1
    if card2.is_big_joker:
        return -1
    if card1.is_small_joker:
        return 1
    if card2.is_small_joker:
        return -1
    if card1.rank == trump_rank and card1.suit == trump_suit:
        return 1
    if card2.rank == trump_rank and card2.suit == trump_suit:
        return -1
    if card1.rank == trump_rank and card2.rank == trump_rank:
        return 0
    if card1.rank == trump_rank:
        return 1
    if card2.rank == trump_rank:
        return -1

    suit_dict = {'clubs': 1, 'diamonds': 2, 'hearts': 3, 'spades': 4, trump_suit: 5}
    rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                 'K': 13, 'A': 14, trump_rank: 15}
    if suit_dict[card1.suit] > suit_dict[card2.suit]:
        return 1
    elif suit_dict[card1.suit] < suit_dict[card2.suit]:
        return -1
    else:
        if rank_dict[card1.rank] > rank_dict[card2.rank]:
            return 1
        else:
            return -1
