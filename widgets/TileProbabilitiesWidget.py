from PyQt6.QtCore import Qt, QPoint, QEvent, QElapsedTimer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
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
    QInputDialog
    )

class TileProbabilitiesWidget(QWidget):
    def __init__(self, toolbox, ):
        super().__init__()