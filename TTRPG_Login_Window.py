#Python application for TTRPG login/registration using PyQt6 and SQL Server with SQLAlchemy ORM. Passwords are hashed with bcrypt for security.
#You need the following Python packages: pyqt6, sqlalchemy, pyodbc, and bcrypt. Install them using "pip install {package_name}"

#Imports the database connection code from the tester file.
import sys
import bcrypt
import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox
)

from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

#DATABASE SETUP SECTION
#Connection string to local SQL Server Express instance
connection_url = URL.create(
    "mssql+pyodbc",
    query={"odbc_connect": (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        r"SERVER=localhost\SQLEXPRESS;"
        "DATABASE=TTRPGUsersDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )}
)

#Creates the SQLAlchemy engine and session factory
engine = create_engine(connection_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()

#relation-mapping model that matches the accounts table in our server
class Account(Base):
    __tablename__ = "accounts"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

class SavedToken(Base):
    __tablename__ = "tokens"
    token_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("accounts.user_id"), nullable=False)
    token_name = Column(String(100), nullable=False)
    token_category = Column(String(50), nullable=False)
    token_data = Column(Text, nullable=False)

#creates a database table if none exists, otherwise it does nothing
Base.metadata.create_all(engine)

def save_token_record(user_id, token_name, token_category, token_dict):
    with SessionLocal() as session:
        new_token = SavedToken(
            user_id=user_id,
            token_name=token_name,
            token_category=token_category,
            token_data=json.dumps(token_dict)
        )
        session.add(new_token)
        session.commit()

def get_saved_token(user_id, token_name, token_category):
    with SessionLocal() as session:
        saved_token = session.execute(
            select(SavedToken).where(
                SavedToken.user_id == user_id,
                SavedToken.token_name == token_name,
                SavedToken.token_category == token_category
            )
        ).scalar_one_or_none()

        if saved_token is None:
            return None

        return json.loads(saved_token.token_data)

#GUI Section
class Window(QWidget):
    def __init__(self, home_window=None):
        super().__init__()
        self.home_window = home_window

        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("TTRPG App - Login/Register")
        self.setLayout(layout)

        title = QLabel("Enter your info to login or register.")
        layout.addWidget(title, 0, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        #username input
        layout.addWidget(QLabel("Username:"), 1, 0)
        self.input_user = QLineEdit()
        layout.addWidget(self.input_user, 1, 1, 1, 2)

        #email input (only required for Register)
        layout.addWidget(QLabel("Email:"), 2, 0)
        self.input_email = QLineEdit()
        layout.addWidget(self.input_email, 2, 1, 1, 2)

        #password input (hashes after)
        layout.addWidget(QLabel("Password:"), 3, 0)
        self.input_pwd = QLineEdit()
        self.input_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_pwd, 3, 1, 1, 2)

        #button for registering a new account
        button_register = QPushButton("Register")
        button_register.clicked.connect(self.register)
        layout.addWidget(button_register, 4, 1)

        #button for logging in with an existing account
        button_login = QPushButton("Login")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login, 4, 2)

    #register function that checks for existing username/email, hashes the password, and stores the new account in the database
    def register(self):
        username = self.input_user.text().strip()
        email = self.input_email.text().strip()
        password = self.input_pwd.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Missing info", "Username, email, and password are required to register.")
            return
        #hashes the password using bcrypt before storing it in the database
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        #tries to add the new account to the database, checking for existing username/email first and showing appropriate messages on success/failure
        try:
            with SessionLocal() as session:
                existing_user = session.execute(
                    select(Account).where(Account.username == username)
                ).scalar_one_or_none()
                if existing_user:
                    QMessageBox.warning(self, "Register failed", "That username is already taken.")
                    return

                existing_email = session.execute(
                    select(Account).where(Account.email == email)
                ).scalar_one_or_none()
                if existing_email:
                    QMessageBox.warning(self, "Register failed", "That email is already in use.")
                    return

                session.add(Account(username=username, email=email, password_hash=pw_hash))
                session.commit()

            QMessageBox.information(self, "Success", "Registered! You can log in now.")
            self.input_pwd.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database error", str(e))
    #login function that checks the entered username and password against the database, showing appropriate messages on success/failure
    def login(self):
        username = self.input_user.text().strip()
        password = self.input_pwd.text()

        #code block that makes email not required to log in (remove to force email input even on login)
        if not username or not password:
            QMessageBox.warning(self, "Missing info", "Enter username and password.")
            return

        #tries to find the account in the database and checks the password hash using bcrypt, showing appropriate messages on success/failure
        try:
            with SessionLocal() as session:
                user = session.execute(
                    select(Account).where(Account.username == username)
                ).scalar_one_or_none()

            if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
                QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            else:
                QMessageBox.critical(self, "Login Failed", "Invalid username or password.")

        except Exception as e:
            QMessageBox.critical(self, "Database error", str(e))

#runs the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())