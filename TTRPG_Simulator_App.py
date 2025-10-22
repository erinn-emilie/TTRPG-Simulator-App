from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDockWidget,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QScrollArea
)
from enum import Enum
import random

class TileTypes(Enum):
    NONE = -1
    PLAINS = 0
    MOUNTAIN = 1
    SWAMP = 2
    FOREST = 3
    DESERT = 4
    HILLS = 5
    ICELAND = 6
    JUNGLE = 7
    TUNDRA = 8
    WASTELAND = 9

    def getPngStrFromTileType(tileType) -> str:
        match(tileType):
            case TileTypes.PLAINS:
                return "yellowhextile.png"
            case TileTypes.MOUNTAIN:
                return "brownhextile.png"
            case TileTypes.SWAMP:
                return "blackhextile.png"
            case TileTypes.FOREST:
                return "greenhextile.png"
            case TileTypes.DESERT:
                return "orangehextile.png"
            case TileTypes.HILLS:
                return "lightgreenhextile.png"
            case TileTypes.ICELAND:
                return "lightbluehextile.png"
            case TileTypes.JUNGLE:
                return "purplehextile.png"
            case TileTypes.TUNDRA:
                return "darkbluehextile.png"
            case TileTypes.WASTELAND:
                return "redhextile.png"
            case _:
                return "greyhextile.png"

    def getTileTypeFromNum(value:int):
        match(value):
            case 0:
                return TileTypes.PLAINS
            case 1:
                return TileTypes.MOUNTAIN
            case 2:
                return TileTypes.SWAMP
            case 3: 
                return TileTypes.FOREST
            case 4:
                return TileTypes.DESERT
            case 5:
                return TileTypes.HILLS
            case 6:
                return TileTypes.ICELAND
            case 7:
                return TileTypes.SWAMP
            case 8:
                return TileTypes.TUNDRA
            case 9: 
                return TileTypes.WASTELAND
            case _:
                return TileTypes.NONE


class MapSizes(Enum):
    XSMALL = 2
    SMALL = 4
    MEDIUM = 6
    LARGE = 8
    XLARGE = 10

class Seed():
    def __init__(self, num = 0):
        if(num < 100000):
            num = random.randint(100000,999999)
        random.seed(num)

    def getNextBiomeInt(self):
        return random.randint(0,9)

    def getChanceInt(self):
        return random.randint(1,100)
    


class TileRecord():
    def __init__(self, tileType:TileTypes):
        self.tileType = tileType

    def getTileType(self) -> TileTypes:
        return self.tileType

    def setTileType(self, newTileType:TileTypes):
        self.tileType = newTileType

class HextileNode():
    def __init__(self, north = None, south = None, southeast = None, northeast = None, southwest = None, northwest = None, tileRecord = None, positionIdx = -1):
        self.north = north
        self.northeast = northeast
        self.northwest = northwest
        self.south = south
        self.southeast = southeast
        self.southwest = southwest
        self.tileRecord = tileRecord
        self.positionIdx = positionIdx
        self.placed = False

    def getPlacedStatus(self):
        return self.placed

    def setPlacedStatus(self, status):
        self.placed = status

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


    

class HextileMap():
    def __init__(self, mapSize = MapSizes.XSMALL):
        self.mapSize = mapSize
        self.centerNode = None
        self.seed = Seed()
        self.__createMap()
        self.__populateMapGenericSettings()

    def getCenterNode(self) -> HextileNode:
        return self.centerNode

    def getMapSize(self) -> MapSizes:
        return self.mapSize

    def __createBlankNode(self, position:int) -> HextileNode:
        tileRec = TileRecord(TileTypes.NONE)
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode

    def __createNodeWithSetType(self, position:int, tileType:TileTypes) -> HextileNode: 
        tileRec = TileRecord(tileType)
        newNode = HextileNode(tileRecord=tileRec, positionIdx=position)
        return newNode

    def __addRandTypeToNode(self, node:HextileNode) -> TileTypes:
        value = self.seed.getNextBiomeInt()
        tileType = TileTypes.getTileTypeFromNum(value)
        node.setTileType(tileType)
        return tileType

    def __createMap(self):
        self.centerNode = self.__createBlankNode(0)
        curNode = self.centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0

        while(curRingNumber <= self.mapSize.value):
            curTileNum += 1
            if(curNode.getNorthNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
                curNode.setNorthNode(newNode)
                newNode.setSouthNode(curNode)
            if(curNode.getNorthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
                curNode.setNorthEastNode(newNode)
                newNode.setSouthWestNode(curNode)
            if(curNode.getSouthEastNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
                curNode.setSouthEastNode(newNode)
                newNode.setNorthWestNode(curNode)
            if(curNode.getSouthNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
                curNode.setSouthNode(newNode)
                newNode.setNorthNode(curNode)
            if(curNode.getSouthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
                curNode.setSouthWestNode(newNode)
                newNode.setNorthEastNode(curNode)
            if(curNode.getNorthWestNode() == None):
                newNode = self.__createBlankNode(curRingNumber)
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
                nextNode = curNode.getSouthEastNode()

                if(nextNode.getPositionIdx() != curRingNumber-1 or curNode.getNorthNode().getPositionIdx() == curRingNumber-1):
                    nextNode = curNode.getSouthNode()
                    if(nextNode.getPositionIdx() != curRingNumber-1):
                        nextNode = curNode.getSouthWestNode()
                        if(nextNode.getPositionIdx() != curRingNumber-1):
                            nextNode = curNode.getNorthWestNode()
                            if(nextNode.getPositionIdx() != curRingNumber-1):
                                nextNode = curNode.getNorthNode()
                                if(nextNode.getPositionIdx() != curRingNumber-1):
                                    nextNode = curNode.getNorthEastNode()
                curNode = nextNode

    def __populateMapGenericSettings(self):
        curNode = self.centerNode
        prevType = self.__addRandTypeToNode(curNode)
        sameTypeChance = 95

        curRingNumber = 1
        curTileNum = 0
        numTilesInRing = 6
        curNode = curNode.getNorthNode()
        while(curRingNumber <= self.mapSize.value):
            if(self.seed.getChanceInt() <= sameTypeChance):
                curNode.setTileType(prevType)
                sameTypeChance -= 5
            else:
                curType = self.__addRandTypeToNode(curNode)
                if(curType == prevType):
                    sameTypeChance -=5
                else:
                    sameTypeChance = 95
                    prevType = curType

            if(curTileNum == numTilesInRing):
                curNode = curNode.getNorthEastNode().getNorthNode()
                curRingNumber += 1
                numTilesInRing = curRingNumber * 6
                curTileNum = 0
            else:
                curTileNum += 1
                nextNode = curNode.getSouthEastNode()
                if(nextNode.getPositionIdx() != curRingNumber-1 or curNode.getNorthNode().getPositionIdx() == curRingNumber-1):
                    nextNode = curNode.getSouthNode()
                    if(nextNode.getPositionIdx() != curRingNumber-1):
                        nextNode = curNode.getSouthWestNode()
                        if(nextNode.getPositionIdx() != curRingNumber-1):
                            nextNode = curNode.getNorthWestNode()
                            if(nextNode.getPositionIdx() != curRingNumber-1):
                                nextNode = curNode.getNorthNode()
                                if(nextNode.getPositionIdx() != curRingNumber-1):
                                    nextNode = curNode.getNorthEastNode()
                curNode = nextNode





              

        



class ToolboxHome(QMainWindow):
    #self has title, mainWidget, mapWidget, mapLayout, hextileMap, mapSettingsToolBar, navbar, scroll, settingsMenuWidget
    def __init__(self):
        super().__init__()            
        self.title = "TTRPG Simulator"
        self.setWindowTitle(self.title)

        self.mainWidget = QWidget()
        self.mapLayout = QVBoxLayout()
        self.mapWidget = QWidget()
        self.hextileMap = HextileMap()

        self.__layoutTiles()
        self.mapLayout.addWidget(self.mapWidget)
        self.mainWidget.setLayout(self.mapLayout)
        self.mapWidget.setMinimumSize(2000,2000)

        self.mapSettingsToolBar = QToolBar()
        self.mapSettingsToolBar.setStyleSheet("background-color: lightblue")
        self.mapSettingsToolBar.setMinimumHeight(100)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.mainWidget)

        self.navbar = QDockWidget(self)
        self.navbar.setDockLocation(Qt.DockWidgetArea.RightDockWidgetArea)
        self.navbar.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.navbar.setStyleSheet("background-color: yellow")
        self.navbar.setMinimumHeight(500)

        extraSettingsButton = QAction("Configure Extra Settings", self)
        extraSettingsButton.triggered.connect(self.__openExtraSettings)
        self.mapSettingsToolBar.addAction(extraSettingsButton)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mapSettingsToolBar)
        self.mainWidget.setStyleSheet("background-color: pink")
        self.setCentralWidget(self.scroll)

    def __openExtraSettings(self, s):
        self.settingsMenuWidget = QWidget()
        self.settingsMenuWidget.setStyleSheet("background-color: purple")
        self.settingsMenuWidget.setWindowTitle("Settings")
        self.settingsMenuWidget.show()


    def __layoutTiles(self):

        centerNode = self.hextileMap.getCenterNode()
        pivotNode = centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        pivX = 500    
        pivY = 500

        newLabel = self.__createLabel(pivotNode.getTileType())
        newLabel.move(pivX, pivY)
        pivotNode.setPlacedStatus(True)
        

        while(curRingNumber <= self.hextileMap.getMapSize().value):
            curTileNum += 1
            north = pivotNode.getNorthNode()
            south = pivotNode.getSouthNode()
            northeast = pivotNode.getNorthEastNode()
            northwest = pivotNode.getNorthWestNode()
            southeast = pivotNode.getSouthEastNode()
            southwest = pivotNode.getSouthWestNode()
            

            if(not north.getPlacedStatus()):
                newLabel = self.__createLabel(north.getTileType())
                newLabel.move(pivX, pivY-200)
                north.setPlacedStatus(True)
            if(not south.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX, pivY+200)
                south.setPlacedStatus(True)
            if(not northeast.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX+200, pivY-100)
                northeast.setPlacedStatus(True)
            if(not northwest.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX-200, pivY-100)
                northwest.setPlacedStatus(True)
            if(not southeast.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX+200, pivY+100)
                southeast.setPlacedStatus(True)
            if(not southwest.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX-200, pivY+100)
                southwest.setPlacedStatus(True)

            if(curTileNum == numTilesInRing):
                if(curRingNumber == 0):
                    pivotNode = pivotNode.getNorthNode()
                    pivY = pivY - 200
                else:
                    pivotNode = pivotNode.getNorthEastNode().getNorthNode()
                    pivX = pivX + 200
                    pivY = pivY - 400
                curRingNumber += 1
                numTilesInRing = curRingNumber * 6
                curTileNum = 0
            else:
                nextNode = pivotNode.getSouthEastNode()
                posX = pivX + 200
                posY = pivY + 100
                
                if(nextNode.getPositionIdx() != curRingNumber-1 or pivotNode.getNorthNode().getPositionIdx() == curRingNumber-1):
                    nextNode = pivotNode.getSouthNode()
                    posX = pivX
                    posY = pivY + 200
                    if(nextNode.getPositionIdx() != curRingNumber-1):
                        nextNode = pivotNode.getSouthWestNode()
                        posX = pivX - 200
                        posY = pivY + 100
                        if(nextNode.getPositionIdx() != curRingNumber-1):
                            nextNode = pivotNode.getNorthWestNode()
                            posX = pivX - 200
                            posY = pivY - 200
                            if(nextNode.getPositionIdx() != curRingNumber-1):
                                nextNode = pivotNode.getNorthNode()
                                posX = pivX
                                posY = pivY - 200
                                if(nextNode.getPositionIdx() != curRingNumber-1):
                                    nextNode = pivotNode.getNorthEastNode()
                                    posX = pivX + 200
                                    posY = pivY - 200
                pivX = posX
                pivY = posY
                pivotNode = nextNode

            


    def __createLabel(self, tileType:TileTypes) -> QLabel:
        label = QLabel(self.mapWidget)
        pngStr = ''
        pngStr = TileTypes.getPngStrFromTileType(tileType)
        pixmap = QPixmap(pngStr)
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)
        label.setScaledContents(True)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return label




if __name__ == "__main__":
    app = QApplication([])

    window = ToolboxHome()
    window.show()

    app.exec()