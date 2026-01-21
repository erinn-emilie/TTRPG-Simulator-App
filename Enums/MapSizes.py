from enum import Enum

class MapSizes(Enum):
    XSMALL = 4
    SMALL = 6
    MEDIUM = 8
    LARGE = 10
    XLARGE = 12

    def getMapSizeFromStr(value:str):
        match(value):
            case "Extra Small":
                return MapSizes.XSMALL
            case "Small":
                return MapSizes.SMALL
            case "Medium":
                return MapSizes.MEDIUM
            case "Large":
                return MapSizes.LARGE
            case "Extra Large":
                return MapSizes.XLARGE
            case _:
                return MapSizes.MEDIUM