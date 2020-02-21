import random
import pygame


class Card:
    def __init__(self, name, move, attack, damage, armor):
        self.name = name
        self.move = move
        self.attack = attack
        self.damage = damage
        self.armor = armor

    def playeffect(self, player):
        # TODO make move, attack, etc. do stuff with the grid
        # armor should work as intended
        player.armor += self.armor
        pass


class Deck:
    def __init__(self, cards):
        self.cards = cards

    def show(self):
        # Not functional, arguably not necessary
        for card in self.cards:
            card.show()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def addcard(self, card):
        self.cards.append(card)

    def drawcard(self):
        return self.cards.pop()

    def swapdeck(self, deck):
        # swaps cards in this deck and another deck. Used for shuffling discard pile back into draw pile.
        temp = self.cards
        self.cards = deck.cards
        deck.cards = temp
        self.shuffle()
        deck.shuffle()
        pass


class Player:
    def __init__(self):
        self.hand = []
        self.armor = 0

    def draw(self, deck):
        self.hand.append(deck.drawcard())
        return self

    def discard(self, cardindex, discarddeck):
        discarddeck.addcard(self.hand.pop(cardindex))

    def playcard(self, cardindex, discarddeck):
        self.hand[cardindex].playeffect()
        self.discard(cardindex, discarddeck)

    def damage(self, amount, drawdeck, trashdeck):
        # when player takes damage, reduces armor first if possible before putting top card of drawdeck into trashdeck
        for x in range(0, amount):
            if self.armor != 0:
                trashdeck.append(drawdeck.drawcard())
            else:
                self.armor = self.armor - 1

    def showhand(self):
        for card in self.hand:
            card.show
        pass



