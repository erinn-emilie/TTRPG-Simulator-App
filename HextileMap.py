from TileTypes import TileTypes
from MapSizes import MapSizes
from Seed import Seed
from TileRecord import TileRecord
from HextileNode import HextileNode


class HextileMap():
    def __init__(self, tileTypesRef, settingsRef):
        self.tileTypes = tileTypesRef
        self.settings = settingsRef
        self.generateMap()

    def generateMap(self):
        self.mapSize = self.settings.getMapSize()
        self.centerNode = None
        self.seed = self.settings.getSeedRef()
        self.__createMap()
        self.__populateMapGenericSettings()

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

        while(curRingNumber < self.mapSize.value):
            curTileNum += 1
            if(curNode.getNorthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthNode(newNode)
                newNode.setSouthNode(curNode)
            if(curNode.getNorthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthEastNode(newNode)
                newNode.setSouthWestNode(curNode)
            if(curNode.getSouthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthEastNode(newNode)
                newNode.setNorthWestNode(curNode)
            if(curNode.getSouthNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthNode(newNode)
                newNode.setNorthNode(curNode)
            if(curNode.getSouthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setSouthWestNode(newNode)
                newNode.setNorthEastNode(curNode)
            if(curNode.getNorthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber+1)
                curNode.setNorthWestNode(newNode)
                newNode.setSouthEastNode(curNode)

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
        newBiomeValue = -1
        newBiomeName = ""
        while(True):
            posBiome = self.seed.getNextBiomeInt()
            posName = self.tileTypes.getTileNameByKey(posBiome)
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
            if(self.seed.getChanceInt() <= sameTypeChance):
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