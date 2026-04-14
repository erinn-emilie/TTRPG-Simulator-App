from PyQt6.QtCore import Qt, QPoint, QEvent, QElapsedTimer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QSizePolicy
    )

from toolbox.Toolbox import Toolbox
from HextileNode import HextileNode
from widgets.SettingsMenu import SettingsMenu
from pages.CustomTokenExploreWindow import CustomTileExploreWindow
from pages.CustomTokenExploreWindow import CustomTokenExploreWindow
from pages.GridWindow import GridWindow
from Enums.TokenTypes import TokenTypes
from widgets.TileChangeMessageBox import TileChangeMessageBox
from widgets.LogWidget import LogWidget
from widgets.DiceRoller import DiceRoller
from widgets.SessionWidget import SessionWidget
from Enums.MapSizes import MapSizes





class HexLabel(QLabel):
    def __init__(self, hex_node:HextileNode, toolbox:Toolbox, home_window, parent=None):
        super().__init__(parent=parent)
        self.message = None
        self.hex_node = hex_node
        self.toolbox = toolbox
        self.tile_types_ref = self.toolbox.get_tile_types_ref()
        self.gridWindow = GridWindow(self.hex_node, self.toolbox)
        self.home_window = home_window

    def get_hex_node(self) -> HextileNode:
        return self.hex_node

    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.RightButton):
            self.message = TileChangeMessageBox(self.toolbox, parent=self)
            self.tile_type = self.hex_node.getTileType()
            self.ret_value = self.message.exec()
            if(self.ret_value == QMessageBox.StandardButton.Cancel):
                self.hex_node.setTileType(self.tile_type)
            else:
                new_tile_type = self.hex_node.getTileType()
                png_str = self.tile_types_ref.get_default_tile_asset_by_name(new_tile_type)
                pixmap = QPixmap(png_str)
                self.setPixmap(pixmap)
        if(event.button() == Qt.MouseButton.LeftButton):
            self.gridWindow.show()
            
        return super().mousePressEvent(event)



class HomeWindow(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox):
        super().__init__()            
        window_title = "Tabletop Roleplaying Game Simulator"
        self.setWindowTitle(window_title)

        
        self.main_widget = QWidget()
        self.map_layout = QVBoxLayout()
        self.map_widget = QWidget()


        self.toolbox = toolbox_ref
        self.user_id = None

        self.hextile_map_obj = self.toolbox.get_hextile_map_ref()
        self.tile_types_ref_obj = self.toolbox.get_tile_types_ref()
        self.settings_ref_obj = self.toolbox.get_settings_ref()


        self.tile_labels_list = []
        self.__layout_tiles()

        self.map_settings_btn_stylesheet = """
            color: #F0F2A6;
            font-size: 10pt;
        """

        self.map_layout.addWidget(self.map_widget)
        self.main_widget.setLayout(self.map_layout)

        self.map_widget.setMinimumSize(3000,3000)

        self.map_widget_stylesheet = """
            background-color: #F0F2A6;
        """

        self.map_widget.setStyleSheet(self.map_widget_stylesheet)

        self.map_settings_toolbar = QToolBar()

        self.map_settings_toolbar.setStyleSheet("background-color: #aa6373")
        self.map_settings_toolbar.setMinimumHeight(100)

        self.xtra_settings_btn = QPushButton("Configure Extra Settings", self)
        self.xtra_settings_btn.clicked.connect(self.__open_xtra_settings)
        self.xtra_settings_btn.setFlat(True)
        self.xtra_settings_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.xtra_settings_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.map_settings_toolbar.addWidget(spacer)

        self.seed_input_field = QLineEdit("Enter in a map seed here!")
        self.seed_input_field.textEdited.connect(self.__recieve_seed_input)
        self.seed_input_field.setStyleSheet("""background-color: white;""")
        self.seed_input_field.setMaximumWidth(300)
        self.map_settings_toolbar.addWidget(self.seed_input_field)

        self.generate_map_btn = QPushButton("Generate Map", self)
        self.generate_map_btn.clicked.connect(self.__generate_map)
        self.generate_map_btn.setFlat(True)
        self.generate_map_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.generate_map_btn)

        self.save_map_btn = QPushButton("Save Map", self)
        self.save_map_btn.clicked.connect(self.__save_map)
        self.save_map_btn.setFlat(True)
        self.save_map_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.save_map_btn)

        self.load_map_btn = QPushButton("Load Map", self)
        self.load_map_btn.setFlat(True)
        self.load_map_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.load_map_btn)
        self.load_map_btn.clicked.connect(self.__load_saved_map)

        self.log_widget_btn = QPushButton("Log Widget", self)
        self.log_widget_btn.setFlat(True)
        self.log_widget_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.log_widget_btn)
        self.log_widget_btn.clicked.connect(self.__open_log_widget)

        self.session_mng_btn = QPushButton("Session Manager", self)
        self.session_mng_btn.setFlat(True)
        self.session_mng_btn.setStyleSheet(self.map_settings_btn_stylesheet)
        self.map_settings_toolbar.addWidget(self.session_mng_btn)
        self.session_mng_btn.clicked.connect(self.__open_session_mngr)




        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.map_settings_toolbar)


        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.main_widget)

        self.navbar = QDockWidget("Custom Tokens", self)
        #self.navbar.setStyleSheet("""background-color: white;""")
        self.navbar.setDockLocation(Qt.DockWidgetArea.RightDockWidgetArea)
        self.navbar.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.navbar.setMinimumHeight(500)
        

        self.navbarContainer = QWidget()

        self.navbarLayout = QVBoxLayout(self.navbarContainer)



        self.customTilesWindow = None
        self.customPlayersWindow = None
        self.customNonPlayersWindow = None
        self.customAnimalsWindow = None
        self.customMonstersWindow = None
        self.customBuildingsWindow = None
        self.customStructuresWindow = None
        self.customNatureWindow = None
        self.diceRollerWindow = None
        self.login_window = None
        self.session_mngr_window = None

        self.customTilesButton = QPushButton("Tiles", self.navbar)
        self.customTilesButton.setIcon(QIcon("assets/tiles.png"))
        self.customTilesButton.setFlat(True)

        self.customPlayerButton = QPushButton("Player Characters", self.navbar)
        self.customPlayerButton.setIcon(QIcon("assets/character.png"))
        self.customPlayerButton.setFlat(True)

        self.customNonPlayerButton = QPushButton("Non-Player Characters", self.navbar)
        self.customNonPlayerButton.setIcon(QIcon("assets/character.png"))
        self.customNonPlayerButton.setFlat(True)
        
        self.customAnimalButton = QPushButton("Animals", self.navbar)
        self.customAnimalButton.setIcon(QIcon("assets/animal.png"))
        self.customAnimalButton.setFlat(True)

        self.customMonsterButton = QPushButton("Monsters", self.navbar)
        self.customMonsterButton.setIcon(QIcon("assets/monsters.png"))
        self.customMonsterButton.setFlat(True)

        self.customBuildingsButton = QPushButton("Buildings", self.navbar)
        self.customBuildingsButton.setIcon(QIcon("assets/buildings.png"))
        self.customBuildingsButton.setFlat(True)

        self.customStructuresButton = QPushButton("Structures", self.navbar)
        self.customStructuresButton.setIcon(QIcon("assets/buildings.png"))
        self.customStructuresButton.setFlat(True)
        
        self.customNatureButton = QPushButton("Nature", self.navbar)
        self.customNatureButton.setIcon(QIcon("assets/nature.png"))
        self.customNatureButton.setFlat(True)

        self.diceRollerButton = QPushButton("Dice Roller", self.navbar)
        self.diceRollerButton.setIcon(QIcon("assets/d20.png"))
        self.diceRollerButton.setFlat(True)

        self.customBtnStyleSheet = """
              background-color: white;
              color: black;
              border-style: solid;
              border-color: black;
              border-width: 2px;
              border-radius: 10px;
              padding: 5px;
              text-align: center;
              font-size: 16px;
              """

        self.navbarContainerStyleSheet = """
            background-color: white;
        """


        self.navbarLayout.addWidget(self.customTilesButton)
        self.navbarLayout.addWidget(self.customPlayerButton)
        self.navbarLayout.addWidget(self.customNonPlayerButton)
        self.navbarLayout.addWidget(self.customAnimalButton)
        self.navbarLayout.addWidget(self.customMonsterButton)
        self.navbarLayout.addWidget(self.customBuildingsButton)
        self.navbarLayout.addWidget(self.customStructuresButton)
        self.navbarLayout.addWidget(self.customNatureButton)
        self.navbarLayout.addWidget(self.diceRollerButton)


        self.customTilesButton.clicked.connect(self.__show_custom_tiles_window)
        self.customPlayerButton.clicked.connect(self.__show_custom_players_window)
        self.customNonPlayerButton.clicked.connect(self.__show_custom_nonplayers_window)
        self.customAnimalButton.clicked.connect(self.__show_custom_animals_window)
        self.customMonsterButton.clicked.connect(self.__show_custom_monsters_window)
        self.customBuildingsButton.clicked.connect(self.__show_custom_buildings_window)
        self.customStructuresButton.clicked.connect(self.__show_custom_structures_window)
        self.customNatureButton.clicked.connect(self.__show_custom_nature_window)
        self.diceRollerButton.clicked.connect(self.__show_dice_roller_window)

        
        self.navbarContainer.setStyleSheet(self.navbarContainerStyleSheet)
        self.navbar.setWidget(self.navbarContainer)

        self.setCentralWidget(self.scroll)
           

        

    def __open_login_window(self):
        if self.login_window is None:
            self.login_window = Window(self)
            self.login_window.show()

    def __show_custom_tiles_window(self):
        if(self.customTilesWindow is None):
            self.customTilesWindow = CustomTileExploreWindow(self.toolbox, self)
        self.customTilesWindow.show()

    def __show_custom_players_window(self):
        if(self.customPlayersWindow is None):
            self.customPlayersWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.PLAYER_CHARACTERS)
        self.customPlayersWindow.show()

    def __show_custom_nonplayers_window(self):
        if(self.customNonPlayersWindow is None):
            self.customNonPlayersWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.NON_PLAYER_CHARACTERS)
        self.customNonPlayersWindow.show()

    def __show_custom_animals_window(self):
        if(self.customAnimalsWindow is None):
            self.customAnimalsWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.ANIMALS)
        self.customAnimalsWindow.show()

    def __show_custom_monsters_window(self):
        if(self.customMonstersWindow is None):
            self.customMonstersWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.MONSTERS)
        self.customMonstersWindow.show()

    def __show_custom_buildings_window(self):
        if(self.customBuildingsWindow is None):
            self.customBuildingsWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.BUILDINGS)
        self.customBuildingsWindow.show()

    def __show_custom_structures_window(self):
        if(self.customStructuresWindow is None):
            self.customStructuresWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.STRUCTURES)
        self.customStructuresWindow.show()

    def __show_custom_nature_window(self):
        if(self.customNatureWindow is None):
            self.customNatureWindow = CustomTokenExploreWindow(self.toolbox, self, TokenTypes.NATURE)
        self.customNatureWindow.show()

    def __show_dice_roller_window(self):
        if(self.diceRollerWindow is None):
            self.diceRollerWindow = DiceRoller(self.toolbox)
        self.diceRollerWindow.show()

    def close_custom_tiles_window(self):
        self.customTilesWindow.hide()

    def close_custom_players_window(self):
        self.customPlayersWindow = None

    def close_custom_nonplayers_window(self):
        self.customNonPlayersWindow = None

    def close_custom_animals_window(self):
        self.customAnimalsWindow = None

    def close_custom_monsters_window(self):
        self.customMonstersWindow = None

    def close_custom_buildings_window(self):
        self.customBuildingsWindow = None

    def close_custom_structures_window(self):
        self.customStructuresWindow = None

    def close_custom_nature_window(self):
        self.customNatureWindow = None


    def __open_log_widget(self):
        self.log_widget = LogWidget(self.toolbox)
        self.log_widget.show()

    def __open_session_mngr(self):
        self.session_mngr_window = SessionWidget(self.toolbox)
        self.session_mngr_window.show()






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
        map_size = self.settings_ref_obj.getMapSize()
        min_size = 0
        match(map_size):
            case MapSizes.XSMALL:
                min_size = 1000
            case MapSizes.SMALL:
                min_size = 2000
            case MapSizes.MEDIUM:
                min_size = 3000
            case MapSizes.LARGE:
                min_size = 4000
            case MapSizes.XLARGE:
                min_size = 5000
            case _:
                min_size = 3000
        
        self.map_widget.setMinimumSize(min_size, min_size)
        self.hextile_map_obj.generateMap()
        self.__layout_tiles()
        self.map_layout.addWidget(self.map_widget)

    def __load_saved_map(self):
        map_name, ok = QInputDialog.getText(self, "Map Name", "Please enter a name to save the map under!")
        if ok and map_name:
            self.map_layout.removeWidget(self.map_widget)
            self.map_widget = QWidget()
            self.map_widget.setMinimumSize(3000,3000)
            self.hextile_map_obj.loadSavedMap(map_name)
            self.__layout_tiles()
            self.map_layout.addWidget(self.map_widget)


    def __layout_tiles(self):
        centerNode = self.hextile_map_obj.getCenterNode()
        pivotNode = centerNode
        curRingNumber = 0
        numTilesInRing = 1
        curTileNum = 0
        self.tile_labels_list = []

        pivX = 840    
        pivY = 840


        newLabel = self.__create_label(pivotNode)
        newLabel.move(pivX, pivY)
        self.tile_labels_list.append(newLabel)
        pivotNode.setPlacedStatus(True)
        posVecXOffset = 0
        posVecYOffset = 70
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
                newLabel = self.__create_label(north)
                newLabel.move(pivX, pivY-140)
                self.tile_labels_list.append(newLabel)
                north.setPlacedStatus(True)
                north.setPositionVector((pivX + posVecXOffset, pivY-140 + posVecYOffset))
            if(south != None and not south.getPlacedStatus()):
                newLabel = self.__create_label(south)
                newLabel.move(pivX, pivY+140)
                self.tile_labels_list.append(newLabel)
                south.setPlacedStatus(True)
                south.setPositionVector((pivX + posVecXOffset, pivY+140 + posVecYOffset))
            if(northeast != None and not northeast.getPlacedStatus()):
                newLabel = self.__create_label(northeast)
                newLabel.move(pivX+122, pivY-70)
                self.tile_labels_list.append(newLabel)
                northeast.setPositionVector((pivX+140 + posVecXOffset, pivY-70 + posVecYOffset))
                northeast.setPlacedStatus(True)
            if(northwest != None and not northwest.getPlacedStatus()):
                newLabel = self.__create_label(northwest)
                newLabel.move(pivX-122, pivY-70)
                self.tile_labels_list.append(newLabel)
                northwest.setPlacedStatus(True)
                northwest.setPositionVector((pivX-140 + posVecXOffset, pivY-70 + posVecYOffset))
            if(southeast != None and not southeast.getPlacedStatus()):
                newLabel = self.__create_label(southeast)
                newLabel.move(pivX+122, pivY+70)
                self.tile_labels_list.append(newLabel)
                southeast.setPlacedStatus(True)
                southeast.setPositionVector((pivX+140+ posVecXOffset, pivY+70+posVecYOffset))
            if(southwest != None and not southwest.getPlacedStatus()):
                newLabel = self.__create_label(southwest)
                newLabel.move(pivX-122, pivY+70)
                self.tile_labels_list.append(newLabel)
                southwest.setPlacedStatus(True)
                southwest.setPositionVector((pivX-140+posVecXOffset, pivY+70+posVecYOffset))


            if(curTileNum == numTilesInRing):
                if(curRingNumber == 0):
                    pivotNode = pivotNode.getNorthNode()
                    pivY = pivY - 140
                elif(curRingNumber != self.hextile_map_obj.getMapSize().value):
                    pivotNode = pivotNode.getNorthEastNode().getNorthNode()
                    pivX = pivX + 122
                    pivY = pivY - 210
                curRingNumber += 1
                numTilesInRing = curRingNumber * 6
                curTileNum = 0
            else:
                nextNode = pivotNode.getSouthEastNode()
                posX = pivX + 122
                posY = pivY + 70
                
                if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                    nextNode = pivotNode.getSouthNode()
                    posX = pivX
                    posY = pivY + 140
                    if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                        nextNode = pivotNode.getSouthWestNode()
                        posX = pivX - 122
                        posY = pivY + 70
                        if(nextNode == None or nextNode.getPositionIdx() != curRingNumber or curTileNum > numTilesInRing/2):
                            nextNode = pivotNode.getNorthWestNode()
                            posX = pivX - 122
                            posY = pivY - 70
                            if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                                nextNode = pivotNode.getNorthNode()
                                posX = pivX
                                posY = pivY - 140
                                if(nextNode == None or nextNode.getPositionIdx() != curRingNumber):
                                    nextNode = pivotNode.getNorthEastNode()
                                    posX = pivX + 122
                                    posY = pivY - 70
                pivX = posX
                pivY = posY
                pivotNode = nextNode

            


    def __create_label(self, tile:HextileNode) -> HexLabel:
        label = HexLabel(tile, self.toolbox, self, parent=self.map_widget,)
        pngStr = ''
        pngStr = self.tile_types_ref_obj.get_default_tile_asset_by_name(tile.getTileType())
        pixmap = QPixmap(pngStr)
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)
        label.setScaledContents(True)
        label.setFixedSize(157,157)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        label.installEventFilter(self)        
        return label


    def __save_map(self):
        acc_ref = self.toolbox.get_account_ref()
        if(not acc_ref.get_logged_in()):
            map_name, ok = QInputDialog.getText(self, "Map Name", "You are not logged in, your map will be saved locally!\nPlease enter a name to save the map under!")
            if ok and map_name:
                self.hextile_map_obj.saveMap(map_name=map_name)
        else:
            map_name, ok = QInputDialog.getText(self, "Map Name", "Your map will be saved to your account!\nPlease enter a name to save the map under!")
            if ok and map_name:
                self.hextile_map_obj.saveMap(map_name=map_name, local=False)
