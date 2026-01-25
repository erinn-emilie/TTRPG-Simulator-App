from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QLineEdit,
    QPushButton
    )

from Toolbox import Toolbox
from HextileNode import HextileNode
from SettingsMenu import SettingsMenu
from pages.CustomTokenExploreWindow import CustomTokenExploreWindow
from Enums.TokenTypes import TokenTypes


class GridWindow(QMainWindow):
    def __init__(self, hexNode:HextileNode):
        super().__init__()
        self.hexNode = hexNode

        self.title = "Grid Window"
        self.setWindowTitle(self.title)

        self.main_widget = QWidget()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.main_widget)
        self.setCentralWidget(self.main_widget)

class HexLabel(QLabel):
    def __init__(self, hexNode:HextileNode, toolbox:Toolbox, parent=None):
        super().__init__(parent=parent)
        self.hexNode = hexNode
        self.gridWindow = GridWindow(self.hexNode)

    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            self.gridWindow.show()


#Class derived from QMainWindow, this is the homepage of the whole app,
#where the map is generated and displayed.  
class HomeWindow(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox):
        super().__init__()            
        window_title = "Tabletop Roleplaying Game Simulator"
        self.setWindowTitle(window_title)

        
        self.main_widget = QWidget()
        self.map_layout = QVBoxLayout()
        self.map_widget = QWidget()

        self.box_select_flag = False
        self.ring_select_flag= False
        self.line_select_flag = False

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

        self.box_select_btn = QPushButton("Box Select Tiles", self)
        self.box_select_btn.clicked.connect(self.__toggle_box_select)
        self.map_settings_toolbar.addWidget(self.box_select_btn)

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

        self.customTilesButton.clicked.connect(self.__show_custom_tiles_window)
        self.customPlayerButton.clicked.connect(self.__show_custom_players_window)

        self.navbar.setWidget(self.navbarContainer)

        self.main_widget.setStyleSheet("background-color: pink")
        self.setCentralWidget(self.scroll)


    def __toggle_box_select(self):
        if(self.box_select_flag):
            self.box_select_flag = False
        else:
            self.box_select_flag = True


    #def __start_box_select(self):

        


    def __show_custom_tiles_window(self):
        if(self.customTilesWindow is None):
            self.customTilesWindow = CustomTokenExploreWindow(self.toolbox, TokenTypes.TILES)
        self.customTilesWindow.show()

    def __show_custom_players_window(self):
        if(self.customTilesWindow is None):
            self.customTilesWindow = CustomTokenExploreWindow(self.toolbox, TokenTypes.PLAYER_CHARACTERS)
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
