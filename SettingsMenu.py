from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QGroupBox,
    QCheckBox,
    QPushButton
)

from Toolbox import Toolbox
from Enums.MapSizes import MapSizes

class SettingsMenu(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox):
        super().__init__()

        self.setWindowTitle("Settings")
        self.settings_ref = toolbox_ref.get_settings_ref()
        self.tile_types = toolbox_ref.get_tile_types_ref()
        self.new_map_size = self.settings_ref.getMapSize()
        self.map_size_dropdown_idx = 0
        match(self.new_map_size):
            case MapSizes.XSMALL: 
                self.map_size_dropdown_idx = 0
            case MapSizes.SMALL: 
                self.map_size_dropdown_idx = 1
            case MapSizes.MEDIUM: 
                self.map_size_dropdown_idx = 2
            case MapSizes.LARGE: 
                self.map_size_dropdown_idx = 3
            case MapSizes.XLARGE: 
                self.map_size_dropdown_idx = 4
            case _: 
                self.map_size_dropdown_idx = 2


        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.map_size_dropdown = QComboBox()
        self.map_size_dropdown_options = ["Extra Small", "Small", "Medium", "Large", "Extra Large"]
        self.map_size_dropdown.addItems(self.map_size_dropdown_options)
        self.map_size_dropdown.activated.connect(self.__on_dropdown_change)
        self.map_size_dropdown.setCurrentIndex(self.map_size_dropdown_idx)
        self.map_size_dropdown.setMaximumSize(100,100)


        self.checkbox_group = QGroupBox("Included Tiles")
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_group.setLayout(self.checkbox_layout)

        # !!!
        # This needs to be better
        tileNamesList = self.tile_types.getTileNamesList()
        for name in tileNamesList:
            new_checkbox = QCheckBox(text=str(name), parent=self)
            if(self.settings_ref.findExcludedType(name.upper())):
                new_checkbox.setChecked(True)
            else:
                new_checkbox.setChecked(False)
            new_checkbox.setStyleSheet("""
                QCheckBox::indicator:unchecked {
                    background-color: green;
                }
                QCheckBox::indicator:checked {
                    background-color: red;
                }
            """)   
            new_checkbox.toggled.connect(self.__on_checkbox_change)
            self.checkbox_layout.addWidget(new_checkbox)

        self.save_btn = QPushButton("Save Settings", self)
        self.save_btn.clicked.connect(self.__save_settings)


        self.main_layout.addWidget(self.checkbox_group)
        self.main_layout.addWidget(self.map_size_dropdown)
        self.main_layout.addWidget(self.save_btn)
        self.setCentralWidget(self.main_widget)

    def __on_dropdown_change(self, index):
        self.new_map_size = MapSizes.getMapSizeFromStr(self.map_size_dropdown_options[index])

    def __on_checkbox_change(self, state):
        checkbox = self.sender()
        if(state):
            self.settings_ref.addExcludedType(checkbox.text().upper())
        else: 
            self.settings_ref.removeExcludedType(checkbox.text().upper())

    def __save_settings(self):
        self.settings_ref.setMapSize(self.new_map_size)
        self.close()