from toolbox.Database import Database
from toolbox.Database import DatabaseMessages

class Account():
    def __init__(self):
        self.logged_in = False
        self.username = ""
        self.account_id = -1
       

    def get_logged_in(self) -> bool:
        return self.logged_in

    def get_username(self) -> str:
        return self.username

    def get_account_id(self) -> int:
        return self.account_id

    def try_log_in(self, username="", password=""):
        msg, user_id = Database.check_user(username, password)
        if(msg == DatabaseMessages.SUCCESS):
            self.account_id = user_id
            self.username = username
            self.logged_in = True
        return msg

    def try_sign_up(self, username="", password="", email=""):
        msg, user_id = Database.create_new_user(username, email, password)
        if(msg == DatabaseMessages.SUCCESS):
            self.account_id = user_id
            self.username = username
            self.logged_in = True
        return msg

    def log_out(self):
        self.logged_in = False
        self.username = ""
        self.account_id = -1