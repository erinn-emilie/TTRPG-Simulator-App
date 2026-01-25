from enum import Enum

class TileGenerationTypes(Enum):
    RANDOM = 0
    WEIGHTED = 1

    def get_gen_type_from_key(key:int):
        match(key):
            case 0:
                return TileGenerationTypes.RANDOM
            case 1:
                return TileGenerationTypes.WEIGHTED
            case _:
                return TileGenerationTypes.WEIGHTED