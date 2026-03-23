from toolbox.TileTypes import TileTypes
from toolbox.HextileMap import HextileMap
from toolbox.Settings import Settings
from toolbox.Tokens import Tokens
from toolbox.SavedMaps import SavedMaps
from toolbox.Logger import Logger

class Toolbox():
    def __init__(self, screen_width:int, screen_height:int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.tile_types_ref = TileTypes()
        self.logger_ref = Logger()
        self.player_characters_ref = Tokens("jsonfiles/PlayerCharacters.json")
        self.nonplayer_characters_ref = Tokens("jsonfiles/NonPlayerCharacters.json")
        self.animals_ref = Tokens("jsonfiles/Animals.json")
        self.monsters_ref = Tokens("jsonfiles/Monsters.json")
        self.buildings_ref = Tokens("jsonfiles/Buildings.json")
        self.structures_ref = Tokens("jsonfiles/Structures.json")
        self.nature_ref = Tokens("jsonfiles/Nature.json")
        self.settings_ref = Settings(self.tile_types_ref)
        self.saved_maps_ref = SavedMaps()
        self.hextile_map_ref = HextileMap(self.tile_types_ref, self.settings_ref, self.player_characters_ref, self.nonplayer_characters_ref, self.animals_ref, self.monsters_ref, self.buildings_ref, self.structures_ref, self.nature_ref, self.saved_maps_ref, self.screen_width, self.screen_height, self.logger_ref)


    def get_tile_types_ref(self) -> TileTypes:
        return self.tile_types_ref

    def get_player_characters_ref(self) -> Tokens:
        return self.player_characters_ref

    def get_nonplayer_characters_ref(self) -> Tokens:
        return self.nonplayer_characters_ref

    def get_animals_ref(self) -> Tokens:
        return self.animals_ref

    def get_monsters_ref(self) -> Tokens:
        return self.monsters_ref

    def get_buildings_ref(self) -> Tokens:
        return self.buildings_ref

    def get_structures_ref(self) -> Tokens:
        return self.structures_ref

    def get_nature_ref(self) -> Tokens:
        return self.nature_ref

    def get_list_of_token_refs(self) -> list:
        return [self.player_characters_ref, self.nonplayer_characters_ref, self.animals_ref, self.monsters_ref, self.buildings_ref, self.structures_ref, self.nature_ref]

    def get_hextile_map_ref(self) -> HextileMap:
        return self.hextile_map_ref

    def get_settings_ref(self) -> Settings:
        return self.settings_ref

    def get_saved_maps_ref(self) -> SavedMaps:
        return self.saved_maps_ref

    def get_logger_ref(self) -> Logger:
        return self.logger_ref

    def get_screen_width(self) -> int:
        return self.screen_width

    def get_screen_height(self) -> int:
        return self.screen_height

