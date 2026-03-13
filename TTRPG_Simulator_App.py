from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QAction, QPixmap, QMouseEvent, QPainter, QPen, QBrush, QGuiApplication
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
from toolbox.Toolbox import Toolbox
from toolbox.TileTypes import TileTypes
from toolbox.HextileMap import HextileMap
from HextileNode import HextileNode
from Enums.MapSizes import MapSizes
from toolbox.Settings import Settings
from widgets.SettingsMenu import SettingsMenu
from pages.HomeWindow import HomeWindow


        




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

        


'''class CustomTilesWindow(QMainWindow):
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
            self.mainLayout.addWidget(widget)
            self.tileTypesRef.add_new_tile("New Tile", asset_path)'''






if __name__ == "__main__":
    app = QApplication([])

    primary_screen = QGuiApplication.primaryScreen() #
    screen_geometry = primary_screen.geometry() #
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()


    #Toolbox holds all the tools necessary for the application to function
    toolbox = Toolbox(screen_width, screen_height)

    #The window is a custom class derived from QWindow that is passed the toolbox
    window = HomeWindow(toolbox)
    window.show()

    app.exec()