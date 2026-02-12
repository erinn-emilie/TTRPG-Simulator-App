from Enums.TileGenerationTypes import TileGenerationTypes
from Enums.MapSizes import MapSizes
from toolbox.Seed import Seed

class Settings():
    def __init__(self, tile_types_ref, excluded_types = [], rand_type = TileGenerationTypes.WEIGHTED, map_size = MapSizes.SMALL, tile_size = 1.0):
        self.excluded_types = excluded_types
        self.rand_type = rand_type
        self.map_size = map_size
        self.tile_size = tile_size
        self.seed = Seed(tile_types_ref)

    def setNewSeed(self, newSeed):
        self.seed = Seed(newSeed)

    def setNewRandomSeed(self):
        self.seed = Seed()

    def getSeedRef(self):
        return self.seed

    def setNewTileSize(self, new_tile_size:float):
        self.tile_size = new_tile_size

    def getTileSize(self) -> float:
        return self.tile_size

    def setRandType(self, newRandType:TileGenerationTypes):
        self.rand_type = newRandType

    def getRandType(self) -> TileGenerationTypes:
        return self.rand_type

    def setMapSize(self, newMapSize:MapSizes):
        self.map_size = newMapSize

    def getMapSize(self) -> MapSizes:
        return self.map_size
    
    def addExcludedType(self, itemToAdd:str):
        self.excluded_types.append(itemToAdd)

    def removeExcludedType(self, itemToRemove:str) -> bool:
        if(itemToRemove in self.excluded_types):
            self.excluded_types.remove(itemToRemove)
            return True
        else:
            return False

    def clearExcludedTypes(self):
        self.excluded_types.clear()

    def findExcludedType(self, itemKey:str) -> bool:
        if(itemKey in self.excluded_types):
            return True
        else:
            return False
