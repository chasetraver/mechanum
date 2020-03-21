import random
import pygame


class Card:
    def __init__(self, name, move, attrange, damage, armor, cost, sprite):
        self.name = name
        self.move = move
        self.attrange = attrange
        self.damage = damage
        self.armor = armor
        self.image = sprite
        self.cost = cost


class Deck:
    def __init__(self, cards):
        self.cards = cards

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
    def __init__(self, drawdeck, discarddeck, trashdeck, xcoord, ycoord, playerselect):
        self.drawdeck = drawdeck
        self.discarddeck = discarddeck
        self.trashdeck = trashdeck
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.hand = []
        self.armor = 0
        self.score = 0
        self.gold = 0
        if playerselect == 1:
            self.sprite = 'Images/Robby.png'
        elif playerselect == 2:
            self.sprite = 'Images/doomcopter.png'
        self.isalive = True
        self.turn = 0
        self.loot = None
        self.cleanup = False

    def draw(self):
        if len(self.drawdeck.cards) > 0:
            self.hand.append(self.drawdeck.drawcard())
        else:
            if len(self.discarddeck.cards) > 0:
                self.drawdeck.swapdeck(self.discarddeck)
                self.hand.append(self.drawdeck.drawcard())
            else:
                self.gameover()

    def addcard(self, card):
        self.drawdeck.addcard(card)

    def discard(self, cardindex):
        self.discarddeck.addcard(self.hand.pop(cardindex))

    def damage(self, amount):
        # when player takes damage, reduces armor first if possible before putting top card of drawdeck into trashdeck
        count = 0
        while True:
            if count == amount:
                break
            count = count + 1
            if self.armor < 1:
                if len(self.drawdeck.cards) > 0:
                    trashedcard = self.drawdeck.drawcard()
                    self.trashdeck.addcard(trashedcard)
                    return trashedcard
                else:
                    if len(self.discarddeck.cards) > 0:
                        self.drawdeck.swapdeck(self.discarddeck)
                        trashedcard = self.drawdeck.drawcard()
                        self.trashdeck.addcard(trashedcard)
                        return trashedcard
                    else:
                        self.gameover()

            else:
                self.armor = self.armor - 1

    def showhand(self):
        for card in self.hand:
            card.show()
        pass

    def gameover(self):
        self.isalive = False
        pass


