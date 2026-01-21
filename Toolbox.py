from TileTypes import TileTypes
from HextileMap import HextileMap
from Settings import Settings
from Creatures import Creatures

# A class that holds the reference to the TileTypes object, the Settings object,
# the Creatures object, and the HextileMap object. Only one of each of these should
# exist in the application (which is what the toolbox is for)
# If a class needs one of these references, it should be passed the toolbox,
# NOT make an object of the class it needs itself.
class Toolbox():
    def __init__(self):
        self.tile_types_ref = TileTypes()
        self.settings_ref = Settings()
        self.creatures_ref = Creatures()
        self.hextile_map_ref = HextileMap(self.tile_types_ref, self.settings_ref)

    def get_tile_types_ref(self) -> TileTypes:
        return self.tile_types_ref

    def get_hextile_map_ref(self) -> HextileMap:
        return self.hextile_map_ref

    def get_settings_ref(self) -> Settings:
        return self.settings_ref

    def get_creatures_ref(self) -> Creatures:
        return self.creatures_ref
