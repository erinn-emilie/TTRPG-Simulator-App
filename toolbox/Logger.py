import copy
from datetime import datetime as dt
from toolbox.Database import Database

class Logger():
    def __init__(self, account_ref, log_file_path = "logfiles/TemporaryLog.txt", writable=False):
        self.log_file_path = log_file_path
        self.save_path = self.log_file_path
        self.map_name = "TemporaryLog"
        self.log_contents = []
        self.last_session_contents = []
        self.current_session_contents = []
        self.__populate_log()
        self.writable = writable
        self.account_ref = account_ref


    def set_writable_status(self, status:bool):
        self.writable = status

    def get_writable_status(self) -> bool:
        return self.writable

    def clear_contents(self):
        self.log_contents.clear()
        self.last_session_contents.clear()
        self.current_session_contents.clear()

    def __populate_log(self, local=True):
        self.log_contents.clear()
        self.last_session_contents.clear()   
        if(local):
            try:
                with open(self.log_file_path, 'r') as file:
                    for line in file:
                        self.log_contents.append(line.strip())
                self.last_session_contents = copy.deepcopy(self.log_contents)
            except FileNotFoundError:
                print("Cannot find the log file!")
        else:
            user_id = self.account_ref.get_account_id()
            log_string = Database.fetch_log_contents(user_id, self.map_name)
            log_split = log_string.split("\n")
            for line in log_split:
                self.log_contents.append(line.strip())

    def __rewrite_log_file(self, local=True):
        if(local):
            try:
                with open(self.save_path, 'w') as file:
                    for line in self.log_contents:
                        line += "\n"
                        file.write(line)
            except FileNotFoundError:
                print("Cannot find the old log file to save!")
        else:
            user_id = self.account_ref.get_account_id()
            Database.save_log_file(user_id, self.map_name, self.log_contents)

    def get_all_log_contents(self) -> list:
        return self.log_contents

    def get_last_session_contents(self) -> list:
        return self.last_session_contents

    def get_current_session_contents(self) -> list:
        return self.current_session_contents

    def get_last_logged_line(self) -> str:
        return self.log_contents[len(self.log_contents) - 1]

    def add_line(self, line:str):
        now = dt.now()
        cur_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        full_line = line + "  " + cur_time_str

        self.log_contents.append(full_line)
        self.current_session_contents.append(full_line)

    def change_save_path(self, path:str, map_name:str):
        self.save_path = path
        self.map_name = map_name

    def save_log(self, local=True):
        if(local):
            self.__rewrite_log_file()
        else:
            user_id = self.account_ref.get_account_id()
            Database.save_log_file(user_id, self.map_name, self.log_contents)

    def open_new_log(self, new_file_name, save_old_log=True, local=True):
        if(save_old_log):
            self.__rewrite_log_file(local=local)
        new_file_path = f"jsonfiles/{new_file_name}.txt"
        self.change_save_path(new_file_path, new_file_name)
        self.__populate_log(local=local)

    def change_to_temporary(self, save_old_log=True, local=True):
        if(save_old_log):
            self.__rewrite_log_file(local=local)
        self.change_save_path("jsonfiles/TemporaryLog.txt", "TemporaryLog")
        self.log_contents = []
        self.last_session_contents = []
        self.current_session_contents = []


