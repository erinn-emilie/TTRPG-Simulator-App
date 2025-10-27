import random

class Seed():
    def __init__(self, num = 0):
        if(num < 100000 or num > 999999):
            num = random.randint(100000,999999)
        random.seed(num)

    def getNextBiomeInt(self):
        return random.randint(0,9)

    def getChanceInt(self):
        return random.randint(1,100)

    def getOtherRandInt(self, start:int, stop:int):
        return random.randint(start, stop)