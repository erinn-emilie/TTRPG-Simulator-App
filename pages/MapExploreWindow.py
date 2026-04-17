from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QPushButton,
    QScrollArea,
    QCheckBox,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QMessageBox
)

from PyQt6.QtCore import Qt

from functools import partial

from toolbox.Toolbox import Toolbox

from toolbox.Database import Database
from toolbox.Database import DatabaseMessages

class MapExploreWindow(QMainWindow):
    def __init__(self, toolbox:Toolbox, home_window):
        super().__init__()
        self.title = "Custom Map Menu"
        self.setWindowTitle(self.title)

        self.home_window = home_window

        self.toolbox = toolbox
        self.saved_maps_ref = self.toolbox.get_saved_maps_ref()
        self.account_ref = self.toolbox.get_account_ref()

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.__setup_layout()

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)


    def __setup_layout(self):
        saved_maps = self.saved_maps_ref.get_all_saved_maps()

        for map_name in saved_maps:
            location = saved_maps[map_name]["save_location"]
            name_label = QLabel(map_name)

            row = QHBoxLayout()
            row.addWidget(name_label)

            load_btn = QPushButton("Load Map")
            load_btn.clicked.connect(partial(self.__load_map, map_name))
            row.addWidget(load_btn)

            if("database" in location):
                database_checkbox = QCheckBox(text="Saved to account.")
                database_checkbox.setChecked(True)
                database_checkbox.toggled.connect(partial(self.__change_save_location, map_name=map_name, map_dict=saved_maps[map_name], checkbox=database_checkbox))
                row.addWidget(database_checkbox)
            self.main_layout.addLayout(row)


    def __change_save_location(self, status, map_name="", map_dict=None, checkbox=None):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Save Map")
        if(status):
            if(self.account_ref.get_logged_in()):
                user_id = self.account_ref.get_account_id()
                message = Database.add_map_to_db(user_id, map_name, map_dict)
                map_dict["save_location"] = "database"
                if(message == DatabaseMessages.SUCCESS):
                    dlg.setText("Map saved to your account!")
                    dlg.exec()
                    self.saved_maps_ref.remove_saved_map(map_name)
                else:
                    dlg.setText("Something went wrong! Please try again!")
                    dlg.exec()
                    checkbox.setChecked(False)
            else:
                dlg.setText("Please log in or sign up to save a map to your account!")
                dlg.exec()
                checkbox.setChecked(False)
        else:
            self.saved_maps_ref.remove_saved_map(map_name, local=False)
            map_dict["save_location"] = "local"
            self.saved_maps_ref.add_saved_map(map_name, map_dict)

    def __load_map(self, map_name):
        self.home_window.load_saved_map(map_name)
