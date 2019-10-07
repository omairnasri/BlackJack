try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

from random import shuffle
from time import sleep

def load_cards(cards):
    suits = ["spade", "club", "diamond", "heart"]
    ranks = ["ace_", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_", "10_", "jack_", "queen_", "king_"]

    extension = get_ext()

    s_i = r_i = 0
    value = 1
    for card in cards:
        rank = ranks[r_i]
        suit = suits[s_i]
        name = "cards/{}{}{}".format(rank, suit, extension)
        image = tkinter.PhotoImage(file=name)

        cards[cards.index(card)] = (value, image)

        if r_i < 12:
            r_i += 1
            value += 1
        else:
            r_i = 0
            value = 1
            s_i += 1


def get_ext():
    if tkinter.TkVersion >= 8.6:
        extension = ".png"
    else:
        extension = ".ppm"
    return extension


def deal_card(user):
    card = cards.pop(0)
    if user == "dealer":
        dealer_hand.append(card)
    elif user == "player":
        player_hand.append(card)
        update_score(user)
    return card


def update_score(user):
    score = 0
    has_ace = False
    if user == "dealer":
        hand = dealer_hand
        score_label = dealer_score_text
    elif user == "player":
        hand = player_hand
        score_label = player_score_text
    for card in hand:
        value = card[0]
        if value == 1 and not has_ace:
            value = 11
            has_ace = True
        elif value > 10:
            value = 10
        score += value
        if score > 21 and has_ace:
            score -= 10
            has_ace = False
    score_label.set(score)
    return score


def show_cards(user):
    global dealer_2card
    if user == "dealer":
        hand = dealer_hand
        frame = dealer_card_frame
        for card in hand:
            if card == hand[1]:
                dealer_2card = tkinter.Label(frame, image=back, relief="raised")
                dealer_2card.pack(side="left", padx=5)
            else:
                tkinter.Label(frame, image=card[1], relief="raised").pack(side="left", padx=5)
    elif user == "player":
        hand = player_hand
        frame = player_card_frame
        for card in hand:
            tkinter.Label(frame, image=card[1], relief="raised").pack(side="left", padx=5)


def end_game():
    global play
    hit.forget()
    stay.forget()
    play = tkinter.Button(button_frame, text="Play again", command=reset)
    play.pack(side="bottom")



def hit_player():
    card = deal_card("player")
    frame = player_card_frame
    tkinter.Label(frame, image=card[1], relief="raised").pack(side="left", padx=5)
    score = update_score("player")
    if score == 21:
        status_text.set("You got blackjack! You win!")
        end_game()
    elif score > 21:
        status_text.set("You have {} points, you busted.".format(score))
        end_game()


def compare(d):
    p = update_score("player")
    if p > d:
        status_text.set("You win with {} points!".format(p))
    elif d > p:
        status_text.set("The Dealer wins with {} points.".format(d))
    elif d == p:
        status_text.set("You and the Dealer tied with {} points!".format(d))
    end_game()



def play_dealer():
    p = update_score("player")
    if p == 21:
        status_text.set("You got blackjack! You win!")
        end_game()
    else:
        global dealer_2card
        dealer_2card.destroy()
        dealer_2card = tkinter.Label(dealer_card_frame, image=dealer_hand[1][1], relief="raised")
        dealer_2card.pack(side="left", padx=5)
        score = update_score("dealer")
        while score < 17:
            card = deal_card("dealer")
            frame = dealer_card_frame
            tkinter.Label(frame, image=card[1], relief="raised").pack(side="left", padx=5)
            score = update_score("dealer")
        if score > 21:
            status_text.set("The Dealer busted, you win!")
            end_game()
        elif score == 21:
            status_text.set("The Dealer got blackjack, you lose.")
            end_game()
        else:
            compare(score)


root = tkinter.Tk()

# Root window
root.geometry("640x400")
root.title("Single Player Blackjack")
root.configure(bg="lime green")

# Status text to let the player what is going on
status_text = tkinter.StringVar()
status_text.set("Let's Play Blackjack!")
status = tkinter.Label(root, textvariable=status_text, bg="grey")
status.config(font=("Courier", 20))
status.pack(side="top", fill="x")

# Table Frame to hold all the cards
table_frame = tkinter.Frame(root, bg="lime green")
table_frame.pack(side="top", fill="both", expand="true")

# Dealer info
dealer_score_text = tkinter.IntVar()
dealer_score_text.set("?")
dealer_score_label = tkinter.Label(table_frame, bg="lime green", textvariable=dealer_score_text, fg="white")
dealer_score_label.grid(row=1, column=0, sticky="n", pady=10)
dealer_name_label = tkinter.Label(table_frame, bg="lime green", text="Dealer", fg="white")
dealer_name_label.grid(row=0, column=0, sticky="s")

# Dealer cards
dealer_card_frame = tkinter.Frame(table_frame, bg="lime green")
dealer_card_frame.grid(row=0, column=1, rowspan=2, sticky="ew", pady=40)

# Player info
player_score_text = tkinter.IntVar()
player_score_text.set(0)
player_score_label = tkinter.Label(table_frame, bg="lime green", textvariable=player_score_text, fg="white")
player_score_label.grid(row=3, column=0, sticky="n", pady=10)
player_name_label = tkinter.Label(table_frame, bg="lime green", text="Player", fg="white")
player_name_label.grid(row=2, column=0, sticky="s")

# Player cards
player_card_frame = tkinter.Frame(table_frame, bg="lime green")
player_card_frame.grid(row=2, column=1, rowspan=2, sticky="ew")

# Buttons Frame
button_frame = tkinter.Frame(root, bg="grey")
button_frame.pack(side="bottom", fill="x")

hit = tkinter.Button(button_frame, text="Hit Me", command=hit_player)
hit.pack(side="left", padx="10")

stay = tkinter.Button(button_frame, text="Stay Hand", command=play_dealer)
stay.pack(side="left", padx="10")


cards = []
dealer_hand = []
player_hand = []

dealer_2card = None

back = tkinter.PhotoImage(file="cards/back{}".format(get_ext()))
def reset():
    global table_frame
    global dealer_card_frame
    global player_card_frame

    dealer_score_text.set("?")
    player_score_text.set(0)

    table_frame.forget()
    table_frame.pack(side="top", fill="both", expand="true")
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(table_frame, bg="lime green")
    dealer_card_frame.grid(row=0, column=1, rowspan=2, sticky="ew", pady=40)
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(table_frame, bg="lime green")
    player_card_frame.grid(row=2, column=1, rowspan=2, sticky="ew")
    play.destroy()
    hit.pack(side="left", padx="10")
    stay.pack(side="left", padx="10")
    status_text.set("Let's Play Blackjack!")
    main()


def main():
    global cards
    global dealer_hand
    global player_hand
    global dealer_2card
    cards = [0] * 52
    dealer_hand = []
    player_hand = []
    dealer_2card = None

    load_cards(cards)

    shuffle(cards)

    for i in range(2):
        deal_card("player")
        deal_card("dealer")

    show_cards("dealer")
    show_cards("player")

main()
root.mainloop()

