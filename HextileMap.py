from TileTypes import TileTypes
from Enums.MapSizes import MapSizes
from Seed import Seed
from TileRecord import TileRecord
from HextileNode import HextileNode
from PyQt6.QtCore import Qt, QPoint, QPointF
import math


class HextileMap():
    def __init__(self, tileTypesRef, settingsRef):
        self.tileTypes = tileTypesRef
        self.settings = settingsRef
        self.tileList = []
        self.generateMap()

    def generateMap(self):
        self.mapSize = self.settings.getMapSize()
        self.centerNode = None
        self.seed = self.settings.getSeedRef()
        self.totalwater = self.__setTotalRivers()
        self.__createMap()
        #self.__populateRandomSettings()
        self.__populateMapGenericSettings()


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

    def __createBlankNode(self, position:int) -> HextileNode:
        tileRec = TileRecord("NONE")
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode

    def __createNodeWithSetType(self, position:int, tileType:str) -> HextileNode: 
        tileRec = TileRecord(tileType)
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode


    def __createMap(self):
        self.centerNode = self.__createBlankNode(0)
        curNode = self.centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        self.tileList.append(curNode)
        while(curRingNumber < self.mapSize.value):
            curTileNum += 1
            if(curNode.getNorthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthNode(newNode)
                newNode.setSouthNode(curNode)
                self.tileList.append(newNode)
            if(curNode.getNorthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthEastNode(newNode)
                newNode.setSouthWestNode(curNode)
                self.tileList.append(newNode)
            if(curNode.getSouthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthEastNode(newNode)
                newNode.setNorthWestNode(curNode)
                self.tileList.append(newNode)
            if(curNode.getSouthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthNode(newNode)
                newNode.setNorthNode(curNode)
                self.tileList.append(newNode)
            if(curNode.getSouthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthWestNode(newNode)
                newNode.setNorthEastNode(curNode)
                self.tileList.append(newNode)
            if(curNode.getNorthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthWestNode(newNode)
                newNode.setSouthEastNode(curNode)
                self.tileList.append(newNode)

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
            posName = self.tileTypes.getTileNameByKey(posBiome)
            while(posName == "WATER" and self.totalwater == 0):
                posBiome = self.seed.getNextBiomeInt()
                posName = self.tileTypes.getTileNameByKey(posBiome)
            if(posName == "WATER"):
                self.__setUpWater(node)
                self.totalwater -= 1
            while(self.settings.findExcludedType(posName)):
                posBiome = self.seed.getNextBiomeInt()
                posName = self.tileTypes.getTileNameByKey(posBiome)

            totalValue = 0
            for i in range(0, len(typeArr)):
                curBiome = self.tileTypes.getTileKeyByName(typeArr[i])
                totalValue = totalValue + self.tileTypes.getTileWeightByKey(curBiome, posBiome)
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




    def __populateMapGenericSettings(self):
        curNode = self.centerNode
        biomeInt = self.seed.getNextBiomeInt()
        prevType = self.tileTypes.getTileNameByKey(biomeInt)
        while(self.settings.findExcludedType(prevType)):
            biomeInt = self.seed.getNextBiomeInt()
            prevType = self.tileTypes.getTileNameByKey(biomeInt)
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
        biome = self.tileTypes.getTileNameByKey(biomeInt)
        while(self.settings.findExcludedType(biome)):
            biomeInt = self.seed.getNextBiomeInt()
            biome = self.tileTypes.getTileNameByKey(biomeInt)
        curNode.setTileType(biome)
        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6
        curNode = curNode.getNorthNode()
        while(curRingNumber < self.mapSize.value + 1):
            curTileNum += 1
            biomeInt = self.seed.getNextBiomeInt()
            biome = self.tileTypes.getTileNameByKey(biomeInt)
            while(self.settings.findExcludedType(biome)):
                biomeInt = self.seed.getNextBiomeInt()
                biome = self.tileTypes.getTileNameByKey(biomeInt)
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

        for i in range(0, len(self.tileList)):
            curTile = self.tileList[i]
            curVector = curTile.getPositionVector()
            curPoint = QPoint(int(curVector[0]),int(curVector[1]))
            if(curPoint in points):
                return curTile
        return None