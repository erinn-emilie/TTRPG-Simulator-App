from Enums.TokenTypes import TokenTypes
import TokenRecord

class TileRecord():
    def __init__(self, tile_type:str):
        self.tile_type = tile_type

        self.all_player_characters = []
        self.all_nonplayer_characters = []
        self.all_animals_characters = []
        self.all_buildings_characters = []
        self.all_monsters_characters = []
        self.all_nature_characters = []
        self.all_structures_characters = []

        self.all_tokens = []
        self.filled_positions = []

    def get_all_tokens(self) -> list:
        return self.all_tokens

    def get_player_characters_list(self) -> list:
        return self.all_player_characters

    def get_nonplayer_characters_list(self) -> list:
        return self.all_nonplayer_characters

    def get_animals_list(self) -> list:
        return self.all_animals_characters

    def add_player_character(self, token:TokenRecord, position:tuple):
        package = (token, position)
        self.all_player_characters.append(package)
        self.all_tokens.append(package)

    def add_nonplayer_character(self, token:TokenRecord, position:tuple):
        package = (token, position)
        self.all_nonplayer_characters.append(package)
        self.all_tokens.append(package)

    def add_animal_token(self, token:TokenRecord, position:tuple):
        package = (token, position)
        self.all_animals_characters.append(package)
        self.all_tokens.append(package)

    def remove_player_character(self, token:TokenRecord):
        record_key = token.get_record_key()
        for player in self.all_player_characters:
            if(player.get_record_key() == record_key):
                self.all_player_characters.remove(player)
                break
        self.__remove_from_all_tokens(record_key)


    def __remove_from_all_tokens(self, record_key:int):
        for item in self.all_tokens:
            if(item.get_record_key() == record_key):
                self.all_tokens.remove(item)
                break


    def get_tile_type(self) -> str:
        return self.tile_type

    def set_tile_type(self, new_tile_type:str):
        self.tile_type = new_tile_type