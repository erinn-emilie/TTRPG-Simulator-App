from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QAction, QPixmap, QMouseEvent, QPainter, QPen, QBrush
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
    QGroupBox,
    QListWidget,
    QFileDialog
    )

import os
from Toolbox import Toolbox
from TileTypes import TileTypes
from HextileMap import HextileMap
from HextileNode import HextileNode
from Enums.MapSizes import MapSizes
from Settings import Settings
from Creatures import Creatures
from SettingsMenu import SettingsMenu


class GridWindow(QMainWindow):
    def __init__(self, hexNode:HextileNode, creatures:Creatures):
        super().__init__()
        self.hexNode = hexNode
        self.creaturesRef = creatures

        self.title = "Grid Window"
        self.setWindowTitle(self.title)

        self.main_widget = QWidget()


        self.creatureBox = QDockWidget("Creature Box", self.main_widget)
        self.creatureBoxContainer = QWidget()
        self.creatureBoxLayout = QVBoxLayout(self.creatureBoxContainer)        

        self.addToken = QPushButton("Add Token")
        self.creatureBoxLayout.addWidget(self.addToken)

        self.creatureBox.setWidget(self.creatureBoxContainer)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def __populateCreatures(self):
        creaturesList = self.creaturesRef.getListOfCreatures()
        for creature in creaturesList:
            creatureLabel = QLabel(creature.getName())
            self.creatureBoxLayout.addWidget(creatureLabel)
        

class HexLabel(QLabel):
    def __init__(self, hexNode:HextileNode, toolbox:Toolbox, parent=None):
        super().__init__(parent=parent)
        self.hexNode = hexNode
        self.creaturesRef = toolbox.get_creatures_ref()
        self.gridWindow = GridWindow(self.hexNode, self.creaturesRef)

    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            self.gridWindow.show()





class GenericContainerWidget(QWidget):
    def __init__(self, tile_name:str, tile_list:list, tile_image_path:str):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        # make special label with stylesheet thats automatically disabled
        self.setStyleSheet("""
            background-color: pink;
        """)

        self.tileNamePromptLabel = QLabel("Tile Name:")
        self.tileNameLabel = QLineEdit(tile_name)
        self.tileNameLabel.setEnabled(False)
        self.tileNameLabel.setMaximumWidth(200)
        self.tileNamePromptLabel.setMaximumWidth(200)
        self.tileImagePixmap = QPixmap(tile_image_path)
        self.tileImageLabel = QLabel()
        self.tileImageLabel.setPixmap(self.tileImagePixmap)
        self.tileImageLabel.setScaledContents(True)
        self.tileImageLabel.setMaximumWidth(300)
        self.tileImageLabel.setMaximumHeight(300)
        self.tileNameRow = QHBoxLayout()
        self.tileNameRow.addWidget(self.tileNamePromptLabel)
        self.tileNameRow.addWidget(self.tileNameLabel)
        self.tileNameRow.addWidget(self.tileImageLabel)
        self.mainLayout.addLayout(self.tileNameRow)
        self.setLayout(self.mainLayout)

    def enable_tile_name_label(self):
        self.tileNameLabel.setEnabled(True)

    def disable_tile_name_label(self):
        self.tileNameLabel.setEnabled(False)

        

class CustomTilesWindow(QMainWindow):
    def __init__(self, toolboxRef:Toolbox):
        super().__init__()
        self.title = "Custom Tile Menu"
        self.setWindowTitle(self.title)
        self.toolbox = toolboxRef
        self.tileTypesRef = self.toolbox.get_tile_types_ref()

        self.main_widget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.tile_list = self.tileTypesRef.getTileNamesList()
        for tile in self.tile_list:
            image_path = self.tileTypesRef.getDefaultTileAssetByName(tile.upper())
            widget = GenericContainerWidget(tile, self.tile_list, image_path)
            self.mainLayout.addWidget(widget)
        self.addTileButton = QPushButton("Add New Tile")
        self.addTileButton.clicked.connect(self.__add_new_tile)
        self.mainLayout.addWidget(self.addTileButton)
        self.main_widget.setLayout(self.mainLayout)
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.main_widget)
        self.setCentralWidget(self.scroll)

    def __add_new_tile(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select a file to use as the image for your tile!")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            try:
                selected_files_list = file_dialog.selectedFiles()
                img_path = selected_files_list[0]
                img_name = os.path.basename(img_path)
                cur_dir = os.getcwd()
                asset_dir = os.path.join(cur_dir, "assets")
                asset_path = os.path.join(asset_dir, img_name)
                os.rename(img_path, asset_path)
            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")

            widget = GenericContainerWidget("New Tile", self.tile_list, asset_path)
            widget.enable_tile_name_label()
            self.mainLayout.addWidget(widget)



#Class derived from QMainWindow, this is the homepage of the whole app,
#where the map is generated and displayed.  
class ToolboxHomePage(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox):
        super().__init__()            
        window_title = "Tabletop Roleplaying Game Simulator"
        self.setWindowTitle(window_title)

        
        self.main_widget = QWidget()
        self.map_layout = QVBoxLayout()
        self.map_widget = QWidget()

        self.toolbox = toolbox_ref

        self.hextile_map_obj = self.toolbox.get_hextile_map_ref()
        self.tile_types_ref_obj = self.toolbox.get_tile_types_ref()
        self.settings_ref_obj = self.toolbox.get_settings_ref()


        self.__layout_tiles()

        #The map_layout contains the map widget, and the layout is given to the map widget
        self.map_layout.addWidget(self.map_widget)
        self.main_widget.setLayout(self.map_layout)

        #!!!
        #Keep for now, need to find a way to make the map fully scrollable and zoom in/out-able lol
        self.map_widget.setMinimumSize(3000,3000)

        # A bar across the top that holds a button for the user to open up custom
        # settings, a field for the user to enter a seed, and the generate map button
        self.map_settings_toolbar = QToolBar()
        # !!!
        # Looks terrible fix lol
        self.map_settings_toolbar.setStyleSheet("background-color: lightblue")
        self.map_settings_toolbar.setMinimumHeight(100)

        # !!!
        # Need to make a custom buttom class for buttons like this that 
        # have a set stylesheet adn stuff
        self.xtra_settings_btn = QPushButton("Configure Extra Settings", self)
        self.xtra_settings_btn.clicked.connect(self.__open_xtra_settings)
        self.map_settings_toolbar.addWidget(self.xtra_settings_btn)


        self.seed_input_field = QLineEdit("Enter in a map seed here!")
        self.seed_input_field.textEdited.connect(self.__recieve_seed_input)
        self.map_settings_toolbar.addWidget(self.seed_input_field)

        self.generate_map_btn = QPushButton("Generate Map", self)
        self.generate_map_btn.clicked.connect(self.__generate_map)
        self.map_settings_toolbar.addWidget(self.generate_map_btn)

        self.boxSelectButton = QPushButton("Box Select Tiles", self)
        self.map_settings_toolbar.addWidget(self.boxSelectButton)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.map_settings_toolbar)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.main_widget)

        self.navbar = QDockWidget("Navigation", self)
        self.navbar.setDockLocation(Qt.DockWidgetArea.RightDockWidgetArea)
        self.navbar.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.navbar.setMinimumHeight(500)


        self.navbarContainer = QWidget()
        self.navbarLayout = QVBoxLayout(self.navbarContainer)

        self.customTilesWindow = None

        self.customTilesButton = QPushButton("Custom Tiles", self.navbar)
        self.customPlayerButton = QPushButton("Custom Player Characters", self.navbar)
        self.customNonPlayerButton = QPushButton("Custom Non-Player Characters", self.navbar)
        self.customAnimalButton = QPushButton("Custom Animals", self.navbar)
        self.customMonsterButton = QPushButton("Custom Monsters", self.navbar)
        self.customBuildingButton = QPushButton("Custom Buildings", self.navbar)
        self.customStructuresButton = QPushButton("Custom Structures", self.navbar)

        self.navbarLayout.addWidget(self.customTilesButton)
        self.navbarLayout.addWidget(self.customPlayerButton)
        self.navbarLayout.addWidget(self.customNonPlayerButton)
        self.navbarLayout.addWidget(self.customAnimalButton)
        self.navbarLayout.addWidget(self.customMonsterButton)
        self.navbarLayout.addWidget(self.customBuildingButton)
        self.navbarLayout.addWidget(self.customStructuresButton)

        self.customTilesButton.clicked.connect(self.__showCustomTilesWindow)

        self.navbar.setWidget(self.navbarContainer)

        self.main_widget.setStyleSheet("background-color: pink")
        self.setCentralWidget(self.scroll)


    def __showCustomTilesWindow(self):
        if(self.customTilesWindow is None):
            self.customTilesWindow = CustomTilesWindow(self.toolbox)
        self.customTilesWindow.show()

    # creates a window of the custom class Settings Menu.
    # !!!
    # Should pass the Toolbox, also shouldn't set stylesheet here should set in the actual class
    def __open_xtra_settings(self):
        self.settings_menu_window = SettingsMenu(self.toolbox)
        self.settings_menu_window.show()


    def __recieve_seed_input(self, seed_str):
        try:
            seed = int(seed_str)
            self.settings_ref_obj.setNewSeed(seed)
        except ValueError:
            self.settings_ref_obj.setNewRandomSeed()

    def __generate_map(self):
        self.map_layout.removeWidget(self.map_widget)
        self.map_widget = QWidget()
        # !!!
        # Layout so bad need fixed
        self.map_widget.setMinimumSize(3000,3000)
        self.hextile_map_obj.generateMap()
        self.__layout_tiles()
        self.map_layout.addWidget(self.map_widget)


    def __layout_tiles(self):
        centerNode = self.hextile_map_obj.getCenterNode()
        pivotNode = centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        # !!!
        # This works for now but the placement of the tiles desperately (cant spell)
        # needs to be more dynamic as i have no idea how it would look on another screen
        # size with this configuration and also its just kinda shit practice
        pivX = 1200    
        pivY = 1200


        newLabel = self.__createLabel(pivotNode)
        newLabel.move(pivX, pivY)
        pivotNode.setPlacedStatus(True)
        posVecXOffset = 125
        posVecYOffset = 100
        pivotNode.setPositionVector((pivX + posVecXOffset, pivY + posVecYOffset))


        while(curRingNumber <= self.hextile_map_obj.getMapSize().value):
            curTileNum += 1
            north = pivotNode.getNorthNode()
            south = pivotNode.getSouthNode()
            northeast = pivotNode.getNorthEastNode()
            northwest = pivotNode.getNorthWestNode()
            southeast = pivotNode.getSouthEastNode()
            southwest = pivotNode.getSouthWestNode()
            

            if(north != None and not north.getPlacedStatus()):
                newLabel = self.__createLabel(north)
                newLabel.move(pivX, pivY-200)
                north.setPlacedStatus(True)
                north.setPositionVector((pivX + posVecXOffset, pivY-200 + posVecYOffset))
            if(south != None and not south.getPlacedStatus()):
                newLabel = self.__createLabel(south)
                newLabel.move(pivX, pivY+200)
                south.setPlacedStatus(True)
                south.setPositionVector((pivX + posVecXOffset, pivY+200 + posVecYOffset))
            if(northeast != None and not northeast.getPlacedStatus()):
                newLabel = self.__createLabel(northeast)
                newLabel.move(pivX+200, pivY-100)
                northeast.setPositionVector((pivX+200 + posVecXOffset, pivY-100 + posVecYOffset))
                northeast.setPlacedStatus(True)
            if(northwest != None and not northwest.getPlacedStatus()):
                newLabel = self.__createLabel(northwest)
                newLabel.move(pivX-200, pivY-100)
                northwest.setPlacedStatus(True)
                northwest.setPositionVector((pivX-200 + posVecXOffset, pivY-100 + posVecYOffset))
            if(southeast != None and not southeast.getPlacedStatus()):
                newLabel = self.__createLabel(southeast)
                newLabel.move(pivX+200, pivY+100)
                southeast.setPlacedStatus(True)
                southeast.setPositionVector((pivX+200+ posVecXOffset, pivY+100+posVecYOffset))
            if(southwest != None and not southwest.getPlacedStatus()):
                newLabel = self.__createLabel(southwest)
                newLabel.move(pivX-200, pivY+100)
                southwest.setPlacedStatus(True)
                southwest.setPositionVector((pivX-200+posVecXOffset, pivY+100+posVecYOffset))


            if(curTileNum == numTilesInRing):
                if(curRingNumber == 0):
                    pivotNode = pivotNode.getNorthNode()
                    pivY = pivY - 200
                elif(curRingNumber != self.hextile_map_obj.getMapSize().value):
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

            


    def __createLabel(self, tile:HextileNode) -> HexLabel:
        label = HexLabel(tile, self.toolbox, self.map_widget,)
        pngStr = ''
        pngStr = self.tile_types_ref_obj.getDefaultTileAssetByName(tile.getTileType())
        pixmap = QPixmap(pngStr)
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)
        label.setScaledContents(True)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return label



if __name__ == "__main__":
    app = QApplication([])

    #Toolbox holds all the tools necessary for the application to function
    toolbox = Toolbox()

    #The window is a custom class derived from QWindow that is passed the toolbox
    window = ToolboxHomePage(toolbox)
    window.show()

    app.exec()