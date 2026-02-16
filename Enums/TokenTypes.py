from enum import Enum

class TokenTypes(Enum):
    TILES = 0
    PLAYER_CHARACTERS = 1
    NON_PLAYER_CHARACTERS = 2
    ANIMALS = 3
    MONSTERS = 4
    BUILDINGS = 5
    STRUCTURES = 6
    NATURE = 7

    def get_str_from_token_type(token_type):
        match(token_type):
            case TokenTypes.TILES:
                return ("Tiles")
            case TokenTypes.PLAYER_CHARACTERS:
                return ("Player Characters")
            case TokenTypes.NON_PLAYER_CHARACTERS:
                return ("NonPlayer Characters")
            case TokenTypes.ANIMALS:
                return ("Animals")
            case TokenTypes.MONSTERS:
                return ("Monsters")
            case TokenTypes.BUILDINGS:
                return ("Buildings")
            case TokenTypes.STRUCTURES:
                return ("Structures")
            case TokenTypes.NATURE:
                return ("Nature")




    def get_token_str_from_key(key:int):
        token_type = TokenTypes.get_token_type_from_key(key)
        return token_type

    def get_token_type_from_key(key:int):
        match(key):
            case 0:
                return TokenTypes.TILES
            case 1:
                return TokenTypes.PLAYER_CHARACTERS
            case 2:
                return TokenTypes.NON_PLAYER_CHARACTERS
            case 3:
                return TokenTypes.ANIMALS
            case 4:
                return TokenTypes.MONSTERS
            case 5:
                return TokenTypes.BUILDINGS
            case 6:
                return TokenTypes.STRUCTURES
            case 7:
                return TokenTypes.NATURE