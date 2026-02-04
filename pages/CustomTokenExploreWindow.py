from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QPushButton,
    QScrollArea
)

from PyQt6.QtCore import Qt


from Toolbox import Toolbox
from Enums.TokenTypes import TokenTypes
from widgets.GenericContainerWidget import GenericContainerWidget

import os


class CustomTokenExploreWindow(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox, token_set_type:TokenTypes):
        super().__init__()

        self.title = "Custom Menu"
        self.setWindowTitle(self.title)
        self.toolbox = toolbox_ref
        self.tile_types_ref = self.toolbox.get_tile_types_ref()

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()


        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.__edit_tiles)
        self.main_layout.addWidget(self.edit_btn)

        self.save_btn = QPushButton("Save Changes")
        self.main_layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.__save_changes)
        self.save_btn.hide()

        self.tile_list = self.tile_types_ref.get_tile_names_list()
        self.tile_widgets = []
        for tile in self.tile_list:
            image_path = self.tile_types_ref.get_default_tile_asset_by_name(tile.upper())
            widget = GenericContainerWidget(tile, self.toolbox, image_path)
            self.tile_widgets.append(widget)
            self.main_layout.addWidget(widget)
        self.add_tile_btn = QPushButton("Add New Tile")
        self.add_tile_btn.clicked.connect(self.__add_new_tile)
        self.main_layout.addWidget(self.add_tile_btn)
        self.main_widget.setLayout(self.main_layout)
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

                img_name = img_name.replace(".jpg", ".png")
                img_name = img_name.replace(".jpeg", ".png")
                cur_dir = os.getcwd()
                asset_dir = os.path.join(cur_dir, "assets")
                asset_path = os.path.join(asset_dir, img_name)
                os.rename(img_path, asset_path)
            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")

            widget = GenericContainerWidget("New Tile", self.tile_list, asset_path)
            self.main_layout.addWidget(widget)
            self.tile_types_ref.add_new_tile("New Tile", asset_path)

    def __edit_tiles(self):
        self.save_btn.show()
        self.edit_btn.hide()
        for widget in self.tile_widgets:
            widget.enable_tile_name_label()

    def __save_changes(self):
        for widget in self.tile_widgets:
            widget.save_new_tile_name()

