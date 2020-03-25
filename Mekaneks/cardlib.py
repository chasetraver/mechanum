import deckcardplayerclasses
import random

pointedstick = deckcardplayerclasses.Card("Pointed Stick", 0, 1, 1, 0, 5, 'Images/pointedStick.png')
conveyorwheels = deckcardplayerclasses.Card("Conveyor Wheels", 1, 0, 0, 0, 5, 'Images/conveyorWheels.png')
scraparmor = deckcardplayerclasses.Card("Scrap Armor", 0, 0, 0, 1, 5, 'Images/scrapArmor.png')
sticklobber = deckcardplayerclasses.Card("Stick Lobber", 0, 2, 1, 0, 7, 'Images/stickLobber.png')
arccannon = deckcardplayerclasses.Card("Arc-Cannon", 0, 2, 2, 0, 12, 'Images/arc-cannon.png')
durdle = deckcardplayerclasses.Card("Durdle", 99, 0, 0, 0, 2, 'Images/durdle.png')
broadside = deckcardplayerclasses.Card("The Broadside", 0, 1, 4, 0, 17, 'Images/theboradside.png')
mobilerepairs = deckcardplayerclasses.Card("Mobile Repairs", 1, 0, 0, 1, 15, 'Images/mobilerepairs.png')
rocketboost = deckcardplayerclasses.Card("Rocket Boost", 1, 1, 1, 0, 15,  'Images/rocket boost.png')

allcards = [pointedstick, conveyorwheels, scraparmor, sticklobber, arccannon, durdle, broadside, mobilerepairs,
            rocketboost]
emptycard = deckcardplayerclasses.Card("", 0, 0, 0, 0, 0, "")


def startingcards(characterselection):
    bugteststartcards = [scraparmor, scraparmor, scraparmor, scraparmor, scraparmor, scraparmor, scraparmor,
                         scraparmor, scraparmor, scraparmor]
    if characterselection == 1:

        startcards = [pointedstick, pointedstick, pointedstick, conveyorwheels, conveyorwheels, conveyorwheels,
                      conveyorwheels, sticklobber, sticklobber, scraparmor]
    elif characterselection == 2:
        startcards = [durdle, durdle, durdle, broadside, broadside, rocketboost, rocketboost, mobilerepairs,
                      arccannon, arccannon]
    else:
        return bugteststartcards
    return startcards


def randomcard():
    i = (len(allcards))
    r = random.randint(0, i)
    return allcards[r - 1]
