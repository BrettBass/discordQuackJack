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
        import random
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()