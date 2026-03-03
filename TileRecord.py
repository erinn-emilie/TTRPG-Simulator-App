from Enums.TokenTypes import TokenTypes
import TokenRecord

class TileRecord():
    def __init__(self, tile_type:str):
        self.tile_type = tile_type

        self.all_player_characters = []
        self.all_nonplayer_characters = []
        self.all_animal_tokens = []
        self.all_building_tokens = []
        self.all_monster_tokens = []
        self.all_nature_tokens = []
        self.all_structure_tokens = []

        self.filled_positions = []

        self.all_tokens = []
    def get_all_tokens(self) -> list:
        return self.all_tokens

    def get_player_characters_list(self) -> list:
        return self.all_player_characters

    def get_nonplayer_characters_list(self) -> list:
        return self.all_nonplayer_characters

    def get_animals_list(self) -> list:
        return self.all_animal_tokens

    def add_player_character(self, token:TokenRecord ):
        self.all_player_characters.append(token)
        self.all_tokens.append(token)

    def add_nonplayer_character(self, token:TokenRecord ):

        self.all_nonplayer_characters.append(token)
        self.all_tokens.append(token)

    def add_animal_token(self, token:TokenRecord ):

        self.all_animal_tokens.append(token)
        self.all_tokens.append(token)

    def add_building_token(self, token:TokenRecord ):

        self.all_building_tokens.append(token)
        self.all_tokens.append(token)

    def add_structure_token(self, token:TokenRecord ):

        self.all_structure_tokens.append(token)
        self.all_tokens.append(token)

    def add_nature_token(self, token:TokenRecord ):

        self.all_nature_tokens.append(token)
        self.all_tokens.append(token)

    def add_monster_token(self, token:TokenRecord ):

        self.all_monster_tokens.append(token)
        self.all_tokens.append(token)

    def remove_player_character(self, token:TokenRecord):
        record_key = token.get_record_key()
        for player in self.all_player_characters:
            if(player.get_record_key() == record_key):
                self.all_player_characters.remove(player)
                break
        self.__remove_from_all_tokens(record_key)


    def add_position(self, position:tuple):
        self.filled_positions.append(position)

    def check_position(self, pos_position:tuple) -> bool:
        for position in self.filled_positions:
            if(position[0] == pos_position[0] and position[1] == pos_position[1]):
                return False
        return True


    def __remove_from_all_tokens(self, record_key:int):
        for item in self.all_tokens:
            if(item.get_record_key() == record_key):
                self.all_tokens.remove(item)
                break


    def get_tile_type(self) -> str:
        return self.tile_type

    def set_tile_type(self, new_tile_type:str):
        self.tile_type = new_tile_type