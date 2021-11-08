from .card import Card, Shoe, Deck
import asyncio
import User

#build a hand class which will hold the cards and the value of the hand
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.value == 11:
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
#build a player object which will hold an id, bet amount and multiple hands
class Player:
    def __init__(self, id, bet):
        self.user = User(id, bet)
        self.hands = []
        self.hands.append(Hand())
        self.active_hand = 0
        self.split = False
        self.double_down = False
        self.blackjack = False
        self.bust = False
        self.win = False
        self.lose = False
        self.push = False

    def add_hand(self):
        self.hands.append(Hand())
        self.active_hand += 1

    def hit(self, card):
        self.hands[self.active_hand].add_card(card)
        self.hands[self.active_hand].adjust_for_ace()

    def double_down(self, card):
        self.double_down = True
        self.user.bet *= 2
        self.hit(card)

    def split(self, card1, card2):
        self.split = True
        self.add_hand()
        self.hit(card1)
        self.hit(card2)


#build a blackjack class that allows multiple players to play against the computer/dealer
class Blackjack:
    def check(author, hit_count):
		def inner_check(message):
			if message.author != author:return False
			if message.content.lower() == "hit":return True
			elif message.content.lower() == "stand" or message.content.lower() == "stay" or message.content.lower() == "pass":return True
			elif message.content.lower() == "double" and hit_count == 0:return True
			elif message.content.lower() == "surrender" and hit_count == 0:return True
		return inner_check
    
    def duelcheck(challenged):
		def inner_check(message):
			if message.author != challenged:return False
			if message.content.lower() == "accept":return True
			if message.content.lower() == "deny":return True
		return inner_check
    
    def hit_check(author, hit_count):
        def inner_check(message):
            if message.author != author:return False
            if message.content.lower() == "hit":return True
            elif message.content.lower() == "stand" or message.content.lower() == "stay" or message.content.lower() == "pass":return True
            elif message.content.lower() == "double" and hit_count == 0:return True
            elif message.content.lower() == "surrender" and hit_count == 0:return True
        return inner_check