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
    QMessageBox,
    QDialog,
    QDialogButtonBox
)

from toolbox.ConnectionLogic import ClientSession
from toolbox.ConnectionLogic import ServerSession
from toolbox.Toolbox import Toolbox
from toolbox.Database import DatabaseMessages

from functools import partial

class FindSessionDialog(QDialog):
    def __init__(self, session_widget):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.session_widget = session_widget

        self.username_prompt = QLineEdit("username of user hosting session")
        self.username_prompt.textEdited.connect(self.__username_input_edited)
        self.password_prompt = QLineEdit("password of session")
        self.password_prompt.textEdited.connect(self.__password_input_edited)


        self.username_input = ""
        self.password_input = ""



        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)


        self.buttonBox.accepted.connect(self.__send_data)
        self.buttonBox.rejected.connect(self.reject)

        self.main_layout.addWidget(self.username_prompt)
        self.main_layout.addWidget(self.password_prompt)
        self.main_layout.addWidget(self.buttonBox)

        self.setLayout(self.main_layout)

    def __username_input_edited(self, text):
        self.username_input = text

    def __password_input_edited(self, text):
        self.password_input = text

    def __send_data(self):
        self.session_widget.set_join_username(self.username_input)
        self.session_widget.set_join_password(self.password_input)
        self.accept()


class SessionWidget(QMainWindow):
    def __init__(self, toolbox:Toolbox, home_window):
        super().__init__()
        self.toolbox = toolbox
        self.map_ref = self.toolbox.get_hextile_map_ref()
        self.account_ref = self.toolbox.get_account_ref()
        self.client_session_ref = self.toolbox.get_client_session_ref()
        self.server_session_ref = self.toolbox.get_server_session_ref()
        self.home_window = home_window
        self.setWindowTitle("Account Manager")

        self.setStyleSheet("background-color: #F0F2A6")


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
        username = self.account_ref.get_username()
        if(self.client_session_ref.get_live_status()):
            label_txt = f"Welcome {username}! You are currently in a session! Have fun!"
            self.user_label = QLabel(label_txt)
            self.main_layout.addWidget(self.user_label)
        elif(self.server_session_ref.get_live_status()):
            password = self.server_ref.get_password()
            label_txt = f"Welcome {username}! You are currently hosting a session! The password is: {password}"
            self.user_label = QLabel(label_txt)
            self.main_layout.addWidget(self.user_label)
        else:
            label_txt = f"Welcome {username}! Would you like to join or start hosting a session?"
            self.user_label = QLabel(label_txt)
            self.start_session_btn = QPushButton("Start Session")
            self.start_session_btn.clicked.connect(self.__start_session)
            self.join_session_btn = QPushButton("Join Session")
            self.join_session_btn.clicked.connect(self.__join_session)

            self.main_layout.addWidget(self.user_label)
            self.main_layout.addWidget(self.start_session_btn)
            self.main_layout.addWidget(self.join_session_btn)

    def __layout_without_acc(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.change_form_btn = QPushButton("Don't have an account? Sign up here!")
        self.change_form_btn.clicked.connect(partial(self.__change_form, "signup"))
        self.change_form_btn.setFlat(True)
        
        change_form_row = QHBoxLayout()
        change_form_row.addWidget(spacer)
        change_form_row.addWidget(self.change_form_btn)
        change_form_row.addWidget(spacer)
        self.main_layout.addStretch()
        self.main_layout.addLayout(change_form_row)

        self.email_label = QLabel("Email")
        self.email_label.hide()
        self.email_prompt = QLineEdit()
        self.email_prompt.textEdited.connect(self.__email_input_edited)
        self.email_prompt.hide()

        email_row = QHBoxLayout()
        email_row.addStretch()
        email_row.addWidget(self.email_label)
        email_row.addWidget(self.email_prompt)
        email_row.addStretch()


        self.username_label = QLabel("Username")
        self.username_prompt = QLineEdit()
        self.username_prompt.textEdited.connect(self.__username_input_edited)
        
        username_row = QHBoxLayout()
        username_row.addStretch()
        username_row.addWidget(self.username_label)
        username_row.addWidget(self.username_prompt)
        username_row.addStretch()

        self.password_label = QLabel("Password")
        self.password_prompt = QLineEdit()
        self.password_prompt.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_prompt.textEdited.connect(self.__password_input_edited)

        password_row = QHBoxLayout()
        password_row.addStretch()
        password_row.addWidget(self.password_label)
        password_row.addWidget(self.password_prompt)
        password_row.addStretch()

        self.log_in_btn = QPushButton("Log In")
        self.log_in_btn.clicked.connect(self.__try_log_in)


        self.sign_up_btn = QPushButton("Sign Up")
        self.sign_up_btn.clicked.connect(self.__try_sign_up)
        self.sign_up_btn.hide()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.log_in_btn)
        btn_row.addWidget(self.sign_up_btn)
        btn_row.addStretch()

        self.main_layout.addLayout(email_row)
        self.main_layout.addLayout(username_row)
        self.main_layout.addLayout(password_row)
        self.main_layout.addLayout(btn_row)
        self.main_layout.addStretch()

    def __change_form(self, new_type):
        if(new_type == "signup"):
            self.change_form_btn.setText("Already have an account? Log in here!")
            self.log_in_btn.hide()
            self.email_prompt.show()
            self.email_label.show()
            self.sign_up_btn.show()
            self.change_form_btn.clicked.disconnect()
            self.change_form_btn.clicked.connect(partial(self.__change_form, "login"))

        else:
            self.change_form_btn.setText("Don't have an account? Sign up here!")
            self.sign_up_btn.hide()
            self.email_prompt.hide()
            self.email_label.hide()
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
            self.main_layout = QVBoxLayout()    
            self.__layout_with_acc()
            self.toolbox.reset_tokens_to_database()
            self.toolbox.get_saved_maps_ref().fetch_from_database()
            self.close()


    def __try_sign_up(self):
        msg = self.account_ref.try_sign_up(email=self.email_input, username=self.username_input, password=self.password_input)
        self.__clear_input()
        if(msg == DatabaseMessages.SUCCESS):
            print("success")
            self.__change_form("login")


    def __start_session(self):
        self.self.server_session_ref.start_session()
        self.map_ref.saveMap(local=False, can_save_to_db=False)
        self.close()

    def set_join_username(self, text):
        self.username_input = text

    def set_join_password(self, text):
        self.password_input = text

    def __join_session(self):
        dlg = FindSessionDialog(self)
        ok = dlg.exec()
        if(ok):
            self.client_session_ref.set_home_window(self.home_window)
            self.client_session_ref.connect_to_host(self.username_input, self.password_input)
        self.username_input = ""
        self.password_input = ""

    def __change_session_pass_view(self):
        if(self.session_pass_label.isVisible()):
            self.session_pass_label.hide()
            self.session_pass_btn.setText("Show Session Password")
        else:
            self.session_pass_label.show()
            self.session_pass_btn.setText("Hide Session Password")


        

    
    