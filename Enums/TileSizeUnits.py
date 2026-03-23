from enum import Enum
import math

class TileSizeUnits(Enum):
    FEET = 0
    YARDS = 1
    MILES = 2


    def convert_feet_to_yards(feet:int) -> int:
        yards = math.floor(feet/3)
        return yards

    def convert_feet_to_miles(feet:int) -> int:
        miles = math.floor(feet/5280)
        return miles
