import random
import time


class Card():
    def __init__(self, level, value, suit):
        self.level = level
        self.value = value
        self.suit = suit

    def show_card(self):
        print(self.level + " of " + self.suit)


class Deck():
    def __init__(self):
        self.cards = []

    def build_deck(self):
        suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        levels = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                  '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

        for suit in suits:
            for level, value in levels.items():
                card = Card(level, value, suit)
                self.cards.append(card)

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def deal_card(self):
        card = self.cards.pop()
        return card


class Player():
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.playing_hand = True

    def draw(self, deck):
        for i in range(2):
            card = deck.deal_card()
            self.hand.append(card)

    def show_hand(self):
        print("\nYour Hand: ")
        for card in self.hand:
            card.show_card()

    def hit(self, deck):
        card = deck.deal_card()
        self.hand.append(card)

    def get_hand_value(self):
        self.hand_value = 0

        ace_in_hand = False

        for card in self.hand:
            self.hand_value += card.value
            if card.level == 'A':
                ace_in_hand = True

        if self.hand_value > 21 and ace_in_hand:
            self.hand_value -= 10

        print("Total Value: " + str(self.hand_value))

    def update_hand(self, deck):
        if self.hand_value < 21:
            choice = input("Would you like to hit (y/n)? ").lower()
            if choice == 'y':
                self.hit(deck)
            else:
                self.playing_hand = False

        else:
            self.playing_hand = False


class Dealer():
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.playing_hand = True

    def draw(self, deck):
        for i in range(2):
            card = deck.deal_card()
            self.hand.append(card)

    def show_hand(self):
        input("Press 'enter' to reveal the dealers hand.")
        for card in self.hand:
            card.show_card()
            time.sleep(1.5)

    def hit(self, deck):
        self.get_hand_value()

        while self.hand_value < 17:
            card = deck.deal_card()
            self.hand.append(card)
            self.get_hand_value()

        print("\nThe dealer has a total of " + str(len(self.hand)) + " cards.")

    def get_hand_value(self):
        self.hand_value = 0

        ace_in_hand = False

        for card in self.hand:
            self.hand_value += card.value
            if card.level == 'A':
                ace_in_hand = True

        if self.hand_value > 21 and ace_in_hand:
            self.hand_value -= 10


class Game():
    def __init__(self, money):
        self.money = int(money)
        self.bet = 20
        self.winner = ''

    def set_bet(self):
        betting = True
        while betting:
            bet = int(input("What would you like to bet (min. $20)?"))
            if bet < 20:
                bet = 20
            if bet > self.money:
                print("Sorry you cannot afford that bet amount.")
            else:
                self.bet = bet
                betting = False

    def scoring(self, player_value, dealer_value):
        if player_value == 21:
            print("\nYou got BLACK JACK!!! You win!")
            self.winner = 'p'
        elif dealer_value == 21:
            print("\nThe dealer got BLACK JACK!!! You lose!")
            self.winner = 'd'
        elif player_value > 21:
            print("\nYou went over 21! You lose!")
            self.winner = 'd'
        elif dealer_value > 21:
            print("\nThe dealer went over 21! You win!")
            self.winner = 'p'
        else:
            if player_value > dealer_value:
                print("\nThe dealer gets " + str(dealer_value) + ". You win!")
                self.winner = 'p'
            elif dealer_value > player_value:
                print("\nThe dealer gets " + str(dealer_value) + ". You lose!")
                self.winner = 'd'
            else:
                print("\nDealer gets " + str(dealer_value) + ". It's a push...")
                self.winner = 'tie'

    def payout(self):
        if self.winner == 'p':
            self.money += self.bet
        elif self.winner == 'd':
            self.money -= self.bet

    def show_money(self):
        print("Current money: $" + str(self.money))

    def show_bet_and_money(self):
        print("\nCurrent money: $" + str(self.money) + "\t\tCurrent bet: $" + str(self.bet))


print("Hello and welcome to BlackJack!")
print("The minimum bet at this table is $20")

playing = True
running = True
while running == True:

    playing = True

    money = int(input("\nHow much money do you want to play with today (min. $20)? "))

    if money < 20:
        print("\nThat is lower than the minimum bet! Sorry!")
        answerr = input("Do you want to buy in a higher amount (y/n)? ").lower()
        if answerr == 'y' or answerr == 'yes':
            continue
        else:
            running = False
            playing = False
    else:
        running = False

    game = Game(money)

    while playing:
        game_deck = Deck()
        game_deck.build_deck()
        game_deck.shuffle_deck()

        player = Player()
        dealer = Dealer()

        game.show_money()
        game.set_bet()

        player.draw(game_deck)
        dealer.draw(game_deck)

        game.show_bet_and_money()
        print("The dealer reveals a " + dealer.hand[0].level + " of " + dealer.hand[0].suit + ".")

        while player.playing_hand:
            player.show_hand()
            player.get_hand_value()
            player.update_hand(game_deck)

        dealer.hit(game_deck)
        dealer.show_hand()

        game.scoring(player.hand_value, dealer.hand_value)
        game.payout()

        again = input("Would you like to play again (y/n)? ").lower()
        if again == 'y' or again == 'yes':
            continue
        else:
            running == False
            playing == False

        if game.money < 20:
            rebuy = input("You have run out of cash! Would you like to rebuy (y/n)? ").lower()
            if rebuy == 'y' or rebuy == 'yes':
                playing = False
                running = True
            else:
                running = False
                playing = False

print("Thank you for playing blackjack!")