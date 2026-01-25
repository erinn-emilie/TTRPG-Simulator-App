import random

class Seed():
    def __init__(self, num = 0):
        if(num < 100000 or num > 999999):
            num = random.randint(100000,999999)
        random.seed(num)

    # !!!
    # The stop number needs to not be static adn change with the number of tiles
    def getNextBiomeInt(self):
        return random.randint(0,10)

    def getChanceInt(self):
        return random.randint(1,100)

    def getOtherRandInt(self, start:int, stop:int):
        return random.randint(start, stop)