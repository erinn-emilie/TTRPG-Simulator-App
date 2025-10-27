class TileRecord():
    def __init__(self, tileType:str):
        self.tileType = tileType

    def getTileType(self) -> str:
        return self.tileType

    def setTileType(self, newTileType:str):
        self.tileType = newTileType