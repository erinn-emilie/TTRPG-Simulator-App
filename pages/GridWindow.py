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
    QCheckBox,
    QGraphicsScene
    )

from toolbox.Toolbox import Toolbox
from HextileNode import HextileNode
from SettingsMenu import QComboBox, SettingsMenu
from pages.CustomTokenExploreWindow import CustomTileExploreWindow
from pages.CustomTokenExploreWindow import CustomTokenExploreWindow
from Enums.TokenTypes import TokenTypes
from widgets.TileChangeMessageBox import TileChangeMessageBox

import math

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
