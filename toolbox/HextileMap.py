from toolbox.TileTypes import TileTypes
from Enums.MapSizes import MapSizes
from TileRecord import TileRecord
from HextileNode import HextileNode
from PyQt6.QtCore import QPoint

import json
import math

from Enums.TileGenerationTypes import TileGenerationTypes
from Enums.TokenTypes import TokenTypes
from Enums.MapLoadLocations import MapLoadLocations
from TokenRecord import TokenRecord

class HextileMap():
    def __init__(self, tile_types_ref, settings_ref, players_ref, nonplayers_ref, animals_ref, monsters_ref, buildings_ref, structures_ref, nature_ref, saved_maps_ref, screen_width, screen_height, logger_ref, load_location=MapLoadLocations.GENERATED, saved_map_name=""):
        self.JSON_SAVE_FILE = "jsonfiles/SavedMaps.json"
        self.local_map = {}
        self.tileTypes = tile_types_ref
        self.settings = settings_ref
        self.seed = settings_ref.getSeedRef()
        self.logger_ref = logger_ref
        self.saved_maps = saved_maps_ref
        self.tile_list = []
        self.tokens_on_map = []



        self.players_ref = players_ref
        self.nonplayers_ref = nonplayers_ref
        self.animals_ref = animals_ref
        self.monsters_ref = monsters_ref
        self.buildings_ref = buildings_ref
        self.structures_ref = structures_ref
        self.nature_ref = nature_ref

        self.tokens_ref_list = [self.players_ref, self.nonplayers_ref, self.animals_ref, self.monsters_ref, self.buildings_ref, self.structures_ref, self.nature_ref]

        self.current_map = {}
        self.load_location = load_location
        self.saved_map_name = saved_map_name

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.generateMap()

    def __findTokenTypeFromStr(self, title):
        match(title):
            case "Player Characters":
                return TokenTypes.PLAYER_CHARACTERS
            case "NonPlayer Characters":
                return TokenTypes.NON_PLAYER_CHARACTERS
            case "Animals":
                return TokenTypes.ANIMALS
            case "Monsters":
                return TokenTypes.MONSTERS
            case "Buildings":
                return TokenTypes.BUILDINGS
            case "Structures":
                return TokenTypes.STRUCTURES
            case "Nature":
                return TokenTypes.NATURE

    def __findTokenRefFromType(self, token_type):
        match(token_type):
            case TokenTypes.PLAYER_CHARACTERS:
                return self.players_ref
            case TokenTypes.NON_PLAYER_CHARACTERS:
                return self.nonplayers_ref
            case TokenTypes.ANIMALS:
                return self.animals_ref
            case TokenTypes.MONSTERS:
                return self.monsters_ref
            case TokenTypes.BUILDINGS:
                return self.buildings_ref
            case TokenTypes.STRUCTURES:
                return self.monsters_ref
            case TokenTypes.NATURE:
                return self.monsters_ref

    def generateMap(self):
        self.mapSize = self.settings.getMapSize()
        self.tile_list.clear()
        self.tokens_on_map.clear()
        self.centerNode = None
        self.seed = self.settings.getSeedRef()
        self.totalwater = self.__setTotalRivers()
        match(self.load_location):
            case MapLoadLocations.GENERATED:
                self.__createMap(self.mapSize.value)
                match(self.settings.getRandType()):
                    case TileGenerationTypes.RANDOM:
                        self.__populateRandomSettings()
                        self.__populateTilesRandomSettings()
                    case TileGenerationTypes.WEIGHTED:
                        self.__populateMapGenericSettings()
                        self.__populateTilesRandomSettings()
            case MapLoadLocations.LOCAL:
                self.loadSavedMap(self.saved_map_name)
        self.logger_ref.set_writable_status(True)



    def __setTotalRivers(self):
        if self.mapSize == MapSizes.XSMALL:
            return 2
        elif self.mapSize == MapSizes.SMALL:
            return 4
        elif self.mapSize == MapSizes.MEDIUM:
            return 6
        elif self.mapSize == MapSizes.LARGE:
            return 8
        else:
            return 10


    def getCenterNode(self) -> HextileNode:
        return self.centerNode

    def getMapSize(self) -> MapSizes:
        return self.mapSize


    def __get_token_ref_type(self, idx:int) -> TokenTypes:
        match(idx):
            case 0:
                return TokenTypes.PLAYER_CHARACTERS
            case 1:
                return TokenTypes.NON_PLAYER_CHARACTERS
            case 2:
                return TokenTypes.ANIMALS
            case 3:
                return TokenTypes.MONSTERS
            case 4:
                return TokenTypes.BUILDINGS
            case 5:
                return TokenTypes.STRUCTURES
            case 6:
                return TokenTypes.NATURE
            case _:
                return TokenTypes.NON_PLAYER_CHARACTERS

    def __createBlankNode(self, position:int) -> HextileNode:
        tileRec = TileRecord("NONE")
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode

    def __createNodeWithSetType(self, position:int, tileType:str) -> HextileNode: 
        tileRec = TileRecord(tileType)
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode




    def __createMap(self, size):
        self.centerNode = self.__createBlankNode(0)
        curNode = self.centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        self.tile_list.clear()
        self.tile_list.append(curNode)
        while(curRingNumber < size):
            curTileNum += 1
            if(curNode.getNorthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthNode(newNode)
                newNode.setSouthNode(curNode)
                self.tile_list.append(newNode)
            if(curNode.getNorthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthEastNode(newNode)
                newNode.setSouthWestNode(curNode)
                self.tile_list.append(newNode)
            if(curNode.getSouthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthEastNode(newNode)
                newNode.setNorthWestNode(curNode)
                self.tile_list.append(newNode)
            if(curNode.getSouthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthNode(newNode)
                newNode.setNorthNode(curNode)
                self.tile_list.append(newNode)
            if(curNode.getSouthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthWestNode(newNode)
                newNode.setNorthEastNode(curNode)
                self.tile_list.append(newNode)
            if(curNode.getNorthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthWestNode(newNode)
                newNode.setSouthEastNode(curNode)
                self.tile_list.append(newNode)

            northNode = curNode.getNorthNode()
            southNode = curNode.getSouthNode()
            northwestNode = curNode.getNorthWestNode()
            northeastNode = curNode.getNorthEastNode()
            southwestNode = curNode.getSouthWestNode()
            southeastNode = curNode.getSouthEastNode()

            northNode.setSouthEastNode(northeastNode)
            northNode.setSouthWestNode(northwestNode)

            northeastNode.setNorthWestNode(northNode)
            northeastNode.setSouthNode(southeastNode)

            southeastNode.setNorthNode(northeastNode)
            southeastNode.setSouthWestNode(southNode)

            southNode.setNorthEastNode(southeastNode)
            southNode.setNorthWestNode(southwestNode)

            southwestNode.setSouthEastNode(southNode)
            southwestNode.setNorthNode(northwestNode)

            northwestNode.setSouthNode(southwestNode)
            northwestNode.setNorthEastNode(northNode)

            if(curTileNum == numTilesInRing):
                if(curRingNumber == 0):
                    curNode = curNode.getNorthNode()
                else:
                    curNode = curNode.getNorthEastNode().getNorthNode()
                curRingNumber += 1
                numTilesInRing = curRingNumber * 6
                curTileNum = 0
            else:
                curNode = self.__iterateThroughNodes(curNode, curRingNumber, curTileNum, numTilesInRing)

    def __findNewTileType(self, node:HextileNode) -> TileTypes:
        northNode = node.getNorthNode()
        southNode = node.getSouthNode()
        northwestNode = node.getNorthWestNode()
        northeastNode = node.getNorthEastNode()
        southwestNode = node.getSouthWestNode()
        southeastNode = node.getSouthEastNode()
        typeArr = []


        if(northNode != None and northNode.getTileType() != "NONE"):
            typeArr.append(northNode.getTileType())
        if(southNode != None and southNode.getTileType() != "NONE"):
            typeArr.append(southNode.getTileType())
        if(northwestNode != None and northwestNode.getTileType() != "NONE"):
            typeArr.append(northwestNode.getTileType())
        if(northeastNode != None and northeastNode.getTileType() != "NONE"):
            typeArr.append(northeastNode.getTileType())
        if(southwestNode != None and southwestNode.getTileType() != "NONE"):
            typeArr.append(southwestNode.getTileType())
        if(southeastNode != None and southeastNode.getTileType() != "NONE"):
            typeArr.append(southeastNode.getTileType())
        newBiomeName = ""
        while(True):
            posBiome = self.seed.getNextBiomeInt()
            posName = self.tileTypes.get_tile_name_by_key(posBiome)
            while(posName == "WATER" and self.totalwater == 0):
                posBiome = self.seed.getNextBiomeInt()
                posName = self.tileTypes.get_tile_name_by_key(posBiome)
            if(posName == "WATER"):
                self.__setUpWater(node)
                self.totalwater -= 1
            while(self.settings.findExcludedType(posName)):
                posBiome = self.seed.getNextBiomeInt()
                posName = self.tileTypes.get_tile_name_by_key(posBiome)

            totalValue = 0
            for i in range(0, len(typeArr)):
                curBiome = self.tileTypes.get_tile_key_by_name(typeArr[i])
                totalValue = totalValue + self.tileTypes.get_tile_weight_by_key(curBiome, posBiome)
            valueToBeat = 100
            if(len(typeArr) != 0):
                valueToBeat = int(totalValue / len(typeArr))
            randValue = self.seed.getChanceInt()
            if(randValue <= valueToBeat):
                newBiomeName = posName
                break
        return newBiomeName

    def __setUpWater(self, node:HextileNode):
        direction = self.seed.getOtherRandInt(1,6)
        length = self.seed.getOtherRandInt(2,7)
        counter = 0
        if direction == 1: 
            node = node.getNorthNode()
        elif direction == 2:
            node = node.getNorthEastNode()
        elif direction == 3:
            node = node.getSouthEastNode()
        elif direction == 4:
            node = node.getSouthNode()
        elif direction == 5:
            node = node.getSouthWestNode()
        else:
            node = node.getNorthWestNode()

        while(node != None and counter < length):
            node.setTileType("WATER")
            if(direction == 1):
                node = node.getNorthNode()
            elif direction == 2:
                node = node.getNorthEastNode()
            elif direction == 3:
                node = node.getSouthEastNode()
            elif direction == 4:
                node = node.getSouthNode()
            elif direction == 5:
                node = node.getSouthWestNode()
            else:
                node = node.getNorthWestNode()
            counter += 1
                


    def __findMatchingTileType(self, node:HextileNode):
        northNode = node.getNorthNode()
        southNode = node.getSouthNode()
        northwestNode = node.getNorthWestNode()
        northeastNode = node.getNorthEastNode()
        southwestNode = node.getSouthWestNode()
        southeastNode = node.getSouthEastNode()
        typeArr = []

        if(northNode != None and northNode.getTileType() != "NONE"):
            typeArr.append(northNode.getTileType())
        if(southNode != None and southNode.getTileType() != "NONE"):
            typeArr.append(southNode.getTileType())
        if(northwestNode != None and northwestNode.getTileType() != "NONE"):
            typeArr.append(northwestNode.getTileType())
        if(northeastNode != None and northeastNode.getTileType() != "NONE"):
            typeArr.append(northeastNode.getTileType())
        if(southwestNode != None and southwestNode.getTileType() != "NONE"):
            typeArr.append(southwestNode.getTileType())
        if(southeastNode != None and southeastNode.getTileType() != "NONE"):
            typeArr.append(southeastNode.getTileType())

        if(len(typeArr) == 0):
            return self.__findNewTileType(node)
        idx = self.seed.getOtherRandInt(0,len(typeArr)-1)
        return typeArr[idx]


    def __iterateThroughNodes(self, curNode:HextileNode, curRingNumber:int, curTileNum:int, numTilesInRing:int) -> HextileNode:
        nextNode = curNode.getSouthEastNode()
        if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
            nextNode = curNode.getSouthNode()
            if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2) :
                nextNode = curNode.getSouthWestNode()
                if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                    nextNode = curNode.getNorthWestNode()
                    if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                        nextNode = curNode.getNorthNode()
                        if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                            nextNode = curNode.getNorthEastNode()
        return nextNode



    def __populateTilesRandomSettings(self):
        self.logger_ref.set_writable_status(False)
        tile_size = self.settings.getTileSize()
        min_tokens_per_tile = int(math.ceil(tile_size/8))
        max_tokens_per_tile = int(tile_size)
        record_key = 0
        self.tokens_on_map.clear()
        for tile in self.tile_list:
            total_tokens = self.seed.getOtherRandInt(min_tokens_per_tile, max_tokens_per_tile)
            tile_record = tile.getTileRecord()
            tile_type = tile_record.get_tile_type()
            for x in range(0, total_tokens-1):
                num_rand_tokens = 0

                rand_token_ref = None
                rand_token_ref_idx = -1


                iteration = 0
                while(num_rand_tokens == 0):
                    rand_token_ref_idx = self.seed.getOtherRandInt(0, len(self.tokens_ref_list)-1)
                    rand_token_ref = self.tokens_ref_list[rand_token_ref_idx]
                    num_rand_tokens = rand_token_ref.get_num_of_tokens()
                    iteration += 1
                    if(iteration == 100):
                        break
                if(iteration == 100):
                    continue


                rand_token_idx = -1
                rand_token = None
                allowed = False
                name = ""
                token_type = None

                iteration = 0
                while(not allowed):
                    rand_token_idx = self.seed.getOtherRandInt(0, num_rand_tokens)
                    rand_token = rand_token_ref.get_random_token_by_value(rand_token_idx)

                    if not rand_token is None:
                        multiple = rand_token["duplicatable"]
                        name = rand_token["name"]

                        token_type = self.__get_token_ref_type(rand_token_ref_idx)
                        allowed = True
                        if not multiple:
                            for token in self.tokens_on_map:
                                if(token_type == token.get_token_type() and name == token.get_name()):
                                    allowed = False
                                    break
                        
                        if allowed:
                            for tile in rand_token["excluded_tiles"]:
                                if(tile == tile_type):
                                    allowed = False
                                    break
                    iteration += 1
                    if(iteration == 50):
                        break

                if(iteration == 50):
                    continue

                record_key += 1
                token_record = TokenRecord(self.logger_ref, rand_token, token_type, record_key)
                self.tokens_on_map.append(token_record)

                match(token_type):
                    case TokenTypes.PLAYER_CHARACTERS:
                        tile_record.add_player_character(token_record)
                    case TokenTypes.NON_PLAYER_CHARACTERS:
                        tile_record.add_nonplayer_character(token_record)
                    case TokenTypes.ANIMALS:
                        tile_record.add_animal_token(token_record)
                    case TokenTypes.MONSTERS:
                        tile_record.add_monster_token(token_record)
                    case TokenTypes.BUILDINGS:
                        tile_record.add_building_token(token_record)
                    case TokenTypes.STRUCTURES:
                        tile_record.add_structure_token(token_record)
                    case TokenTypes.NATURE:
                        tile_record.add_nature_token(token_record)
        self.logger_ref.set_writable_status(True)

    def positionTokensOnTile(self):
        self.logger_ref.set_writable_status(False)
        tile_size = int(self.settings.getTileSize())

        #sqrt_tile_size = math.floor(math.sqrt(tile_size))


        for tile in self.tile_list:
            tile_record = tile.getTileRecord()
            all_tokens = tile_record.get_all_tokens()

            for token in all_tokens:
                x = self.seed.getOtherRandInt(0, tile_size)
                y = self.seed.getOtherRandInt(0, tile_size)
                iteration = 0
                while(not tile_record.check_position((x, y))):
                    x = self.seed.getOtherRandInt(0, tile_size)
                    y = self.seed.getOtherRandInt(0, tile_size)
                    iteration += 1
                    if iteration == 50:
                        break

                if iteration == 50:
                    break

                tile_record.add_position((x,y))
                token.set_position((x,y))

        self.logger_ref.set_writable_status(True)




    def __populateMapGenericSettings(self):
        curNode = self.centerNode
        biomeInt = self.seed.getNextBiomeInt()
        prevType = self.tileTypes.get_tile_name_by_key(biomeInt)
        while(self.settings.findExcludedType(prevType)):
            biomeInt = self.seed.getNextBiomeInt()
            prevType = self.tileTypes.get_tile_name_by_key(biomeInt)
        curNode.setTileType(prevType)
        sameTypeChance = 80

        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6
        curNode = curNode.getNorthNode()
        while(curRingNumber < self.mapSize.value + 1):
            curTileNum += 1
            if(curNode.getTileType() == "NONE"):
                if(self.seed.getChanceInt() <= sameTypeChance and prevType != "WATER"):
                    newType = self.__findMatchingTileType(curNode)
                    curNode.setTileType(newType)
                    if(newType == prevType):
                        sameTypeChance -=5
                    else:
                        sameTypeChance = 80
                        prevType = newType
                else:
                    newType = self.__findNewTileType(curNode)
                    curNode.setTileType(newType)
                    if(newType == prevType):
                        sameTypeChance -=5
                    else:
                        sameTypeChance = 80
                        prevType = newType
            
            if(curTileNum == numTilesInRing):
                curRingNumber += 1
                if(not curRingNumber > self.mapSize.value):
                    prevType = curNode.getNorthEastNode().getTileType()
                    curNode = curNode.getNorthEastNode().getNorthNode()
                    sameTypeChance = 8


                    numTilesInRing = curRingNumber * 6
                    curTileNum = 0
            else:
                curNode = self.__iterateThroughNodes(curNode, curRingNumber, curTileNum, numTilesInRing)

                

    def __populateRandomSettings(self):
        curNode = self.centerNode
        biomeInt = self.seed.getNextBiomeInt()
        biome = self.tileTypes.get_tile_name_by_key(biomeInt)
        while(self.settings.findExcludedType(biome)):
            biomeInt = self.seed.getNextBiomeInt()
            biome = self.tileTypes.get_tile_name_by_key(biomeInt)
        curNode.setTileType(biome)
        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6
        curNode = curNode.getNorthNode()
        while(curRingNumber < self.mapSize.value + 1):
            curTileNum += 1
            biomeInt = self.seed.getNextBiomeInt()
            biome = self.tileTypes.get_tile_name_by_key(biomeInt)
            while(self.settings.findExcludedType(biome)):
                biomeInt = self.seed.getNextBiomeInt()
                biome = self.tileTypes.get_tile_name_by_key(biomeInt)
            curNode.setTileType(biome)
            if(curTileNum == numTilesInRing):
                curRingNumber += 1
                if(not curRingNumber > self.mapSize.value):
                    prevType = curNode.getNorthEastNode().getTileType()
                    curNode = curNode.getNorthEastNode().getNorthNode()

                    numTilesInRing = curRingNumber * 6
                    curTileNum = 0
            else:
                curNode = self.__iterateThroughNodes(curNode, curRingNumber, curTileNum, numTilesInRing)


    def searchByPositionVector(self, vector:QPoint) -> HextileNode:
        vecX = vector.x()
        vecY = vector.y()
        radius = 50
        points = []
        
        points.append(vector)
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= radius:
                    x = int(vecX + dx)
                    y = int(vecY + dy)
                    points.append(QPoint(x, y))

        for i in range(0, len(self.tile_list)):
            curTile = self.tile_list[i]
            curVector = curTile.getPositionVector()
            curPoint = QPoint(int(curVector[0]),int(curVector[1]))
            if(curPoint in points):
                return curTile
        return None

    def saveMap(self, map_name:str):
        cur_node = self.centerNode
        cur_record = cur_node.getTileRecord()
        cur_tokens_list = []
        all_tiles_dict = {}
        cur_tile_pos_key = 0
        all_tiles_dict[str(cur_tile_pos_key)] = {}
        for token in cur_record.get_all_tokens():
            token_dict = token.get_token_dict()
            if(token.get_default_status):
                abrev_dict = {
                    token_dict["name"]: {
                        "type": token_dict["token_type"],
                        "key": token_dict["key"],
                        "x_position": token_dict["x_position"],
                        "y_position": token_dict["y_position"]
                    }
                }
                cur_tokens_list.append(abrev_dict)
            else:
                token_dict = token.get_token_dict()
                cur_tokens_list.append(token_dict)
        all_tiles_dict[str(cur_tile_pos_key)]["tokens"] = cur_tokens_list
        all_tiles_dict[str(cur_tile_pos_key)]["type_str"] = cur_record.get_tile_type()
        all_tiles_dict[str(cur_tile_pos_key)]["type_key"] = self.tileTypes.get_tile_key_by_name(cur_record.get_tile_type())



        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6
        cur_node = cur_node.getNorthNode()
        while(curRingNumber < self.mapSize.value + 1):
            curTileNum += 1
            cur_tokens_list = []
            cur_tile_pos_key += 1
            all_tiles_dict[str(cur_tile_pos_key)] = {}
            for token in cur_record.get_all_tokens():
                token_dict = token.get_token_dict()
                if(token.get_default_status):
                    abrev_dict = {
                        token_dict["name"]: {
                            "type": token_dict["token_type"],
                            "key": token_dict["key"],
                            "x_position": token_dict["x_position"],
                            "y_position": token_dict["y_position"],
                            "modified": False
                        }
                    }
                    cur_tokens_list.append(abrev_dict)
                else:
                    token_dict = token.get_token_dict()
                    token_dict["modified"] = True
                    cur_tokens_list.append(token_dict)
            all_tiles_dict[str(cur_tile_pos_key)]["tokens"] = cur_tokens_list
            all_tiles_dict[str(cur_tile_pos_key)]["type_str"] = cur_record.get_tile_type()
            all_tiles_dict[str(cur_tile_pos_key)]["type_key"] = self.tileTypes.get_tile_key_by_name(cur_record.get_tile_type())
            if(curTileNum == numTilesInRing):
                curRingNumber += 1
                if(not curRingNumber > self.mapSize.value):
                    cur_node = cur_node.getNorthEastNode().getNorthNode()
                    cur_record = cur_node.getTileRecord()
                    numTilesInRing = curRingNumber * 6
                    curTileNum = 0
            else:
                cur_node = self.__iterateThroughNodes(cur_node, curRingNumber, curTileNum, numTilesInRing)
                cur_record = cur_node.getTileRecord()

        final_dict = {map_name: all_tiles_dict}

        self.logger_ref.change_save_path("logfiles/" + map_name + ".txt")
        self.logger_ref.save_log()
        with open(self.JSON_SAVE_FILE, 'w') as file: 
            json.dump(final_dict, file, indent=4)



    def loadSavedMap(self, map_name:str):
        map_dict = self.saved_maps.find_map_by_name(map_name)
        self.__createMap(len(map_dict))
        curNode = self.centerNode
        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6

        dict_pos = 0

        tile_type = map_dict[str(dict_pos)]["type_str"]

        curNode.setTileType(tile_type)

        record_key = 0
        tokens = map_dict[str(dict_pos)]["tokens"]
        #def __init__(self, token_dict:dict, token_type:TokenTypes, record_key:int, position=(0,0)):
        curRecord = curNode.getTileRecord()
        for token in tokens:           
            record_key += 1
            for name in token: 
                type_str = token[name]["type"]
                token_type = self.__findTokenTypeFromStr(token[name]["type"])
                token_type_ref = self.__findTokenRefFromType(token_type)
                token_record = TokenRecord(self.logger_ref, token_type_ref.get_token_by_name(name), token_type, record_key, position=(token[name]["x_position"], token[name]["y_position"]))

                self.tokens_on_map.append(token_record)

                match(token_type):
                    case TokenTypes.PLAYER_CHARACTERS:
                        curRecord.add_player_character(token_record)
                    case TokenTypes.NON_PLAYER_CHARACTERS:
                        curRecord.add_nonplayer_character(token_record)
                    case TokenTypes.ANIMALS:
                        curRecord.add_animal_token(token_record)
                    case TokenTypes.MONSTERS:
                        curRecord.add_monster_token(token_record)
                    case TokenTypes.BUILDINGS:
                        curRecord.add_building_token(token_record)
                    case TokenTypes.STRUCTURES:
                        curRecord.add_structure_token(token_record)
                    case TokenTypes.NATURE:
                        curRecord.add_nature_token(token_record)

        curNode = curNode.getNorthNode()

        dict_pos += 1

        while(str(dict_pos) in map_dict):
            curTileNum += 1
            tile_type = map_dict[str(dict_pos)]["type_str"]
            tokens = map_dict[str(dict_pos)]["tokens"]
            dict_pos += 1
            curNode.setTileType(tile_type)
            curRecord = curNode.getTileRecord()
            for token in tokens:           
                record_key += 1
                for name in token:
                    token_type = self.__findTokenTypeFromStr(token[name]["type"])
                    token_type_ref = self.__findTokenRefFromType(token_type)
                    token_record = TokenRecord(self.logger_ref, token_type_ref.get_token_by_name(name), token_type, record_key, position=(token[name]["x_position"], token[name]["y_position"]))

                    self.tokens_on_map.append(token_record)

                    match(token_type):
                        case TokenTypes.PLAYER_CHARACTERS:
                            curRecord.add_player_character(token_record)
                        case TokenTypes.NON_PLAYER_CHARACTERS:
                            curRecord.add_nonplayer_character(token_record)
                        case TokenTypes.ANIMALS:
                            curRecord.add_animal_token(token_record)
                        case TokenTypes.MONSTERS:
                            curRecord.add_monster_token(token_record)
                        case TokenTypes.BUILDINGS:
                            curRecord.add_building_token(token_record)
                        case TokenTypes.STRUCTURES:
                            curRecord.add_structure_token(token_record)
                        case TokenTypes.NATURE:
                            curRecord.add_nature_token(token_record)

            if(curTileNum == numTilesInRing):
                curRingNumber += 1
                if(not curRingNumber > len(map_dict)):
                    curNode = curNode.getNorthEastNode().getNorthNode()

                    numTilesInRing = curRingNumber * 6
                    curTileNum = 0
            else:
                curNode = self.__iterateThroughNodes(curNode, curRingNumber, curTileNum, numTilesInRing)

