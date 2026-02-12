from toolbox.TileTypes import TileTypes
from TileRecord import TileRecord

class HextileNode():
    def __init__(self, north = None, south = None, southeast = None, northeast = None, southwest = None, northwest = None, tileRecord = None, positionIdx = -1, positionVector = ()):
        self.north = north
        self.northeast = northeast
        self.northwest = northwest
        self.south = south
        self.southeast = southeast
        self.southwest = southwest
        self.tileRecord = tileRecord
        self.positionIdx = positionIdx
        self.positionVector = positionVector
        self.placed = False

    def getPlacedStatus(self):
        return self.placed

    def setPlacedStatus(self, status):
        self.placed = status

    def getPositionVector(self) -> tuple:
        return self.positionVector

    def setPositionVector(self, vector:tuple):
        self.positionVector = vector

    def getTileRecord(self) -> TileRecord:
        return self.tileRecord

    def getTileType(self) -> TileTypes:
        return self.tileRecord.getTileType()
    
    def setTileType(self, tileType:TileTypes):
        self.tileRecord.setTileType(tileType)

    def getPositionIdx(self):
        return self.positionIdx

    def setTileRecord(self, newTileRecord:TileRecord):
        self.tileRecord = newTileRecord

    def getNorthNode(self):
        return self.north

    def setNorthNode(self, newNode):
        self.north = newNode

    def getNorthEastNode(self):
        return self.northeast

    def setNorthEastNode(self, newNode):
        self.northeast = newNode

    def getNorthWestNode(self):
        return self.northwest

    def setNorthWestNode(self, newNode):
        self.northwest = newNode

    def getSouthNode(self):
        return self.south

    def setSouthNode(self, newNode):
        self.south = newNode

    def getSouthEastNode(self):
        return self.southeast

    def setSouthEastNode(self, newNode):
        self.southeast = newNode

    def getSouthWestNode(self):
        return self.southwest

    def setSouthWestNode(self, newNode):
        self.southwest = newNode
