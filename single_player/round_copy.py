"""
Keep track of:
everyone's cards
current Zhuang Jia
Zhuang Jia discard
current trump
current attacker's points

also play the round:
dealing, compare cards, and playing
"""
from typing import Dict, Any

from single_player.deck import *
# import single_player.pim_copy as pim

connections = []

class testRound(object):
    """
    players = list of Player (size = 4) (list of Player object)
    zhuang_jia_id = ID of zhuang jia in players (int)
    set_zhuang_jia = True if there is a zhuang jia at the start of the round (boolean)
    trump_suit = trump suit (string)
    trump_suit_cnt = number of cards used to liang the trump suit (exceptions: 0 if no liang and 3 if wu zhu)
    trump_rank = rank of trump card
    suit_played = suit of first card played (the suit that everyone must follow)
    discards = list of discarded cards by zhuang jia
    attacker_points = # points attackers collected
    """
    num_di_pai = 8
    global connections

    def __init__(self, players):
        self.deck = Deck()
        assert (len(players) == 4)
        self.players = players

        # find ID of zhuang jia, set_zhuang_jia is True if someone is zhuang jia
        self.set_zhuang_jia = False
        for i in range(len(players)):
            if players[i].is_zhuang_jia:
                self.zhuang_jia_id = i
                self.set_zhuang_jia = True

        self.trump_suit = "none"
        self.trump_suit_cnt = 0
        self.trump_rank = players[self.zhuang_jia_id].get_trump_rank()  # assumes there is a zhuang jia
        self.suit_played = "none"
        self.discards = []
        self.attacker_points = 0
        self.current_player = 5
        self.cards_played = {0: [], 1: [], 2: [], 3: []}
        self.clear = False
        self.di_pai = True
        self.game_start = False
        self.client_input = ''
        # assumes there is a zhuang jia
        print("Round starting: " + players[self.zhuang_jia_id].get_name()
              + " is zhuang jia and the trump rank is " + self.trump_rank)

    # returns number of points attackers earned
    def play_round(self):
        self.game_start = True
        self.deal()
        # todo implement trump ranking (depends on trump rank and trump suit)
        # play out the turns
        # pass in trump info as a dictionary
        info = self.play_turn(self.zhuang_jia_id)
        self.clear = True
        while len(self.players[0].get_hand()) > 0:
            # todo need id of player starting next turn
            # assumes that play_turn return an info dictionary
            trick_winner = info['trick_winner']
            self.current_player = trick_winner
            info = self.play_turn(trick_winner)

        # reveal di pai and add to attacker's points if necessary
        attacker_multiplier = 2 * info['num_cards']
        if (info['trick_winner'] == self.zhuang_jia_id) or (info['trick_winner'] == (self.zhuang_jia_id + 2) % 4):
            attacker_multiplier = 0

        di_pai_points = 0
        print("Di pai: ", end='')
        for card in self.discards:
            di_pai_points += card.point_value
            print(card, end=' ')
        print('')

        if attacker_multiplier > 0:
            print("Attackers won the last trick, adding %d * %d = %d points."
                  % (attacker_multiplier, di_pai_points, attacker_multiplier * di_pai_points))
            self.attacker_points += attacker_multiplier * di_pai_points

        return self.attacker_points

    def deal(self):
        self.deck.shuffle()
        current_drawer = self.zhuang_jia_id
        while len(self.deck) > self.num_di_pai:
            self.players[current_drawer].draw(self.deck.pop())
            print(self.players[current_drawer].name)
            self.players[current_drawer].print_hand()
            # self.liang_query(current_drawer)
            current_drawer = (current_drawer + 1) % 4
        # no liang -> flip di pai
        if self.trump_suit == "none":
            self.flip_di_pai()
        for i in range(len(self.players)):
            self.players[i].hand.sort(key = self.view_value, reverse = True)
        # zhuang jia chooses 8 cards for di pai
        self.choose_di_pai()

    def liang_query(self, current_drawer):
        # format is "suit cnt" or "SJo 2" or "BJo 2"
        print("Liang?")
        response = input().split()
        # "n" "no" or nothing means no liang
        if len(response) == 0 or response[0] == "n" or response[0] == "no":
            print("No liang, continuing")
            return
        # check for validity of the response
        if len(response) != 2:
            print("invalid response, continuing")
            return
        if response[1] != "1" and response[1] != "2":
            print("invalid response, continuing")
            return
        if (response[0] == "SJo" or response[0] == "BJo") and response[1] == "2":
            # wu zhu liang
            new_trump_suit = "wu zhu"
            new_trump_suit_cnt = 3
        elif response[0] in Card.suit_map:
            # other liang
            new_trump_suit = response[0]
            new_trump_suit_cnt = int(response[1])
        else:
            print("invalid response, continuing")
            return

        # check whether the liang is valid
        if response[0] == "SJo":
            card_to_check = SMALL_JOKER
            cnt_to_check = 2
        elif response[0] == "BJo":
            card_to_check = BIG_JOKER
            cnt_to_check = 2
        else:
            card_to_check = Card(self.players[0].get_trump_rank(), new_trump_suit)
            cnt_to_check = new_trump_suit_cnt

        if self.players[current_drawer].card_count(card_to_check) >= cnt_to_check:
            if new_trump_suit_cnt > self.trump_suit_cnt:
                print("Set trump suit to: " + new_trump_suit)
                self.trump_suit = new_trump_suit
                self.trump_suit_cnt = new_trump_suit_cnt
            else:
                print("You don't have the cards necessary for that liang")
        else:
            print("You don't have the cards necessary for that liang")

    def card_value(self, card):
        """
        Returns a relative value of the card.
        Lowest card in a suit is 1, second lowest is 2, etc... highest (usually A) is 12 because one rank is trump
        All cards of trump suit and not in the top 12 will have 100 added to signify trump
        ex: trump_rank == 4, trump_suit == spades
        2d: 1 3d: 2 5d: 3 ... 10d: 8 Jd: 9 Qd: 10 Kd: 11 Ad: 12
        2s: 101 3s: 102 5s: 103 10s: 108 Js: 109 Qs: 110 Ks: 111 As: 112 4d: 113 4c: 113 4s: 114 SJo: 115 BJo: 116

        ex: trump_rank == 4, trump_suit == "none" (wuzhu)
        2d: 1 3d: 2 5d: 3 ... Ad: 12
        4c: 114 4d: 114 4h: 114 4s: 114 SJo: 115 BJo: 116

        :param card:
        :return: int
        """
        trump_rank = self.trump_rank
        trump_suit = self.trump_suit
        if card.is_big_joker:
            return 116
        elif card.is_small_joker:
            return 115
        card_suit = card.get_suit()
        card_rank = card.get_rank()
        if card_rank == trump_rank:
            if card_suit == trump_suit or trump_suit == "none":
                return 114
            else:
                return 113
        rank_dict = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11,
                     'K': 12, 'A': 13}
        temp_card_value = rank_dict[card_rank]
        if temp_card_value > rank_dict[trump_rank]:
            temp_card_value -= 1
        if self.is_trump(card):
            temp_card_value += 100
        return temp_card_value

    def view_value(self, card):
        card_value = self.card_value(card)
        suit_order = {
            'diamonds': 0,
            'clubs': 1,
            'hearts': 2,
            'spades': 3
        }
        r_suit_order = {
            0: 'diamonds',
            1: 'clubs',
            2: 'hearts',
            3: 'spades'
        }
        if self.trump_suit == 'none':
            if self.get_suit(card) == 'trump':
                return 400+card_value
            else:
                if self.get_suit(card) == 'diamonds':
                    return 300+card_value
                if self.get_suit(card) == 'clubs':
                    return 200+card_value
                if self.get_suit(card) == 'hearts':
                    return 100+card_value
                return card_value
        else:
            trump_suit = self.trump_suit
            suit_index = suit_order[trump_suit]
            if self.get_suit(card) == 'trump':
                return 400+card_value
            for i in range(suit_index, suit_index+4):
                c_index = i % 4
                if self.get_suit(card) == r_suit_order[c_index]:
                    return 100*(4-(i-suit_index)) + card_value

    def cmp_cards(self, a, b):
        # Compares cards in game, with consideration to the first card played
        # returns 1 if a>b, 0 if a=b, and -1 if a<b
        if a == b:
            return 0
        if a.is_big_joker:
            return 1
        if b.is_big_joker:
            return -1
        if a.is_small_joker:
            return 1
        if b.is_small_joker:
            return -1
        if a.rank == self.trump_rank and a.suit == self.trump_suit:
            return 1
        if b.rank == self.trump_rank and b.suit == self.trump_suit:
            return -1
        if a.rank == self.trump_rank and b.rank == self.trump_rank:
            return 0
        if a.rank == self.trump_rank:
            return 1
        if b.rank == self.trump_rank:
            return -1

        suit_dict = {'clubs': 1, 'diamonds': 2, 'hearts': 3, 'spades': 4, self.suit_played: 5, self.trump_suit: 6}
        rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                     'K': 13, 'A': 14, self.trump_rank: 15}
        if suit_dict[a.suit] > suit_dict[b.suit]:
            return 1
        elif suit_dict[a.suit] < suit_dict[b.suit]:
            return -1
        else:
            if rank_dict[a.rank] > rank_dict[b.rank]:
                return 1
            else:
                return -1

    def flip_di_pai(self):
        # Flips cards from di pai until the trump rank or joker is hit, and sets the trump suit accordingly
        # Otherwise makes the largest card the trump rank
        print("No liang, flipping di pai...")
        largest_rank_suit = "none"
        largest_rank = 1
        rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                     'K': 13, 'A': 14}
        for card in self.deck.cards:
            print(card)
            if card.is_big_joker or card.is_small_joker:
                self.trump_suit = "none"
                print("The game is now WuZhu")
                return
            elif card.rank == self.trump_rank:
                self.trump_suit = card.suit
                print("The trump suit is now %s" % card.suit)
                return
            else:
                if rank_dict[card.rank] > largest_rank:
                    largest_rank_suit = card.suit
        self.trump_suit = largest_rank_suit
        print("The trump suit is now %s" % self.trump_suit)
        return

    def choose_di_pai(self):
        zhuang_jia_player = self.players[self.zhuang_jia_id]
        self.current_player = self.zhuang_jia_id
        for card in self.deck.cards:
            zhuang_jia_player.draw(card)
        self.di_pai = False
        print(zhuang_jia_player.get_name() + ". Your hand after di pai:")
        zhuang_jia_player.print_hand()
        print("The trump suit is " + self.trump_suit)
        while len(self.discards) != 8:
            print("Enter 8 indexes you want to discard:")
            discard_indexes = self.get_player_input(self.zhuang_jia_id)
            if not len(discard_indexes) == 8 or not self.is_valid_input(zhuang_jia_player, discard_indexes):
                continue
            else:
                self.current_player = 5
                self.client_input = ''
                break
        # ADDS DISCARDS TO SELF.DISCARDS, DELETES CARDS FROM PLAYER HAND
        for each_index in discard_indexes:
            self.discards.append(zhuang_jia_player.get_hand()[each_index])
        self.di_pai = True
        self.del_indexes(zhuang_jia_player, discard_indexes)

        '''
            print("Enter the card that you want to discard. Or, enter \'undo\' to return "
                  "a card from the discard to your hand")
            card_input = pim.get_player_input()
            if card_input.lower() == 'undo':
                print("Enter the card that you want to return to your hand")
                if card_input == "BJo":
                    discard_card = Card('2', 's', is_big_joker=True)
                elif card_input == "SJo":
                    discard_card = Card('2', 's', is_small_joker=True)
                else:
                    discard_card = Card(card_input[:-1], card_input[-1])
                self.discards.remove(discard_card)
            elif pim.is_card(card_input):
                if card_input == "BJo":
                    discard_card = Card('2', 's', is_big_joker=True)
                elif card_input == "SJo":
                    discard_card = Card('2', 's', is_small_joker=True)
                else:
                    discard_card = Card(card_input[:-1], card_input[-1])
                self.discards.append(discard_card)
            else:
                print("Not a valid input. Please enter a valid input")
        for card in self.discards:
            self.players[self.zhuang_jia_id].play(card)
            '''

    def get_trump_info(self):
        trump_info = {
            'suit': str(self.trump_suit),
            'rank': str(self.trump_rank)
        }
        return trump_info

    def is_trump(self, card):
        trump_info = self.get_trump_info()
        if card.get_is_joker():
            return True
        if card.get_suit() == trump_info['suit']:
            return True
        if card.get_rank() == trump_info['rank']:
            return True
        return False

    def get_suit(self, card):
        if self.is_trump(card):
            return "trump"
        else:
            return card.get_suit()

    # returns true if pair1 played greater than pair2
    def pair_gt(self, pair1, pair2):
        if pair1.get_suit() == 'trump' and pair2.get_suit() != 'trump':
            return True
        elif pair2.suit == pair2.get_suit():
            if self.cmp_cards(pair1.get_card(), pair2.get_card()) == 1:
                return True
        else:
            return False

    # FINDS A PAIR ON PRECONDITION THAT ENTIRE HAND IS OF ONE SUIT
    def contains_pair(self, hand):
        suit = self.get_suit(hand[0])
        return self.contains_pair_in_suit(hand, suit)

    # RETURNS THE NUMBER OF PAIRS IN A CERTAIN SUIT
    def contains_pair_in_suit(self, hand, suit):
        num_pairs = 0
        for card in hand:
            if self.get_suit(card) != suit:
                continue
            for card2 in hand:
                if card is not card2 and card == card2:
                    num_pairs += 1
        num_pairs /= 2
        return num_pairs

    def contains_tractor_of_length(self, hand, length_tractor):
        """
        This checks if the first player's move is a valid tractor.
        we find the value of each card in the play and add it to a list
        This list is then sorted
        If it is a tractor, it should look something similar to
        (1) [3, 3, 4, 4, 5, 5] etc.
        Since it is already the same suit, we just need to check that we have this type of sequence
        :param hand: the list of cards first player wants to play
        :param length_tractor: the number of pairs in the tractor (min: 2)
        :return:
        """
        assert length_tractor >= 2, 'contains_tractor_of_length function invalid variable'
        assert len(hand) % 2 == 0, 'hand contains odd number of cards in contains_tractor_of_length'
        assert len(hand) == 2 * length_tractor
        card_value_list = []
        for card in hand:
            card_value_list.append(self.card_value(card))
        card_value_list.sort()

        assert len(hand) == len(card_value_list), 'contains_tractor_of_length error'
        for i in range(len(card_value_list)):
            if card_value_list[i] - card_value_list[0] != i % 2:
                return False
        #At this point, should satisfy the format (1) in the documentation
        return True

    def is_valid_fpi(self, hand):
        if len(hand) == 2:
            if self.contains_pair(hand) == 1:
                return True
        elif len(hand) == 1:
            return True
        else:
            return False

    # ASSUMES ALL CARDS ARE IN SAME SuIT
    def return_tractors(self, hand):
        '''
        Should be a tractor at this point, just need to return in tractor format
        :param hand:
        :return:
        '''
        maxval = 0
        for card in hand:
            maxval = max(self.card_value(card), maxval)
        len_tractor = len(hand) // 2
        return Tractor(maxval, len_tractor)

    def return_pairs(self, hand):
        list_pair = []
        for card in hand:
            for card2 in hand:
                if card is not card2 and card == card2:
                    list_pair.append(Pair(card, self.get_suit(card)))
        return list_pair

    def return_singles(self, hand):
        list_singles = []
        for card in hand:
            list_singles.append(card)
        return list_singles

    def get_num_points(self, hand):
        total = 0
        for card in hand:
            if card.get_rank() == '5':
                total += 5
            elif card.get_rank() == '10' or card.get_rank() == 'K':
                total += 10
        return total

    def get_first_player_move(self, first_player):
        self.current_player = self.players.index(first_player)
        fp_input = self.get_player_input(self.current_player)

        # Check if input is a list of valid indexes
        if not self.is_valid_input(first_player, fp_input):
            return {"move_code": "invalid indexes"}
        fp_hand = first_player.get_hand()

        # CHECK IF SELECtiON IS ONE SUIT
        suit_list = []
        for each_index in fp_input:
            suit_list.append(self.get_suit(fp_hand[each_index]))
        suit_set = set(suit_list)
        if len(suit_set) != 1:
            return {"move_code": "suit_set error"}

        else:
            cur_suit = self.get_suit(first_player.get_hand()[fp_input[0]])
        fpi_hand = []
        hand_type = []
        for index in fp_input:
            fpi_hand.append(fp_hand[index])

        # FOR NOW, JUST CHECK IF PAIR OR SINGLE
        if not self.is_valid_fpi(fpi_hand):
            return {"move_code": "invalid move"}

        # CHECK FOR LARGEST PAIR, THEN LARGEST SINGLE
        if len(fpi_hand) == 2:
            fpi_response = self.return_pairs(fpi_hand)
            hand_type.append('pair')
        elif len(fpi_hand) == 1:
            fpi_response = self.return_singles(fpi_hand)
            hand_type.append('single')
        return {"move_code": "valid",
                "index_response": fp_input,
                "suit": cur_suit,
                "fpi_hand": fpi_response,
                "hand_type": hand_type,
                "size": len(fpi_hand),
                'points': self.get_num_points(fpi_hand)}

    def num_cards_in_suit(self, hand, suit):
        total = 0
        for card in hand:
            if self.get_suit(card) == suit:
                total += 1
        return total

    def num_pairs_in_suit(self, hand, suit):
        total_pair = 0
        for card in hand:
            if self.get_suit(card) != suit:
                continue
            else:
                for card2 in hand:
                    if card == card2 and card is not card2:
                        total_pair += 1
        total_pair /= 2
        return total_pair

    def contains_tractor_of_length_in_suit(self, hand, length, suit):
        card_value_list = []
        for card in hand:
            if self.get_suit(card) == suit:
                card_value_list.append(self.card_value(card))
        card_value_list.sort()
        if len(card_value_list) < 2 * length:
            return False
        found_tractor = False
        for starting_index in range(len(card_value_list) - 2 * length + 1):
            not_a_tractor = False
            for i in range(starting_index, starting_index + 2 * length):
                if not_a_tractor:
                    break
                if card_value_list[i] - card_value_list[starting_index] != i % 2 - starting_index:
                    not_a_tractor = True

            if not not_a_tractor:
                found_tractor = True
                return True

        return False

    def tractor_gt(self, tractor1, tractor2):
        if tractor1.get_highest_value() > tractor2.get_highest_value():
            return True
        else:
            return False

    def get_secondary_player_move(self, player, cur_hand_info):
        self.current_player = self.players.index(player)
        cur_suit = cur_hand_info['suit']
        hand_size = cur_hand_info['size']
        print("Current suit: " + cur_suit + ", current hand size: " + str(hand_size))
        np_input = self.get_player_input(self.current_player)
        if not self.is_valid_input(player, np_input):
            return {"move_code": "invalid indexes"}
        if not hand_size == len(np_input):
            return {"move_code": "wrong number of cards"}
        np_hand = player.get_hand()
        npi_hand = []
        for index in np_input:
            npi_hand.append(np_hand[index])

        # CHECK IF PLAYED PROPER NUMBER OF SINGLES AND PAIR IN SAME SUIT
        min_singles = min(self.num_cards_in_suit(np_hand, cur_suit), hand_size)
        if not self.num_cards_in_suit(npi_hand, cur_suit) == min_singles:
            return {'move_code': 'insufficient number of current suit'}
        if min_singles == 2:
            min_pair = min(self.num_pairs_in_suit(np_hand, cur_suit), 1)
            if not self.num_pairs_in_suit(npi_hand, cur_suit) == min_pair:
                return {'move_code': 'insufficient number of pairs'}

        biggest_hand = cur_hand_info['biggest_hand']
        biggest_player = cur_hand_info['biggest_player']
        if hand_size == 1:
            npi_response = self.return_singles(npi_hand)
            has_bigger_single = self.cmp_cards(npi_response[0], biggest_hand[0]) > 0
            return {'move_code': 'valid',
                    'index_response': np_input,
                    'npi_hand': npi_response,
                    'biggest_hand': npi_response if has_bigger_single else biggest_hand,
                    'biggest_player': player if has_bigger_single else biggest_player,
                    'points': self.get_num_points(npi_hand)}

        if hand_size == 2 and self.contains_pair(npi_hand):
            npi_response = self.return_pairs(npi_hand)
            has_bigger_pair = self.pair_gt(npi_response[0], biggest_hand[0])
            return {'move_code': 'valid',
                    'index_response': np_input,
                    'npi_hand': npi_response,
                    'biggest_hand': npi_response if has_bigger_pair else biggest_hand,
                    'biggest_player': player if has_bigger_pair else biggest_player,
                    'points': self.get_num_points(npi_hand)}

        else:
            npi_response = self.return_singles(npi_hand)
            return {'move_code': 'valid',
                    'index_response': np_input,
                    'npi_hand': npi_response,
                    'biggest_hand': biggest_hand,
                    'biggest_player': biggest_player,
                    'points': self.get_num_points(npi_hand)}

    def is_attacker(self, player):
        if player is self.players[self.zhuang_jia_id] or player is self.players[(self.zhuang_jia_id + 2) % 4]:
            return False
        return True

    def del_indexes(self, player, index_response):
        for index in sorted(index_response, reverse=True):
            del player.get_hand()[index]

    def play_turn(self, sp_index):
        self.cards_played = {0: [], 1: [], 2: [], 3: []}
        first_player = self.players[sp_index]
        print("Hello " + first_player.get_name() + '. Please enter the cards you would like to play.'
                                                   ' Attacker current points: ' + str(self.attacker_points))

        first_player.print_hand()
        while True:
            fpi = self.get_first_player_move(first_player)
            if fpi['move_code'] != 'valid':
                print("ERROR: " + fpi['move_code'])
                continue
            else:
                break
        self.current_player = 5
        self.client_input = ''
        for index in fpi['index_response']:
            self.cards_played[sp_index].append(first_player.get_hand()[index])
        current_turn_points = 0
        current_turn_points += fpi['points']
        info_dict = {'suit': fpi['suit'],
                     'hand_type': fpi['hand_type'],
                     'size': fpi['size'],
                     'biggest_hand': fpi['fpi_hand'],
                     'biggest_player': first_player}
        self.del_indexes(first_player, fpi['index_response'])

        for i in range(sp_index + 1, sp_index + 4):
            cur_player_index = i % 4
            cur_player = self.players[cur_player_index]
            print("Hello " + cur_player.get_name() + '. Please enter the cards you would like to play.'
                                                     ' Attacker current points: ' + str(self.attacker_points) +
                  ' Current turn points: ' + str(current_turn_points))
            cur_player.print_hand()
            while True:
                npi = self.get_secondary_player_move(cur_player, info_dict)
                if npi['move_code'] != 'valid':
                    print("ERROR: " + npi['move_code'])
                    continue
                else:
                    break
            self.current_player = 5
            self.client_input = ''
            for index in npi['index_response']:
                self.cards_played[cur_player_index].append(cur_player.get_hand()[index])
            info_dict['biggest_hand'] = npi['biggest_hand']
            info_dict['biggest_player'] = npi['biggest_player']
            current_turn_points += npi['points']
            self.del_indexes(self.players[cur_player_index], npi['index_response'])

        if self.is_attacker(info_dict['biggest_player']):
            self.attacker_points += current_turn_points

        print(info_dict['biggest_player'].get_name() + ' won the hand with ' + str(npi['biggest_hand'][0]))

        return {'trick_winner': self.players.index(info_dict['biggest_player']),
                'num_cards': info_dict['size']}

    def get_players(self):
        return self.players

    def get_deck(self):
        return self.deck

    def get_current_player(self):
        return self.current_player

    def get_player_input(self, curr_player):
        # just player indexes, check if integerse
        self.current_player = curr_player
        response = self.client_input

        integer_list = [int(s) for s in response if s.isdigit()]
        return integer_list

    def is_valid_input(self, player, response):
        if len(set(response)) != len(response):
            return False
        for each_index in response:
            if int(each_index) < 0 or int(each_index) >= len(player.get_hand()):
                return False
        return True

    def get_data(self):
        data = ''
        data += str(0) + ':' + str(self.players[0].get_hand()) + ':' + str(self.cards_played[0])
        for i in range(3):
            data += ':' + str(i+1) + ':' + str(self.players[i+1].get_hand()) + ':' + str(self.cards_played[i+1])
        data += ':' + str(self.clear) + ':' + str(self.di_pai) + ':' + str(self.game_start) \
                + ':' + str(self.attacker_points) + ':' + str(self.trump_suit)
        return data

    def set_client_input(self, input):
        self.client_input = input

    def get_attacker_points(self):
        return self.attacker_points