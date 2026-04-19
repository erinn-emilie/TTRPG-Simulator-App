from toolbox.TileTypes import TileTypes
from toolbox.HextileMap import HextileMap
from toolbox.Settings import Settings
from toolbox.Tokens import Tokens
from toolbox.SavedMaps import SavedMaps
from toolbox.Logger import Logger
from toolbox.Account import Account
from toolbox.ConnectionLogic import ClientSession
from toolbox.ConnectionLogic import ServerSession

from Enums.TokenTypes import TokenTypes

class Toolbox():
    def __init__(self, screen_width:int, screen_height:int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.account_ref = Account()
        self.tile_types_ref = TileTypes(self.account_ref)
        self.logger_ref = Logger(self.account_ref)
        self.player_characters_ref = Tokens("jsonfiles/PlayerCharacters.json", "assets/character.png", TokenTypes.PLAYER_CHARACTERS, self.account_ref)
        self.nonplayer_characters_ref = Tokens("jsonfiles/NonPlayerCharacters.json", "assets/character.png", TokenTypes.NON_PLAYER_CHARACTERS, self.account_ref)
        self.animals_ref = Tokens("jsonfiles/Animals.json", "assets/animal.png", TokenTypes.ANIMALS, self.account_ref)
        self.monsters_ref = Tokens("jsonfiles/Monsters.json", "assets/monsters.png", TokenTypes.MONSTERS, self.account_ref)
        self.buildings_ref = Tokens("jsonfiles/Buildings.json", "assets/buildings.png", TokenTypes.BUILDINGS, self.account_ref)
        self.structures_ref = Tokens("jsonfiles/Structures.json", "assets/buildings.png", TokenTypes.STRUCTURES, self.account_ref)
        self.nature_ref = Tokens("jsonfiles/Nature.json", "assets/nature.png", TokenTypes.NATURE, self.account_ref)
        self.settings_ref = Settings(self.tile_types_ref)
        self.saved_maps_ref = SavedMaps(self.account_ref)
        self.hextile_map_ref = HextileMap(self.tile_types_ref, self.settings_ref, self.player_characters_ref, self.nonplayer_characters_ref, self.animals_ref, self.monsters_ref, self.buildings_ref, self.structures_ref, self.nature_ref, self.saved_maps_ref, self.screen_width, self.screen_height, self.logger_ref, self.account_ref)
        self.client_session_ref = ClientSession(self.account_ref, self.saved_maps_ref, self.hextile_map_ref)
        self.server_session_ref = ServerSession(self.account_ref, self.saved_maps_ref, self.hextile_map_ref)


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

    def get_token_ref_by_category(self, category: str) -> Tokens:
        if category == "player_characters":
            return self.player_characters_ref
        elif category == "nonplayer_characters":
            return self.nonplayer_characters_ref
        elif category == "animals":
            return self.animals_ref
        elif category == "monsters":
            return self.monsters_ref
        elif category == "buildings":
            return self.buildings_ref
        elif category == "structures":
            return self.structures_ref
        elif category == "nature":
            return self.nature_ref
        return None

    def get_hextile_map_ref(self) -> HextileMap:
        return self.hextile_map_ref

    def get_settings_ref(self) -> Settings:
        return self.settings_ref

    def get_saved_maps_ref(self) -> SavedMaps:
        return self.saved_maps_ref

    def get_logger_ref(self) -> Logger:
        return self.logger_ref

    def get_account_ref(self) -> Account:
        return self.account_ref

    def get_screen_width(self) -> int:
        return self.screen_width

    def get_screen_height(self) -> int:
        return self.screen_height

    def get_client_session_ref(self) -> ClientSession:
        return self.client_session_ref

    def get_server_session_ref(self) -> ServerSession:
        return self.server_session_ref

    def reset_tokens_to_local(self):
        self.player_characters_ref.load_from_json()
        self.nonplayer_characters_ref.load_from_json()
        self.animals_ref.load_from_json()
        self.monsters_ref.load_from_json()
        self.buildings_ref.load_from_json()
        self.structures_ref.load_from_json()
        self.nature_ref.load_from_json()

    def reset_tokens_to_database(self):
        self.player_characters_ref.load_from_database()
        self.nonplayer_characters_ref.load_from_database()
        self.animals_ref.load_from_database()
        self.monsters_ref.load_from_database()
        self.buildings_ref.load_from_database()
        self.structures_ref.load_from_database()
        self.nature_ref.load_from_database()
        self.tile_types_ref.load_from_database()



