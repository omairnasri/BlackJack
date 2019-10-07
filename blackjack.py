from time import sleep
from random import randint

# Seconds to sleep
s1 = 1
s2 = 2
s3 = 3
s6 = 6
s10 = 10

def print_menu():
    print("""\n{0}Menu{0}
0.) Quit
1.) Play Blackjack
Please enter an option from above""".format(("-" * 15)))

def check_int(x):
    for char in x:
        if char in "0123456789":
            result = True
        else:
            result = False
            break
    return result

def test_menu_selected(x):
    is_int = check_int(x)
    if is_int:
        x = int(x)
    else:
        print("Please only enter an integer")
        return x
    if x == 0:
        return x
    if x == 1:
        explain_blackjack()
    else:
        print("Please only enter one of the available options.")
        return x


def test_player_options(option):
    is_int = check_int(option)
    if is_int:
        option = int(option)
    else:
        print("Please only enter one of the available choices")
        return False
    if option == 1:
        return "hit"
    elif option == 2:
        return "stay"
    else:
        print("Please only enter one of the available choices")
        return False


def explain_blackjack():
    global needs_explain
    if needs_explain:
        needs_explain = False
        print("Thanks for playing blackjack. The rules are as follows:")
        sleep(s3)
        print("""1.) The dealer will deal you and himself two cards each.
    You will be able to see BOTH of your cards and ONE of the dealer's cards.""")
        sleep(s6)
        print("""2.) The object is to get as close to 21 points as possible without going over.
    The dealer will try to get as close to 21 as possible as well.
    He has to keep drawing until his points are higher than 17.
    You may stop drawing whenever you like""")
        sleep(s10)
        print("""3.) All number cards (2-10) are worth their number value in points
    All face cards(Jack, Queen, King) are worth 10 points
    The Ace is worth either 1 or 11, it is up to you to decide.""")
        sleep(s10)
        print("Press enter when you are ready to play")
    else:
    	pass


def load_deck():
    deck = [0] * 52
    suits = ["hearts", "diamonds", "spades", "clubs"]
    ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
    i = s_i = r_i = 0
    c_i = 1
    for card in deck:
        rank = ranks[r_i]
        suit = suits[s_i]
        new_card = "{} of {}".format(rank, suit)
        deck[i] = [c_i, new_card]
        if r_i < 12:
            r_i += 1
            c_i += 1
        else:
            r_i = 0
            c_i = 1
            s_i += 1
        i += 1
    return deck


def shuffle_deck(old_deck):
    new_deck = []
    used_indexes = []
    while len(new_deck) < 52:
        index_to_use = randint(0, 51)
        if index_to_use in used_indexes:
            continue
        else:
            new_deck.append(old_deck[index_to_use])
            used_indexes.append(index_to_use)
    return new_deck


needs_explain = True