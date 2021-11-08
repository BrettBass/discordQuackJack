import random

#build a card object which holds values 2 - ace
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

#build a deck object which holds 52 cards
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for value in range(2, 11):
                self.cards.append(Card(value, suit))
            for face in ["Jack", "Queen", "King", "Ace"]:
                self.cards.append(Card(face, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

#define a class to hold deck information of multiple decks called shoe
class Shoe:
    def __init__(self, decks):
        self.decks = decks
        self.cards = []
        self.build()

    def build(self):
        for deck in range(self.decks):
            deck = Deck()
            self.cards.extend(deck.cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
    
    def cut(self):
        random.shuffle(self.cards)
        cut = random.randint(0, len(self.cards))
        self.cards = self.cards[cut:] + self.cards[:cut]