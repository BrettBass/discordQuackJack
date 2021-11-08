import random
#build a card class
values = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

#bulid a deck class to hold 52 cards
class Deck:
    def __init__(self):
        self.deck = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
                self.deck.append(Card(suit, rank))
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
#build a hand class to hold cards and calculate values
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

#build a shoe class
class Shoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = []
        for i in range(num_decks):
            self.cards += Deck().deck
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        single_card = self.cards.pop()
        return single_card

#bulid a player class
class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
    
    def hit(self, card):
        self.hand.add_card(card)
        self.hand.adjust_for_ace()
    
    def get_total(self):
        return self.hand.value

    def show_hand(self):
        print("\n" + self.name + ":")
        for card in self.hand.cards:
            print(card)
        print("\nTotal: " + str(self.hand.value))

    def clear_hand(self):
        self.hand.cards = []
        self.hand.value = 0
        self.hand.aces = 0

#build a dealer class
class Dealer:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand
    
    def hit(self, card):
        self.hand.add_card(card)
        self.hand.adjust_for_ace()
    
    def get_total(self):
        return self.hand.value

    def show_hand(self):
        print("\nDealer:")
        for card in self.hand.cards:
            print(card)
        print("\nTotal: " + str(self.hand.value))

    def clear_hand(self):
        self.hand.cards = []
        self.hand.value = 0
        self.hand.aces = 0

#build a game class
class Game:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.shoe = Shoe(num_decks)
        self.player = Player("Player", Hand())
        self.dealer = Dealer("Dealer", Hand())
    
    def deal_card(self):
        single_card = self.shoe.deal()
        return single_card
    
    def show_hands(self):
        self.player.show_hand()
        self.dealer.show_hand()
    
    def hit_or_stand(self):
        while True:
            choice = input("\nHit or Stand? ")
            if choice[0].lower() == "h":
                self.player.hit(self.deal_card())
            elif choice[0].lower() == "s":
                break
            else:
                print("\nInvalid choice. Try again.")
    
    def play_game(self):
        self.player.hit(self.deal_card())
        self.player.hit(self.deal_card())
        self.dealer.hit(self.deal_card())
        self.dealer.hit(self.deal_card())
        self.show_hands()
        self.hit_or_stand()
        self.show_hands()
        if self.player.get_total() > 21:
            print("\nYou busted!")
        elif self.dealer.get_total() > 21:
            print("\nDealer busted!")
        elif self.player.get_total() > self.dealer.get_total():
            print("\nYou win!")
        elif self.player.get_total() < self.dealer.get_total():
            print("\nDealer wins!")
        else:
            print("\nPush!")
        self.player.clear_hand()
        self.dealer.clear_hand()

#play the game
game = Game(1)
game.play_game()