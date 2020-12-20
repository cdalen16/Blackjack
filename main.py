# Author - Campbell Dalen

import random


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    # get card suit
    def get_suit(self):
        return self.suit

    # get card value
    def get_value(self):
        if self.num == 14:
            return 11
        if self.num >= 10:
            return 10
        else:
            return self.num

    def get_symbol(self):
        if self.num > 10:
            if self.num == 11:
                return "J"
            elif self.num == 12:
                return "Q"
            elif self.num == 13:
                return "K"
            else:
                return "A"
        else:
            return str(self.num)


class Deck:

    def __init__(self):
        self.deck = []
        for i in range(2, 15):
            curr_card1 = Card(i, "Spades")
            curr_card2 = Card(i, "Hearts")
            curr_card3 = Card(i, "Clubs")
            curr_card4 = Card(i, "Diamonds")

            self.deck.append(curr_card1)
            self.deck.append(curr_card2)
            self.deck.append(curr_card3)
            self.deck.append(curr_card4)

        self.initial_deck = self.deck

    def get_deck(self):
        return self.deck

    def reset_deck(self):
        self.deck = self.initial_deck

    def hit_card(self):
        next_card = self.deck[0]
        self.deck.remove(next_card)
        return next_card

    def shuffle(self):
        new_deck = [None] * 52

        for k in self.deck:
            spot = random.randrange(0, 52)

            while new_deck[spot] is not None:
                spot = random.randrange(0, 52)

            new_deck[spot] = k

        self.deck = new_deck


class Player:

    def __init__(self):
        self.cards = []

    def deal(self, curr_deck):
        self.cards.append(curr_deck.hit_card())
        self.cards.append(curr_deck.hit_card())

    def hit_card(self, curr_deck):
        self.cards.append(curr_deck.hit_card())

    def get_hand(self):
        return self.cards


class Dealer:

    def __init__(self):
        self.cards = []

    def deal(self, curr_deck):
        self.cards.append(curr_deck.hit_card())
        self.cards.append(curr_deck.hit_card())

    def hit_card(self, curr_deck):
        self.cards.append(curr_deck.hit_card())

    def get_hand(self):
        return self.cards


def get_val(curr_hand):
    val = 0
    for k in curr_hand:
        val += k.get_value()

    return val


def print_hand(curr_hand):
    for k in curr_hand:
        print(k.get_symbol() + " " + k.get_suit())


this_deck = Deck()
this_deck.shuffle()

player1 = Player()
player1.deal(this_deck)

dealer = Dealer()
dealer.deal(this_deck)

hand = player1.get_hand()
dealer_hand = dealer.get_hand()

print("Your Hand")
print(hand[0].get_symbol() + " " + hand[0].get_suit())
print(hand[1].get_symbol() + " " + hand[1].get_suit())
print("Dealer")
print(dealer_hand[0].get_symbol() + " " + dealer_hand[0].get_suit())

hit = input("Hit or Stand?")

bust = False
while hit[0] == "h" and not bust:
    player1.hit_card(this_deck)

    print("Your Hand")
    print_hand(hand)

    if get_val(hand) > 21:
        print("You busted!")
        bust = True
    else:
        hit = input("Hit or Stand?")

if not bust:
    while get_val(dealer_hand) < 17:
        dealer.hit_card(this_deck)

    print("Your Hand")
    print_hand(hand)
    print("Total: " + str(get_val(hand)))

    print("Dealer")
    print_hand(dealer_hand)
    print("Total: " + str(get_val(dealer_hand)))

    if get_val(dealer_hand) > 21:
        print("Dealer busted! You win!")
    elif get_val(dealer_hand) > get_val(hand):
        print("Better luck next time!")
    elif get_val(dealer_hand) < get_val(hand):
        print("You win!")
