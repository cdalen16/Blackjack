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


class Application:
    def __init__(self):
        self.deck = Deck()
        self.labels = []
        self.deal_labels = []

        self.window = tk.Tk()
        self.window.geometry("500x700")
        self.create_widgets()

        self.hit_button.bind("<Button-1>", self.hit_key)
        self.stand_button.bind("<Button-1>", self.stand_key)
        self.game_button.bind("<Button-1>", self.game_key)
        self.quit_button.bind("<Button-1>", self.quit_key)

        self.T = tk.Text(self.window, height=1, width=30)
        self.F = tk.Text(self.window, height=1, width=30)
        self.D = tk.Text(self.window, height=1, width=30)
        self.G = tk.Text(self.window, height=1, width=30)
        self.H = tk.Text(self.window, height=1, width=30)

        self.window.mainloop()

    def create_widgets(self):
        self.label = tk.Label(text="Blackjack", fg="white", bg="black")
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
            text="New Game",
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

        self.label.pack()
        self.hit_button.pack()
        self.stand_button.pack()
        self.game_button.pack()
        self.quit_button.pack()

    def hit_key(self, event):
        hand = self.player1.get_hand()

        self.player1.hit_card(self.deck)

        for k in hand:
            if k.get_value() == 11 and self.get_val(hand) > 21:
                k.set_value(1)

        self.print_hand(hand)

        if self.get_val(hand) > 21:
            self.H = tk.Text(self.window, height=2, width=30)
            self.H.insert(tk.END, "You busted!")
            self.H.place(x=0, y=650)

    def stand_key(self, event):
        hand = self.player1.get_hand()
        dealer_hand = self.dealer.get_hand()

        while self.get_val(dealer_hand) < 17:
            self.dealer.hit_card(self.deck)

        self.print_hand(hand)
        self.print_deal_hand(True, dealer_hand)

        if self.get_val(dealer_hand) > 21:
            self.H.insert(tk.END, "Dealer busted! You win!")
        elif self.get_val(dealer_hand) > self.get_val(hand):
            self.H.insert(tk.END, "Better luck next time!")
        elif self.get_val(dealer_hand) < self.get_val(hand):
            self.H.insert(tk.END, "You win!")

        self.H.place(x=0, y=650)

    def game_key(self, event):
        self.player1 = Player()
        self.dealer = Dealer()

        self.player1.deal(self.deck)
        self.dealer.deal(self.deck)

        hand = self.player1.get_hand()
        dealer_hand = self.dealer.get_hand()

        self.H.delete('1.0', tk.END)

        self.print_hand(hand)
        self.print_deal_hand(False, dealer_hand)

    def quit_key(self, event):
        self.window.quit()

    def print_hand(self, curr_hand):

        for k in self.labels:
            k.destroy()
        count = 0
        self.T.delete('1.0', tk.END)
        self.F.delete('1.0', tk.END)
        self.F.delete('1.0', tk.END)
        string = "Your Hand: \n"
        self.T.insert('1.0', string)

        for k in curr_hand:
            load = Image.open("JPEG/" + k.get_symbol() + k.get_suit()[0] + ".jpg")
            newsize = (40, 50)
            load = load.resize(newsize)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self.window, image=render)
            img.image = render
            self.labels.append(img)
            img.place(x=count*50, y=400)
            count = count + 1

        self.F.insert('1.0', "Total: " + str(self.get_val(curr_hand)))
        self.F.place(x=0, y=470)

    def print_deal_hand(self, final, curr_hand):
        for k in self.deal_labels:
            k.destroy()

        self.D.delete('1.0', tk.END)
        self.G.delete('1.0', tk.END)
        string = "Dealer Hand: \n"
        self.D.insert('1.0', string)
        self.D.place(x=0, y=500)

        count = 0
        if final:
            for k in curr_hand:
                load = Image.open("JPEG/" + k.get_symbol() + k.get_suit()[0] + ".jpg")
                newsize = (40, 50)
                load = load.resize(newsize)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(self.window, image=render)
                img.image = render
                self.deal_labels.append(img)
                img.place(x=count*50, y=530)
                count = count + 1

            self.G.insert('1.0', "Total: " + str(self.get_val(curr_hand)))
        else:
            load = Image.open("JPEG/" + curr_hand[0].get_symbol() + curr_hand[0].get_suit()[0] + ".jpg")
            newsize = (40, 50)
            load = load.resize(newsize)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self.window, image=render)
            img.image = render
            self.deal_labels.append(img)
            img.place(x=0, y=530)

        self.G.place(x=0, y=600)

    def get_val(self, curr_hand):
        val = 0
        for k in curr_hand:
            val += k.get_value()

        return val


app = Application()
