from RandomizationTypes import RandomizationTypes
from MapSizes import MapSizes
from Seed import Seed

class Settings():
    def __init__(self, excludedTypes = [], randType = RandomizationTypes.DEFAULT, mapSize = MapSizes.SMALL):
        self.excludedTypes = excludedTypes
        self.randType = randType
        self.mapSize = mapSize
        self.seed = Seed()

    def setNewSeed(self, newSeed):
        self.seed = Seed(newSeed)

    def setNewRandomSeed(self):
        self.seed = Seed()

    def getSeedRef(self):
        return self.seed

    def setRandType(self, newRandType:RandomizationTypes):
        self.randType = newRandType

    def getRandType(self) -> RandomizationTypes:
        return self.randType

    def setMapSize(self, newMapSize:MapSizes):
        self.mapSize = newMapSize

    def getMapSize(self) -> MapSizes:
        return self.mapSize
    
    def addExcludedType(self, itemToAdd:str):
        self.excludedTypes.append(itemToAdd)

    def removeExcludedType(self, itemToRemove:str) -> bool:
        if(itemToRemove in self.excludedTypes):
            self.excludedType.remove(itemToRemove)
            return True
        else:
            return False

    def clearExcludedTypes(self):
        self.excludedTypes.clear()

    def findExcludedType(self, itemKey:str) -> bool:
        if(itemKey in self.excludedTypes):
            return True
        else:
            return False
