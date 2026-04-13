from PyQt6.QtCore import Qt, QMimeData, QLineF, QPoint
from PyQt6.QtGui import QPainter, QPen, QPixmap, QColor, QIcon, QDrag
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QDockWidget,
    QPushButton,
    QGridLayout,  
    QToolBar,
    QComboBox,
    QLineEdit,
    QInputDialog,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QMessageBox
)

from toolbox.ConnectionLogic import Session
from toolbox.Toolbox import Toolbox
from toolbox.Database import DatabaseMessages

from functools import partial


class SessionWidget(QMainWindow):
    def __init__(self, toolbox:Toolbox):
        super().__init__()
        self.toolbox = toolbox
        self.map_ref = self.toolbox.get_hextile_map_ref()
        self.account_ref = self.toolbox.get_account_ref()
        self.session_ref = self.toolbox.get_session_ref()


        self.username_input = ""
        self.password_input = ""
        self.email_input = ""

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.main_widget.setLayout(self.main_layout)

        if(self.account_ref.get_logged_in()):
            self.__layout_with_acc()
        else:
            self.__layout_without_acc()


        self.setCentralWidget(self.main_widget)

    def __layout_with_acc(self):
        self.user_label = QLabel("User " + self.account_ref.get_username())
        self.start_session_btn = QPushButton("Start Session")
        self.start_session_btn.clicked.connect(self.__start_session)
        self.main_layout.addWidget(self.user_label)
        self.main_layout.addWidget(self.start_session_btn)

    def __layout_without_acc(self):
        self.change_form_btn = QPushButton("Don't have an account? Sign up here!")
        self.change_form_btn.clicked.connect(partial(self.__change_form, "signup"))
        self.change_form_btn.setFlat(True)
        
        self.main_layout.addWidget(self.change_form_btn)

        self.email_prompt = QLineEdit("enter your email")
        self.email_prompt.textEdited.connect(self.__email_input_edited)
        self.email_prompt.hide()

        self.username_prompt = QLineEdit("enter your username")
        self.username_prompt.textEdited.connect(self.__username_input_edited)
        self.password_prompt = QLineEdit("enter your password")
        self.password_prompt.textEdited.connect(self.__password_input_edited)
        self.log_in_btn = QPushButton("Log In")
        self.log_in_btn.clicked.connect(self.__try_log_in)

        self.sign_up_btn = QPushButton("Sign Up")
        self.sign_up_btn.clicked.connect(self.__try_sign_up)
        self.sign_up_btn.hide()

        self.main_layout.addWidget(self.email_prompt)
        self.main_layout.addWidget(self.username_prompt)
        self.main_layout.addWidget(self.password_prompt)
        self.main_layout.addWidget(self.log_in_btn)
        self.main_layout.addWidget(self.sign_up_btn)

    def __change_form(self, new_type):
        if(new_type == "signup"):
            self.change_form_btn.setText("Already have an account? Log in here!")
            self.log_in_btn.hide()
            self.email_prompt.show()
            self.sign_up_btn.show()
            self.change_form_btn.clicked.disconnect()
            self.change_form_btn.clicked.connect(partial(self.__change_form, "login"))

        else:
            self.change_form_btn.setText("Don't have an account? Sign up here!")
            self.sign_up_btn.hide()
            self.email_prompt.hide()
            self.log_in_btn.show()
            self.change_form_btn.clicked.disconnect()
            self.change_form_btn.clicked.connect(partial(self.__change_form, "signup"))

    def __username_input_edited(self, text):
        self.username_input = text

    def __password_input_edited(self, text):
        self.password_input = text

    def __email_input_edited(self, text):
        self.email_input = text

    def __clear_input(self):
        self.username_input = ""
        self.password_input = ""
        self.email_input = ""
        self.username_prompt.setText("enter your username")
        self.password_prompt.setText("enter your password")
        self.email_prompt.setText("enter your email")

    def __try_log_in(self):
        msg = self.account_ref.try_log_in(username=self.username_input, password=self.password_input)
        self.__clear_input()
        if(msg == DatabaseMessages.SUCCESS):
            for i in reversed(range(self.main_layout.count()-1)): 
                self.main_layout.itemAt(i).widget().setParent(None)            
            self.__layout_with_acc()


    def __try_sign_up(self):
        msg = self.account_ref.try_sign_up(email=self.email_input, username=self.username_input, password=self.password_input)
        self.__clear_input()
        if(msg == DatabaseMessages.SUCCESS):
            print("success")
            self.__change_form("login")


    def __start_session(self):
        self.session_ref.start_session_as_host()
        #here we r gonna need to ask the map to create an object that is sendable
        self.map_ref.saveMap()
        

    
    