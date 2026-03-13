import copy

class Logger():
    def __init__(self, log_file_path = "logfiles/TemporaryLog.txt", writable=False):
        self.log_file_path = log_file_path
        self.save_path = self.log_file_path
        self.log_contents = []
        self.last_session_contents = []
        self.current_session_contents = []
        self.__populate_log()
        self.writable = writable


    def set_writable_status(self, status:bool):
        self.writable = status

    def get_writable_status(self) -> bool:
        return self.writable

    def __populate_log(self):
        self.log_contents.clear()
        self.last_session_contents.clear()
        try:
            with open(self.log_file_path, 'r') as file:
                for line in file:
                    self.log_contents.append(line.strip())
            self.last_session_contents = copy.deepcopy(self.log_contents)
        except FileNotFoundError:
            print("Cannot find the log file!")

    def __rewrite_log_file(self):
            try:
                with open(self.save_path, 'w') as file:
                    for line in self.log_contents:
                        line += "\n"
                        file.write(line)
            except FileNotFoundError:
                print("Cannot find the old log file to save!")

    def get_all_log_contents(self) -> list:
        return self.log_contents

    def get_last_session_contents(self) -> list:
        return self.last_session_contents

    def get_current_session_contents(self) -> list:
        return self.current_session_contents

    def get_last_logged_line(self) -> str:
        return self.log_contents[len(self.log_contents) - 1]

    def add_line(self, line:str):
        self.log_contents.append(line)
        self.current_session_contents.append(line)

    def change_save_path(self, path:str):
        self.save_path(path)

    def open_new_log(self, new_file_path, save_old_log=True):
        if(save_old_log):
            self.__rewrite_log_file()
        self.log_file_path = new_file_path
        self.__populate_log()


