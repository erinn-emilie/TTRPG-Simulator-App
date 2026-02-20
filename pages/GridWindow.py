from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget
)

import math

from HextileNode import HextileNode
from toolbox.Toolbox import Toolbox


class GridWindow(QMainWindow):
    def __init__(self, hexNode:HextileNode, toolbox:Toolbox):
        super().__init__()
        self.hexNode = hexNode
        self.toolbox = toolbox
        self.settings_ref = self.toolbox.get_settings_ref()

        self.title = "Grid Window"
        self.setWindowTitle(self.title)

        self.main_widget = QWidget()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.main_widget)
        self.setCentralWidget(self.main_widget)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)

        width = self.width()
        height = self.height()

        tile_size = self.settings_ref.getTileSize()


        for x in range(0, width, math.ceil(tile_size)):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, math.ceil(tile_size)):
            painter.drawLine(0, y, width, y)
