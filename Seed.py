import random

class Seed():
    def __init__(self, tile_types_ref, num = 0):
        if(num < 100000 or num > 999999):
            num = random.randint(100000,999999)
        random.seed(num)
        self.total_tiles = tile_types_ref.get_total_tiles()

    # !!!
    # The stop number needs to not be static and change with the number of tiles
    def getNextBiomeInt(self):
        return random.randint(0,self.total_tiles+1)

    def getChanceInt(self):
        return random.randint(1,100)

    def getOtherRandInt(self, start:int, stop:int):
        return random.randint(start, stop)