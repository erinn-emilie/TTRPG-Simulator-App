import random

from toolbox import Toolbox
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class LogWidget(QWidget):
    def __init__(self, toolbox:Toolbox):
        super().__init__()

        self.toolbox = toolbox
        self.logger_ref = self.toolbox.get_logger_ref()
        
        self.setWindowTitle("Session Log")


        self.log_contents_widget = QWidget()
        self.log_contents_layout = QVBoxLayout()
        self.log_contents_widget.setLayout(self.log_contents_layout)

        self.__populate_log_layout()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.log_contents_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def __populate_log_layout(self):
        log_contents = self.logger_ref.get_all_log_contents()
        for line in reversed(log_contents):
            label = QLabel(line)
            self.log_contents_layout.addWidget(label)

