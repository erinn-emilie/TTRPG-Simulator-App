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