from blackjack import * 

def main():
    selected = None
    while selected != 0:
        print_menu()
        selected = input()
        if selected:
            selected = test_menu_selected(selected)
        if selected == 0:
            return
        elif selected == 1:
            play_blackjack()
        else:
            print("Please enter an option.")


def play_blackjack():
    deck = load_deck()
    deck = shuffle_deck(deck)
    players = get_players()
    players_dict, deck = deal_cards(players, deck)
    play_round(players_dict, deck)
    # show_cards(players_dict)


def get_players():
    print("How many players are there?")
    has_num_players = False
    while not has_num_players:
        num_players = input()
        if num_players:
            if num_players in "1234":
                has_num_players = True
                num_players = int(num_players)
                return num_players
            else:
                print("Please only enter a valid number of players between 1 and 4.")
        else:
            print("Please enter something.")


def deal_cards(players, deck):
    players_dict = [
        ["Dealer: ", []],
        ["Player1:", []],
        ["Player2:", []],
        ["Player3:", []],
        ["Player4:", []]
    ]
    for i in range(2):
        for i in range(players):
            card = deck[0]
            players_dict[i+1][1].append(card)
            deck.remove(card)
        card = deck[0]
        players_dict[0][1].append(card)
        deck.remove(card)
    return players_dict, deck


def play_round(players_dict, deck):
    announce_deal(players_dict)
    play_player(players_dict, deck)


def announce_deal(players_dict):
    for player in players_dict:
        player_num = players_dict.index(player)
        hand = get_hand(players_dict, player_num)
        if player_num == 0:
            print("The Dealer has been dealt a(n) {} and an unknown card.".format(hand[0][1].upper()))
            sleep(s2)
        elif hand == None:
            continue
        else:
            print("Player {} has been dealt a(n) {} and a(n) {}.".format(player_num, hand[0][1].upper(), hand[1][1].upper()))
            sleep(s2)


def play_player(players_dict, deck):
    for player in players_dict:
        player_num = players_dict.index(player)
        if player_num == 0:
            continue
        elif players_dict[player_num][1] != []:
            hand = get_hand(players_dict, player_num)
            print("\nPlayer {}, here is your hand:".format(player_num))
            card_name_hand = []
            for card in hand:
                card_name_hand.append(card[1])
            print(", ".join(card_name_hand).upper() + "\n")
            hand, deck = play_hand(hand, deck)
            players_dict[player_num][1] = hand
    play_dealer(players_dict, deck)


def get_hand(players_dict, player_num):
    list = players_dict[player_num]
    if list[1] != []:
        hand = []
        for card in list[1]:
            hand.append(card)
        return hand


def play_hand(hand, deck):
    stayed = False
    while not stayed:
        sleep(s2)
        print("What would you like to do?")
        print("1.) Hit (get another card)")
        print("2.) Stay (keep your cards and end your turn)")
        entered = False
        while not entered:
            decision = input()
            if decision:
                entered = True
                if decision.isdigit():
                    decision = int(decision)
                    if decision == 1:
                        hand, deck, card = hit(hand, deck)
                        print("You were dealt a {}. This is now your hand:".format(card[1].upper()))
                        card_name_hand = []
                        for card in hand:
                            card_name_hand.append(card[1].upper())
                        print(", ".join(card_name_hand))
                        current_points = get_min_score(hand)
                        if current_points > 21:
                            sleep(s2)
                            print("You have {} points.  You have busted.".format(current_points))
                            sleep(s2)
                            stayed = True
                    elif decision == 2:
                        print("Thank you. You have stayed.".format())
                        sleep(s2)
                        stayed = True
                        break
                    else:
                        print("Please only enter an available option.")
                        entered = False
                else:
                    print("Please enter an integer.")
                    entered = False
            else:
                print("Please enter something.")
    return hand, deck


def hit(hand, deck):
    card = deck[0]
    hand.append(card)
    deck.remove(card)
    return hand, deck, card


def get_min_score(cards):
    total = 0
    for card in cards:
        if card[0] > 10:
            total += 10
        else:
            total += card[0]
    return total


def play_dealer(players_dict, deck):
    dealer_done = False
    first_time = True
    while not dealer_done:
        hand = (players_dict[0][1])
        score = score_dealer(hand)
        if score >= 17:
            if first_time:
                print("The dealer has:")
                card_name_hand = []
                for card in hand:
                    card_name_hand.append(card[1])
                print(", ".join(card_name_hand).upper())
            print("The dealer has {} points.".format(score))
            compare_points(players_dict)
            dealer_done = True
        else:
            first_time = False
            hand, deck, card = hit(hand, deck)
            print("The dealer was dealt a {}. This is now the dealer's hand:".format(card[1].upper()))
            card_name_hand = []
            for card in hand:
                card_name_hand.append(card[1].upper())
            print(", ".join(card_name_hand))
            sleep(s2)



def score_dealer(hand):
    total = 0
    aces = []
    for card in hand:
        value = card[0]
        if value == 1:
            aces.append(card)
            continue
        elif value < 11:
            total += value
        else:
            total += 10
    for card in aces:
        option1 = total + 11
        option2 = total + 1
        difference1 = 21 - option1
        difference2 = 21 - option2
        if difference1 < 0 or (option1 == 21 and len(aces) > (aces.index(card) + 1)):
            total += 1
        elif difference1 < difference2:
            total += 11
    return total


def compare_points(players_dict):
    for list in players_dict:
        player_num = players_dict.index(list)
        if player_num == 0:
            dealer_points = score_dealer(list[1])
        else:
            hand = list[1]
            if hand != []:
                total = 0
                aces = []
                for card in hand:
                    value = card[0]
                    if value == 1:
                        aces.append(card)
                        continue
                    elif value < 11:
                        total += value
                    else:
                        total += 10
                if len(aces) > 0:
                    for ace in aces:
                        got_value = False
                        while not got_value:
                            print("Would you like your {} to be worth 1 or 11 points?".format(ace[1]))
                            ace_value = input()
                            if ace_value:
                                if ace_value in ["1", "11"]:
                                    total += ace_value
                                    got_value = True
                                else:
                                    print("Please only enter one of the available options.")

                            else:
                                print("Please enter something.")
                if total > 21:
                    print("Sorry, Player {}, but you have {} points, you have bust.".format(player_num, total))
                elif total == 21:
                    print("Congrats, Player {}, you had 21 points, you win this hand!".format(player_num))
                else:
                    if dealer_points > 21:
                        print("Congrats, Player {}, the Dealer got {} points, they have busted. You win!".format(player_num, dealer_points))
                    elif dealer_points > total:
                        print("Sorry, Player {}, you had {} points, but the Dealer got {} points. You lose.".format(player_num, total, dealer_points))
                    elif dealer_points < total:
                        print("Congrats, Player {}, you had {} points, and the Dealer only got {} points.  You win!".format(player_num, total, dealer_points))
                    else:
                        print("Congrats, Player {} and the Dealer tied with {} points each, you win!".format(player_num, total))
        sleep(s2)
    print("Play again?")


def determine_player_points(hand):
    value = 0
    for card in hand:
        # if card has 3 entries, it is an ace with a special value
        if len(card) == 3:
            value += card[2]
        # else if its value is 11 or above, it is a face card
        elif card[0] < 11:
            value += card[0]
        # else, its value is its points
        else:
            value += 10
    if value == 21:
        print(value)
        print("You win! Want to play again?")
        main()
    elif value > 21:
        print(value)
        print("You've busted! Dealer wins, want to play again?")
        main()
    else:
        return False, value


def hit_dealer(hand, deck):
    # determine if dealer has more than 17 points
    #   if he does see if he has over 21, if so, end game
    #   else, compare points
    # else, deal him a card and see if he has 17 points now
    d_points = 0
    first_time = True
    while d_points < 17:
        d_points = 0
        aces = []
        for card in hand:
            if card[0] == 1:
                aces.append(card)
                continue
            elif 11 > card[0] > 1:
                d_points += card[0]
            elif card[0] >= 11:
                d_points += 10
        for card in aces:
            option1 = d_points + 11
            option2 = d_points + 1
            difference1 = 21 - option1
            difference2 = 21 - option2
            if difference1 < 0 or (option1 == 21 and len(aces) > (aces.index(card) + 1)):
                d_points += 1
            elif difference1 < difference2:
                d_points += 11
        if d_points >= 17:
            print("The dealer has:")
            sleep(s1)
            new_hand = []
            for card in hand:
                name = card[1].upper()
                new_hand.append(name)
            print(", ".join(new_hand))
            sleep(s3)
            print("The dealer has {} points.".format(d_points))
            sleep(s2)
            break
        else:
            if first_time:
                print("The dealer has {} points.".format(d_points))
                sleep(s2)
                first_time = False
            else:
                print("Now the dealer has {} points.".format(d_points))
                sleep(s2)
            new_card = deck[0]
            print("The dealer dealt himself a {}.".format(new_card[1].upper()))
            sleep(s2)
            hand.append(new_card)
            deck.remove(new_card)
    if d_points > 21:
        print("The dealer busted, you win! Want to play again?")
        sleep(s2)
        main()
    else:
        return d_points


def stay(p_hand, d_hand, deck):
    for card in p_hand:
        if card[0] == 1:
            value_determined = False
            while not value_determined:
                value_determined = True
                print("Would you like your {} to be 1 point or 11 points?".format(card[1]))
                end_value = input()
                if end_value in ["1", "11"]:
                    end_value = int(end_value)
                    card.append(end_value)
                    determine_player_points(p_hand)
                else:
                    print("Please enter only a '1' or an '11'")
                    value_determined = False
    game_over, p_points = determine_player_points(p_hand)
    if not game_over:
        print("You have:")
        new_hand = []
        for card in p_hand:
            name = card[1].upper()
            new_hand.append(name)
        print(", ".join(new_hand))
        sleep(s2)
        print("You have {} points".format(p_points))
        sleep(s2)
        print("The dealer was dealt a(n) {} and a(n) {}".format(d_hand[0][1].upper(), d_hand[1][1].upper()))
        sleep(s3)
        print("Now the dealer will play his hand:")
        sleep(s3)
        d_points = hit_dealer(d_hand, deck)
        sleep(s2)
        compare_points(p_points, d_points)

main()