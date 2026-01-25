from enum import Enum

class TokenTypes(Enum):
    TILES = 0
    PLAYER_CHARACTERS = 1
    NON_PLAYER_CHARACTERS = 2
    MONSTERS = 3
    CREATURES = 4
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
                return ("Non-Player Characters")
            case TokenTypes.MONSTERS:
                return ("Monsters")
            case TokenTypes.CREATURES:
                return ("Creatures")
            case TokenTypes.BUILDINGS:
                return ("Buildings")
            case TokenTypes.STRUCTURES:
                return ("Structures")




    def get_token_str_from_key(key:int):
        token_type = TokenTypes.get_token_type_from_key(key)

    def get_token_type_from_key(key:int):
        match(key):
            case 0:
                return TokenTypes.TILES
            case 1:
                return TokenTypes.PLAYER_CHARACTERS
            case 2:
                return TokenTypes.NON_PLAYER_CHARACTERS
            case 3:
                return TokenTypes.MONSTERS
            case 4:
                return TokenTypes.CREATURES
            case 5:
                return TokenTypes.BUILDINGS
            case 6:
                return TokenTypes.STRUCTURES