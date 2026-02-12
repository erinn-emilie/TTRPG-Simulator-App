
class TileRecord():
    def __init__(self, tile_type:str):
        self.tile_type = tile_type
        self.player_characters = []

    def getTileType(self) -> str:
        return self.tile_type

    def setTileType(self, new_tile_type:str):
        self.tile_type = new_tile_type