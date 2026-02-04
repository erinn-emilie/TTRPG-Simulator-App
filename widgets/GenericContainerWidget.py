from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    )

from Toolbox import Toolbox


class GenericContainerWidget(QWidget):
    def __init__(self, tile_name:str, toolbox:Toolbox, tile_image_path:str):
        super().__init__()
        self.toolbox = toolbox
        self.tile_types_ref = self.toolbox.get_tile_types_ref()
        self.main_layout = QVBoxLayout()
        # make special label with stylesheet thats automatically disabled
        '''self.setStyleSheet("""
            background-color: pink;
        """)'''

        self.tile_name_prompt_label = QLabel("Tile Name:")

        self.old_tile_name = tile_name
        self.new_tile_name = ""
        self.tile_name_label = QLineEdit(self.old_tile_name)
        self.tile_name_label.setEnabled(False)
        self.tile_name_label.textEdited.connect(self.__tile_name_edited)
        self.tile_name_label.setMaximumWidth(200)
        self.tile_name_prompt_label.setMaximumWidth(200)


        self.tile_image_pixmap = QPixmap(tile_image_path)
        self.tile_image_label = QLabel()
        self.tile_image_label.setPixmap(self.tile_image_pixmap)
        self.tile_image_label.setScaledContents(True)
        self.tile_image_label.setMaximumWidth(300)
        self.tile_image_label.setMaximumHeight(300)
        self.tile_name_row = QHBoxLayout()
        self.tile_name_row.addWidget(self.tile_name_prompt_label)
        self.tile_name_row.addWidget(self.tile_name_label)
        self.tile_name_row.addWidget(self.tile_image_label)
        self.main_layout.addLayout(self.tile_name_row)
        self.setLayout(self.main_layout)

    def enable_tile_name_label(self):
        self.tile_name_label.setEnabled(True)

    def disable_tile_name_label(self):
        self.tile_name_label.setEnabled(False)

    def __tile_name_edited(self,text):
        self.new_tile_name = text

    def cancel_tile_name_edit(self):
        self.new_tile_name = ""

    def save_new_tile_name(self):
        if(self.new_tile_name != ""):
            self.tile_types_ref.change_tile_name(self.old_tile_name, self.new_tile_name)
            self.old_tile_name = self.new_tile_name
            self.new_tile_name = ""
