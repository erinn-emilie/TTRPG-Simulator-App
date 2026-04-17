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
        self.log_contents_layout.setSpacing(0)
        self.log_contents_widget.setLayout(self.log_contents_layout)

        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.__clear_log)

        self.add_btn = QPushButton("Add Line")
        self.add_btn.clicked.connect(self.__add_line)
        self.added_line = ""
        self.line_input = QLineEdit("")
        self.line_input.textEdited.connect(self.__type_line)

        self.__populate_log_layout()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.log_contents_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.clear_btn)
        row = QHBoxLayout()
        row.addWidget(self.line_input)
        row.addWidget(self.add_btn)
        layout.addLayout(row)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def __populate_log_layout(self):
        log_contents = self.logger_ref.get_all_log_contents()
        for line in reversed(log_contents):
            label = QLabel(line)
            self.log_contents_layout.addWidget(label)

    def __clear_log(self):    
        self.logger_ref.clear_contents()
        for i in reversed(range(self.log_contents_layout.count())): 
            self.log_contents_layout.itemAt(i).widget().setParent(None)


    def __type_line(self, text):
        self.added_line = text

    def __add_line(self):
        username = self.toolbox.get_account_ref().get_username()
        if(username == ""):
            username = "Player"
        self.added_line = f"{username}: {self.added_line}"
        self.logger_ref.add_line(self.added_line)
        for i in reversed(range(self.log_contents_layout.count())): 
            self.log_contents_layout.itemAt(i).widget().setParent(None)
        self.line_input.setText("")
        self.__populate_log_layout()
