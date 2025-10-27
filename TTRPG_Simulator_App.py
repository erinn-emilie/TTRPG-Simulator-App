from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QScrollArea,
    QLineEdit,
    QPushButton,
    QGroupBox
    )

from TileTypes import TileTypes
from HextileMap import HextileMap
from MapSizes import MapSizes
from Settings import Settings

                   

class Toolbox():
    def __init__(self):
        self.tileTypesRef = TileTypes()
        self.settingsRef = Settings()
        self.hextileMapRef = HextileMap(self.tileTypesRef, self.settingsRef)

    def getTileTypesRef(self):
        return self.tileTypesRef

    def getHextileMapRef(self):
        return self.hextileMapRef

    def getSettingsRef(self):
        return self.settingsRef


class SettingsMenu(QWidget):
    def __init__(self, settingsRef:Settings, tileTypes:TileTypes):
        super().__init__()

        self.settingsRef = settingsRef
        self.tileTypes = tileTypes
        self.posMapSize = self.settingsRef.getMapSize()

        self.layout = QVBoxLayout()

        self.mapsizeDropdown = QComboBox()
        self.mapsizeDropdownOptions = ["Extra Small", "Small", "Medium", "Large", "Extra Large"]
        self.mapsizeOptionIdx = 2
        self.mapsizeDropdown.addItems(self.mapsizeDropdownOptions)
        self.mapsizeDropdown.activated.connect(self.__onDDChanged)
        self.mapsizeDropdown.setCurrentIndex(self.mapsizeOptionIdx)
        self.mapsizeDropdown.setMaximumSize(100,100)

        self.checkboxGroup = QGroupBox("Included Biomes")
        self.checkboxLayout = QVBoxLayout()
        self.checkboxGroup.setLayout(self.checkboxLayout)

        tileNamesList = self.tileTypes.getTileNamesList()
        for name in tileNamesList:
            newCheckBox = QCheckBox(text=str(name), parent=self)
            if(self.settingsRef.findExcludedType(name.upper())):
                newCheckBox.setChecked(True)
            else:
                newCheckBox.setChecked(False)
            newCheckBox.setStyleSheet("""
                QCheckBox::indicator:unchecked {
                    background-color: green;
                }
                QCheckBox::indicator:checked {
                    background-color: red;
                }
            """)   
            newCheckBox.toggled.connect(self.__onCBStateChange)
            self.checkboxLayout.addWidget(newCheckBox)

        self.saveSettingButton = QPushButton("Save Settings", self)
        self.saveSettingButton.clicked.connect(self.__saveSettings)


        self.layout.addWidget(self.checkboxGroup)
        self.layout.addWidget(self.mapsizeDropdown)
        self.layout.addWidget(self.saveSettingButton)
        self.setLayout(self.layout)


    def __onDDChanged(self, index):
        self.posMapSize = MapSizes.getMapSizeFromStr(self.mapsizeDropdownOptions[index])

    def __onCBStateChange(self, state):
        checkbox = self.sender()
        if(state):
            self.settingsRef.addExcludedType(checkbox.text().upper())
        else: 
            self.settingsRef.removeExcludedType(checkbox.text().upper())

    def __saveSettings(self):
        self.settingsRef.setMapSize(self.posMapSize)
        self.close()




        


        
class ToolboxHome(QMainWindow):
    #self has title, mainWidget, mapWidget, mapLayout, hextileMap, mapSettingsToolBar, navbar, scroll, settingsMenuWidget
    def __init__(self, toolboxRef:Toolbox):
        super().__init__()            
        self.title = "TTRPG Simulator"
        self.setWindowTitle(self.title)

        self.mainWidget = QWidget()
        self.mapLayout = QVBoxLayout()
        self.mapWidget = QWidget()
        self.toolbox = toolboxRef
        self.hextileMap = self.toolbox.getHextileMapRef()
        self.tileTypes = self.toolbox.getTileTypesRef()
        self.settingsRef = self.toolbox.getSettingsRef()

        self.__layoutTiles()
        self.mapLayout.addWidget(self.mapWidget)
        self.mainWidget.setLayout(self.mapLayout)
        self.mapWidget.setMinimumSize(3000,3000)

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

        self.extraSettingsButton = QAction("Configure Extra Settings", self)
        self.extraSettingsButton.triggered.connect(self.__openExtraSettings)
        self.mapSettingsToolBar.addAction(self.extraSettingsButton)

        self.seedInput = QLineEdit("Enter in a map seed here!")
        self.seedInput.textEdited.connect(self.__recieveSeedInput)
        self.mapSettingsToolBar.addWidget(self.seedInput)

        self.generateMapButton = QAction("GenerateMap", self)
        self.generateMapButton.triggered.connect(self.__generateMap)
        self.mapSettingsToolBar.addAction(self.generateMapButton)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mapSettingsToolBar)
        self.mainWidget.setStyleSheet("background-color: pink")
        self.setCentralWidget(self.scroll)

    def __openExtraSettings(self):
        self.settingsMenuWidget = SettingsMenu(self.settingsRef, self.tileTypes)
        self.settingsMenuWidget.setParent(None)  # ensure top-level
        self.settingsMenuWidget.setWindowFlags(Qt.WindowType.Window)
        self.settingsMenuWidget.setStyleSheet("background-color: white")
        self.settingsMenuWidget.setWindowTitle("Settings")
        self.settingsMenuWidget.show()


    def __recieveSeedInput(self, seedStr):
        try:
            seed = int(seedStr)
            self.settingsRef.setNewSeed(seed)
        except ValueError:
            self.settingsRef.setNewRandomSeed()

    def __generateMap(self):
        self.mapLayout.removeWidget(self.mapWidget)
        self.mapWidget = QWidget()
        self.mapWidget.setMinimumSize(3000,3000)
        self.hextileMap.generateMap()
        self.__layoutTiles()
        self.mapLayout.addWidget(self.mapWidget)


    def __layoutTiles(self):
        centerNode = self.hextileMap.getCenterNode()
        pivotNode = centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        pivX = 1200    
        pivY = 1200

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
            

            if(north != None and not north.getPlacedStatus()):
                newLabel = self.__createLabel(north.getTileType())
                newLabel.move(pivX, pivY-200)
                north.setPlacedStatus(True)
            if(south != None and not south.getPlacedStatus()):
                newLabel = self.__createLabel(south.getTileType())
                newLabel.move(pivX, pivY+200)
                south.setPlacedStatus(True)
            if(northeast != None and not northeast.getPlacedStatus()):
                newLabel = self.__createLabel(northeast.getTileType())
                newLabel.move(pivX+200, pivY-100)
                northeast.setPlacedStatus(True)
            if(northwest != None and not northwest.getPlacedStatus()):
                newLabel = self.__createLabel(northwest.getTileType())
                newLabel.move(pivX-200, pivY-100)
                northwest.setPlacedStatus(True)
            if(southeast != None and not southeast.getPlacedStatus()):
                newLabel = self.__createLabel(southeast.getTileType())
                newLabel.move(pivX+200, pivY+100)
                southeast.setPlacedStatus(True)
            if(southwest != None and not southwest.getPlacedStatus()):
                newLabel = self.__createLabel(southwest.getTileType())
                newLabel.move(pivX-200, pivY+100)
                southwest.setPlacedStatus(True)

            if(curTileNum == numTilesInRing):
                if(curRingNumber == 0):
                    pivotNode = pivotNode.getNorthNode()
                    pivY = pivY - 200
                elif(curRingNumber != self.hextileMap.getMapSize().value):
                    pivotNode = pivotNode.getNorthEastNode().getNorthNode()
                    pivX = pivX + 200
                    pivY = pivY - 300
                curRingNumber += 1
                numTilesInRing = curRingNumber * 6
                curTileNum = 0
            else:
                nextNode = pivotNode.getSouthEastNode()
                posX = pivX + 200
                posY = pivY + 100
                
                if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                    nextNode = pivotNode.getSouthNode()
                    posX = pivX
                    posY = pivY + 200
                    if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                        nextNode = pivotNode.getSouthWestNode()
                        posX = pivX - 200
                        posY = pivY + 100
                        if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                            nextNode = pivotNode.getNorthWestNode()
                            posX = pivX - 200
                            posY = pivY - 100
                            if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                                nextNode = pivotNode.getNorthNode()
                                posX = pivX
                                posY = pivY - 200
                                if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                                    nextNode = pivotNode.getNorthEastNode()
                                    posX = pivX + 200
                                    posY = pivY - 100
                pivX = posX
                pivY = posY
                pivotNode = nextNode

            


    def __createLabel(self, tileType:TileTypes) -> QLabel:
        label = QLabel(self.mapWidget)
        pngStr = ''
        pngStr = self.tileTypes.getDefaultTileAssetByName(tileType)
        pixmap = QPixmap(pngStr)
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)
        label.setScaledContents(True)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return label




if __name__ == "__main__":
    app = QApplication([])
    toolbox = Toolbox()

    window = ToolboxHome(toolbox)
    window.show()

    app.exec()