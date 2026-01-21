from Creatures import Creatures

class TileRecord():
    def __init__(self, tileType:str):
        self.tileType = tileType
        self.creatures = []

    def getTileType(self) -> str:
        return self.tileType

    def setTileType(self, newTileType:str):
        self.tileType = newTileType

    def addCreature(self, newCreature:Creatures):
        self.creatures.append(newCreature)

    def removeCreature(self, oldCreature:Creatures):
        self.creatures.remove(oldCreature)

    def findCreature(self, creature:Creatures) -> bool:
        if(creature in self.creatures):
            return True
        else:
            return False