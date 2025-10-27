import json

class TileTypes():
    JSON_FILE_PATH = "TileTypes.json"

    def __init__(self):
        self.typesDict = {}
        self.tileKeyMap = {}
        self.tileNamesList = []
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.typesDict = json.load(file)
            self.__setup()
        except FileNotFoundError:
            print("Couldn't find JSON file with tile types!")
        except json.JSONDecodeError:
            print("JSON file with tile types couldn't be decoded!")

    def __setup(self):
        counter = 0
        for tile in self.typesDict:
            self.tileKeyMap[tile] = self.typesDict[tile]["key"]
            if(counter != 0):
                self.tileNamesList.append(self.typesDict[tile]["name"])
            counter += 1

    def getTileNamesList(self) -> list:
        return self.tileNamesList

    def getTileNameByKey(self, key) -> str:
        try: 
            for tile in self.tileKeyMap:
                if self.tileKeyMap[tile] == key:
                    return tile
            return "NONE"
        except KeyError:
            return "NONE"

    def getTileKeyByName(self, tileName) -> int:
        try: 
            return self.tileKeyMap[tileName]
        except KeyError:
            return -1


    def getTileWeightByName(self, rowTileName:str, colTileName:str) -> int:
        try: 
            return self.typesDict[rowTileName]["tile_weights"][colTileName]
        except KeyError:
            return 0

    def getTileWeightByKey(self, row:int, col:int) -> int:
        rowTileName = self.getTileNameByKey(row)
        colTileName = self.getTileNameByKey(col)
        return self.getTileWeightByName(rowTileName, colTileName)


    def getDefaultTileAssetByName(self, tileName:str) -> str:
        try: 
            return self.typesDict[tileName]["default_asset"]
        except KeyError:
            return ''
    def getDefaultTileAssetByKey(self, key:int) -> str:
        tileName = self.__getTileNameByKey(key)
        return self.getDefaultTileAssetByName(tileName)

