# Author - Campbell Dalen

import random
import tkinter as tk
from PIL import Image, ImageTk


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    # get card suit
    def get_suit(self):
        return self.suit

    # get numerical value of card
    def get_value(self):
        if self.num == 14:
            return 11
        if self.num >= 10:
            return 10
        else:
            return self.num

    # get symbol of the card
    def get_symbol(self):
        if self.num > 10 or self.num == 1:
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

    # changes the value of the card
    def set_value(self, new_value):
        self.num = new_value


class Deck:

    def __init__(self):
        self.deck = []
        self.set_deck()

    # adds all 52 cards to the deck
    def set_deck(self):
        for i in range(2, 15):
            curr_card1 = Card(i, "Spades")
            curr_card2 = Card(i, "Hearts")
            curr_card3 = Card(i, "Clubs")
            curr_card4 = Card(i, "Diamonds")

            self.deck.append(curr_card1)
            self.deck.append(curr_card2)
            self.deck.append(curr_card3)
            self.deck.append(curr_card4)

        self.shuffle()

    # returns the deck
    def get_deck(self):
        return self.deck

    # removes the card from the deck when it is given to player/dealer
    # if the deck is empty, resets the deck
    def hit_card(self):
        if len(self.deck) == 0:
            self.set_deck()

        next_card = self.deck[0]
        self.deck.remove(next_card)
        return next_card

    # randomizes the card placement in the deck
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
        self.bal = 50.00

    # gives 2 cards to the player for the initial hand
    def deal(self, curr_deck):
        if len(self.cards) > 0:
            self.cards.clear()
        self.cards.append(curr_deck.hit_card())
        self.cards.append(curr_deck.hit_card())

    # adds another card to player's hand
    def hit_card(self, curr_deck):
        self.cards.append(curr_deck.hit_card())

    # adds given value to player's balance
    def deposit(self, deposit):
        self.bal = self.bal + deposit

    # removes given value from player's balance
    def place_bet(self, num):
        self.bal = self.bal - num

    # returns the cards in the player's hand
    def get_hand(self):
        return self.cards

    # returns the player's balance
    def get_bal(self):
        return self.bal


class Dealer:

    def __init__(self):
        self.cards = []

    # gives 2 cards to the dealer for the initial hand
    def deal(self, curr_deck):
        if len(self.cards) > 0:
            self.cards.clear()
        self.cards.append(curr_deck.hit_card())
        self.cards.append(curr_deck.hit_card())

    # adds another card to dealer's hand
    def hit_card(self, curr_deck):
        self.cards.append(curr_deck.hit_card())

    # returns the cards in the dealer's hand
    def get_hand(self):
        return self.cards


class Application:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player()
        self.dealer = Dealer()

        self.window = tk.Tk()
        self.window.geometry("400x700")
        self.create_widgets()

        self.window.mainloop()

    # adds widgets to window
    def create_widgets(self):
        label = tk.Label(text="Blackjack", fg="white", bg="black")
        label.place(x=177, y=0)
        your = tk.Label(text="Your Hand:", fg="black")
        your.place(x=0, y=375)
        deal = tk.Label(text="Dealer Hand:", fg="black")
        deal.place(x=0, y=500)

        self.bal = tk.Label(text="Balance: " + str(self.player1.get_bal()), fg="black")
        self.bet = tk.Entry(self.window)
        self.bet.place(x=10, y=250)

        self.labels = []
        self.deal_labels = []

        self.player_total = tk.Text(self.window, height=1, width=30)
        self.deal_total = tk.Text(self.window, height=1, width=30)
        self.message = tk.Text(self.window, height=1, width=30)

        self.stand_button = tk.Button(
            text="Stand",
            width=25,
            height=5,
            bg="Red",
        )
        self.hit_button = tk.Button(
            text="Hit",
            width=25,
            height=5,
            bg="Green",
        )
        self.game_button = tk.Button(
            text="Place Bet",
            width=25,
            height=5,
            bg="Yellow",
        )
        self.quit_button = tk.Button(
            text="Quit",
            width=25,
            height=5,
            bg="Purple",
        )

        self.bal.place(x=0, y=0)

        self.hit_button.bind("<Button-1>", self.hit_key)
        self.stand_button.bind("<Button-1>", self.stand_key)
        self.game_button.bind("<Button-1>", self.game_key)
        self.quit_button.bind("<Button-1>", self.quit_key)

        self.hit_button.place(x=10, y=50)
        self.stand_button.place(x=210, y=50)
        self.game_button.place(x=10, y=150)
        self.quit_button.place(x=210, y=150)

        disable(self.hit_button)
        disable(self.stand_button)

    # player hits card
    def hit_key(self, event):
        # makes sure button is enabled
        if self.stand_button['state'] == "disabled":
            return

        hand = self.player1.get_hand()

        self.player1.hit_card(self.deck)

        # checks for aces and resets values
        for k in hand:
            if k.get_value() == 11 and get_val(hand) > 21:
                k.set_value(1)

        self.print_hand(hand)

        # checks for a bust
        if get_val(hand) > 21:
            self.message.insert(tk.END, "You busted!")
            self.message.place(x=0, y=650)
            disable(self.hit_button)
            disable(self.stand_button)
            enable(self.game_button)

    # player stands
    def stand_key(self, event):
        # makes sure button is enables
        if self.stand_button['state'] == "disabled":
            return

        # resets widgets
        enable(self.game_button)
        disable(self.hit_button)
        disable(self.stand_button)

        hand = self.player1.get_hand()
        dealer_hand = self.dealer.get_hand()

        # dealer hits until hand is at least 17
        while get_val(dealer_hand) < 17:
            self.dealer.hit_card(self.deck)

        self.print_hand(hand)
        self.print_deal_hand(True, dealer_hand)

        # checks for hand outcome against dealer
        if get_val(dealer_hand) > 21:
            self.message.insert(tk.END, "Dealer busted! You win!")
            self.player1.deposit(self.my_bet * 2)
            self.bal.config(text="Balance: " + str(self.player1.get_bal()))
        elif get_val(dealer_hand) > get_val(hand):
            self.message.insert(tk.END, "Better luck next time!")
        elif get_val(dealer_hand) < get_val(hand):
            self.message.insert(tk.END, "You win!")
            self.player1.deposit(self.my_bet * 2)
            self.bal.config(text="Balance: " + str(self.player1.get_bal()))
        else:
            self.message.insert(tk.END, "Push")
            self.player1.deposit(self.my_bet)
            self.bal.config(text="Balance: " + str(self.player1.get_bal()))

        self.message.place(x=0, y=650)

    # player places new bet
    def game_key(self, event):
        # makes sure button is enabled
        if self.game_button['state'] == "disabled":
            return

        # resets widgets
        enable(self.hit_button)
        enable(self.stand_button)
        disable(self.game_button)
        self.message.delete('1.0', tk.END)

        # places bet
        self.my_bet = 0.0
        if self.bet.get() != "":
            self.my_bet = float(self.bet.get())
        self.player1.place_bet(self.my_bet)
        self.bal.config(text="Balance: " + str(self.player1.get_bal()))

        self.player1.deal(self.deck)
        self.dealer.deal(self.deck)

        # checks for double ace hand
        for k in self.player1.get_hand():
            if k.get_value() == 11 and get_val(self.player1.get_hand()) > 21:
                k.set_value(1)

        # checks for a blackjack
        if get_val(self.player1.get_hand()) == 21 and self.dealer.get_hand()[0].get_value() < 10:
            self.message.insert(tk.END, "Blackjack!")
            self.player1.deposit(self.my_bet + (self.my_bet * 1.5))
            self.bal.config(text="Balance: " + str(self.player1.get_bal()))
            disable(self.hit_button)
            disable(self.stand_button)
            enable(self.game_button)

        self.print_hand(self.player1.get_hand())
        self.print_deal_hand(False, self.dealer.get_hand())

    # player quits
    def quit_key(self, event):
        self.window.quit()

    # displays player's hand in window
    def print_hand(self, curr_hand):
        # resets hand in window
        for k in self.labels:
            k.destroy()
        self.player_total.delete('1.0', tk.END)

        # gets the right images for given hand
        count = 0
        for k in curr_hand:
            load = Image.open("JPEG/" + k.get_symbol() + k.get_suit()[0] + ".jpg")
            self.load_img(load, self.labels).place(x=count*50, y=400)

            count = count + 1

        self.player_total.insert('1.0', "Total: " + str(get_val(curr_hand)))
        self.player_total.place(x=0, y=470)

    # displays dealer's hand in window
    def print_deal_hand(self, final, curr_hand):
        # resets hand in window
        for k in self.deal_labels:
            k.destroy()
        self.deal_total.delete('1.0', tk.END)

        # checks if dealer is only showing first card or not
        # gets images for the hand
        count = 0
        if final:
            for k in curr_hand:
                load = Image.open("JPEG/" + k.get_symbol() + k.get_suit()[0] + ".jpg")
                self.load_img(load, self.deal_labels).place(x=count * 50, y=530)
                count = count + 1

            self.deal_total.insert('1.0', "Total: " + str(get_val(curr_hand)))
        else:
            load = Image.open("JPEG/" + curr_hand[0].get_symbol() + curr_hand[0].get_suit()[0] + ".jpg")
            self.load_img(load, self.deal_labels).place(x=count * 50, y=530)
            self.deal_total.insert('1.0', "Total: " + str(curr_hand[0].get_value()))

        self.deal_total.place(x=0, y=600)

    # loads and resizes images for hand
    def load_img(self, load, hand):
        load = load.resize((50, 60))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.window, image=render)
        img.image = render
        hand.append(img)
        return img


# returns the value of the given hand
def get_val(curr_hand):
    val = 0
    for k in curr_hand:
        val += k.get_value()

    return val


# disables given button
def disable(button):
    button.config(state=tk.DISABLED)


# enables given button
def enable(button):
    button.config(state=tk.NORMAL)


game = Application()
