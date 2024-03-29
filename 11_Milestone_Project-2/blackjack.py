
# Udemy course - Complete Python Bootcamp
# Section 11: Milestone Project - 2
# Blackjack game


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank+ " of " +self.suit

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces +=1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips to bet?  "))
        except:
            print("Sorry, please provide an integer")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, you don't have enough! You have {chips.total}")
            else:
                break

def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input("Hit or Stand? (H/S)")
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player stands, dealer's turn")
            playing = False
        else:
            print("Sorry, what?")
            continue
        break

def player_busts(player,dealer,chips):
    print("Player BUSTS!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player WINS!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer BUSTS! Player WINS!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer WINS!")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and player tie! It's a PUSH.")

def show_some(player,dealer):
    print("DEALERS HAND:")
    print("One card hidden!")
    print(dealer.cards[1])
    print("\nPLAYER'S HAND:")
    for card in player.cards:
        print(card)

def show_all(player,dealer):
    print("DEALERS HAND:")
    for card in dealer.cards:
        print(card)
    print("\nPLAYER'S HAND:")
    for card in player.cards:
        print(card)

while True:

    # Print an openign statement
    print("Welcome to Blackjack!")

    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips
    player_chips = Chips()

    # Prompt the player for their bet
    take_bet(player_chips)

    # Show cards (but keep 1 dealer card hidden)
    show_some(player_hand,dealer_hand)

    while playing:

        # Prompt for player to Hit or Stand
        hit_or_stand(deck,player_hand)
        # Show cards  (but keep 1 dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Plater hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scnearios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    # Inform Player of their chip total
    print(f"\n Player's chips: {player_chips.total}")

    # Ask to play again
    new_game = input("Would you like to play again? y/n  ")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break
