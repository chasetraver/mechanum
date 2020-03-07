import deckcardplayerclasses
import random

pointedstick = deckcardplayerclasses.Card("Pointed Stick", 0, 1, 1, 0, 'pointedstick.png')
conveyorwheels = deckcardplayerclasses.Card("Conveyor Wheels", 1, 0, 0, 0, 'conveyorwheels.png')
scraparmor = deckcardplayerclasses.Card("Scrap Armor", 0, 0, 0, 1, 'scraparmor.png')
sticklobber = deckcardplayerclasses.Card("Stick Lobber", 0, 2, 1, 0, 'sticklobber.png')

allcards = [pointedstick, conveyorwheels, scraparmor, sticklobber]


def startingcards():
    startcards = [pointedstick, pointedstick, pointedstick, conveyorwheels, conveyorwheels, conveyorwheels, conveyorwheels, sticklobber, sticklobber, scraparmor]
    return startcards


def randomcard():
    i = (len(allcards))
    r = random.randint(0, i)
    return allcards[r]
