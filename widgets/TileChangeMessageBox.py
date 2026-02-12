from PyQt6.QtCore import Qt, QPoint, QEvent, QElapsedTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QDockWidget,
    QLabel,
    QMainWindow,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox
    )

from toolbox.Toolbox import Toolbox
from HextileNode import HextileNode
from SettingsMenu import QComboBox, SettingsMenu
from Enums.TokenTypes import TokenTypes
class TileChangeMessageBox(QMessageBox):
    def __init__(self, toolbox:Toolbox, parent=None):
        super().__init__(parent=parent)
        self.toolbox = toolbox
        self.tile_types = self.toolbox.get_tile_types_ref()
        self.settings_ref = self.toolbox.get_settings_ref()
        self.hex_node = self.parent().get_hex_node()
        self.cur_tile_type = self.hex_node.getTileType()
        self.new_tile_type = None

        self.setText("Choose a new tile type!")
        self.setStandardButtons(
            QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel
        )
        
        


        tileNamesList = self.tile_types.get_tile_names_list()
        self.checkboxes = []
        for name in tileNamesList:
            name = name.upper()
            new_checkbox = QCheckBox(text=str(name), parent=self)
            if(name == self.cur_tile_type):
                new_checkbox.setChecked(True)
            else:
                new_checkbox.setChecked(False)
            new_checkbox.setStyleSheet("""
                QCheckBox::indicator:unchecked {
                    background-color: red;
                }
                QCheckBox::indicator:checked {
                    background-color: green;
                }
            """)   
            self.checkboxes.append(new_checkbox)
            new_checkbox.toggled.connect(self.__on_checkbox_change)
            
            self.layout().addWidget(new_checkbox)


    def __on_checkbox_change(self, state):
        cur_checkbox = self.sender()
        name = cur_checkbox.text()
        if(state):
            for checkbox in self.checkboxes:
                if(checkbox != cur_checkbox):
                    checkbox.setChecked(False)
            self.hex_node.setTileType(name.upper())