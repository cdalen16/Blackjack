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

    # get card value
    def get_value(self):
        if self.num == 14:
            return 11
        if self.num >= 10:
            return 10
        else:
            return self.num

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

    def set_value(self, new_value):
        self.num = new_value


class Deck:

    def __init__(self):
        self.deck = []
        self.set_deck()

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

    def get_deck(self):
        return self.deck

    def hit_card(self):
        if len(self.deck) == 0:
            self.set_deck()

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
        self.bal = 50.00

    def deal(self, curr_deck):
        if len(self.cards) > 0:
            self.cards.clear()
        self.cards.append(curr_deck.hit_card())
        self.cards.append(curr_deck.hit_card())

    def hit_card(self, curr_deck):
        self.cards.append(curr_deck.hit_card())

    def deposit(self, deposit):
        self.bal = self.bal + deposit

    def place_bet(self, num):
        self.bal = self.bal - num

    def get_hand(self):
        return self.cards

    def get_bal(self):
        return self.bal


class Dealer:

    def __init__(self):
        self.cards = []

    def deal(self, curr_deck):
        if len(self.cards) > 0:
            self.cards.clear()
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


class Application:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player()
        self.dealer = Dealer()

        self.window = tk.Tk()
        self.window.geometry("400x700")
        self.create_widgets()

        self.window.mainloop()

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

        self.disable(self.hit_button)
        self.disable(self.stand_button)

    def hit_key(self, event):
        hand = self.player1.get_hand()

        self.player1.hit_card(self.deck)

        for k in hand:
            if k.get_value() == 11 and get_val(hand) > 21:
                k.set_value(1)

        self.print_hand(hand)

        if get_val(hand) > 21:
            self.message.insert(tk.END, "You busted!")
            self.message.place(x=0, y=650)
            self.disable(self.hit_button)
            self.disable(self.stand_button)

    def stand_key(self, event):
        self.disable(self.hit_button)
        self.disable(self.stand_button)
        hand = self.player1.get_hand()
        dealer_hand = self.dealer.get_hand()

        while get_val(dealer_hand) < 17:
            self.dealer.hit_card(self.deck)

        self.print_hand(hand)
        self.print_deal_hand(True, dealer_hand)

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

    def game_key(self, event):
        self.enable(self.hit_button)
        self.enable(self.stand_button)
        self.my_bet = 0.0

        if self.bet.get() != "":
            self.my_bet = float(self.bet.get())

        self.player1.place_bet(self.my_bet)
        self.bal.config(text="Balance: " + str(self.player1.get_bal()))

        self.message.delete('1.0', tk.END)

        self.player1.deal(self.deck)
        self.dealer.deal(self.deck)

        if get_val(self.player1.get_hand()) == 21 and self.dealer.get_hand()[0].get_value() < 10:
            self.message.insert(tk.END, "Blackjack!")
            self.player1.deposit(float(self.bet.get()) * 2.5)
            self.bal.config(text="Balance: " + str(self.player1.get_bal()))
            self.disable(self.hit_button)
            self.disable(self.stand_button)

        self.print_hand(self.player1.get_hand())
        self.print_deal_hand(False, self.dealer.get_hand())

    def quit_key(self, event):
        self.window.quit()

    def print_hand(self, curr_hand):
        for k in self.labels:
            k.destroy()
        self.player_total.delete('1.0', tk.END)

        count = 0
        for k in curr_hand:
            load = Image.open("JPEG/" + k.get_symbol() + k.get_suit()[0] + ".jpg")
            self.load_img(load, self.labels).place(x=count*50, y=400)

            count = count + 1

        self.player_total.insert('1.0', "Total: " + str(get_val(curr_hand)))
        self.player_total.place(x=0, y=470)

    def print_deal_hand(self, final, curr_hand):
        for k in self.deal_labels:
            k.destroy()
        self.deal_total.delete('1.0', tk.END)

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

    def load_img(self, load, hand):
        load = load.resize((50, 60))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.window, image=render)
        img.image = render
        hand.append(img)
        return img

    def disable(self, button):
        button.config(state=tk.DISABLED)

    def enable(self, button):
        button.config(state=tk.NORMAL)


game = Application()
