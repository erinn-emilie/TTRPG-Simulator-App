import random

from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Log(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Log")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.rejected.connect(self.reject)

        label = QLabel("Log contents:")
        log = open("log..")
        contents = QLabel(log.read())
        log.close()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(contents)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.buttonBox)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

class start(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.button = QPushButton("Open log")
        self.button.clicked.connect(self.clicked)
        
        self.setWindowTitle("Start Page")
        self.setCentralWidget(self.button)
        
    def clicked(self):
        Log().exec()

app = QApplication([])

window = start()
window.show()

app.exec()
