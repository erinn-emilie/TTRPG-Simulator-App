from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QGroupBox,
    QCheckBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QSizePolicy
)

from toolbox.Toolbox import Toolbox
from Enums.MapSizes import MapSizes
from Enums.TileGenerationTypes import TileGenerationTypes

class SettingsMenu(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setStyleSheet("background-color: #F0F2A6;")
        self.settings_ref = toolbox_ref.get_settings_ref()
        self.tile_types = toolbox_ref.get_tile_types_ref()
        self.new_map_size = self.settings_ref.getMapSize()
        self.new_rand_type = self.settings_ref.getRandType()
        self.map_size_dropdown_idx = 2
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

        self.tile_gen_type_dropdown_idx = 1
        match(self.new_rand_type):
            case TileGenerationTypes.RANDOM:
                self.tile_gen_type_dropdown_idx = 0
            case TileGenerationTypes.WEIGHTED:
                self.tile_gen_type_dropdown_idx = 1


        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.map_size_dropdown = QComboBox()
        self.map_size_dropdown_options = ["Extra Small", "Small", "Medium", "Large", "Extra Large"]
        self.map_size_dropdown.addItems(self.map_size_dropdown_options)
        self.map_size_dropdown.activated.connect(self.__on_map_dropdown_change)
        self.map_size_dropdown.setCurrentIndex(self.map_size_dropdown_idx)
        self.map_size_dropdown.setMaximumSize(100,100)
        self.map_size_dropdown.setStyleSheet("""background-color: #392061; color: #F0F2A6; padding: 3px;""")

        self.tile_gen_type_dropdown = QComboBox()
        self.tile_gen_type_dropdown_options = ["Random", "Weighted"]
        self.tile_gen_type_dropdown.addItems(self.tile_gen_type_dropdown_options)
        self.tile_gen_type_dropdown.activated.connect(self.__on_tile_gen_dropdown_change)
        self.tile_gen_type_dropdown.setCurrentIndex(self.tile_gen_type_dropdown_idx)
        self.tile_gen_type_dropdown.setMaximumSize(100,100)
        self.tile_gen_type_dropdown.setStyleSheet("""background-color: #392061; color: #F0F2A6; padding: 3px;""")


        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  

        self.main_layout.addStretch()



        self.checkbox_group = QGroupBox("Included Tiles")
        self.checkbox_group.setStyleSheet("color: #1A1B25;")
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_group.setLayout(self.checkbox_layout)

        self.checked_boxes = 0
        self.total_boxes = 0

        tileNamesList = self.tile_types.get_tile_names_list()
        for name in tileNamesList:
            new_checkbox = QCheckBox(text=str(name), parent=self)
            if(self.settings_ref.findExcludedType(name.upper())):
                new_checkbox.setChecked(True)
            else:
                new_checkbox.setChecked(False)
            new_checkbox.setStyleSheet("""
                QCheckBox::indicator:unchecked {
                    background-color: #AA6373;
                }
                QCheckBox::indicator:checked {
                    background-color: #1A1B25;
                }
            """)   
            new_checkbox.toggled.connect(self.__on_checkbox_change)
            self.total_boxes += 1
            self.checkbox_layout.addWidget(new_checkbox)

        self.save_btn = QPushButton("Save Settings", self)
        self.save_btn.clicked.connect(self.__save_settings)

        self.save_btn.setStyleSheet("""background-color: #392061; color: #F0F2A6; padding: 10px;""")
  

        row = QHBoxLayout()
        row.addWidget(spacer)
        row.addWidget(self.checkbox_group)
        row.addWidget(spacer)

        self.main_layout.addLayout(row)


        map_size_row = QHBoxLayout()
        map_size_label = QLabel("Pick the size of your map!")
        map_size_label.setStyleSheet("color: #1A1B25")
        map_size_row.addStretch()
        map_size_row.addWidget(map_size_label)
        map_size_row.addWidget(self.map_size_dropdown)
        map_size_row.addStretch()
        self.main_layout.addLayout(map_size_row)

        tile_gen_row = QHBoxLayout()
        tile_gen_label = QLabel("Pick the type of tile generation!")
        tile_gen_label.setStyleSheet("color: #1A1B25")
        tile_gen_row.addStretch()
        tile_gen_row.addWidget(tile_gen_label)
        tile_gen_row.addWidget(self.tile_gen_type_dropdown)
        tile_gen_row.addStretch()
        self.main_layout.addLayout(tile_gen_row)

        save_btn_row = QHBoxLayout()
        save_btn_row.addStretch()
        save_btn_row.addWidget(self.save_btn)
        save_btn_row.addStretch()


        self.main_layout.addLayout(save_btn_row)
        self.main_layout.addStretch()
        self.setCentralWidget(self.main_widget)

    def __on_map_dropdown_change(self, index):
        self.new_map_size = MapSizes.getMapSizeFromStr(self.map_size_dropdown_options[index])

    def __on_tile_gen_dropdown_change(self, index):
        self.new_rand_type = TileGenerationTypes.get_gen_type_from_key(index)

    def __on_checkbox_change(self, state):
        checkbox = self.sender()
        if(state):
            self.checked_boxes += 1
            self.settings_ref.addExcludedType(checkbox.text().upper())
            if(self.checked_boxes > self.total_boxes // 3):
                checkbox.setChecked(False)
        else: 
            self.settings_ref.removeExcludedType(checkbox.text().upper())
            self.checked_boxes -= 1

    def __save_settings(self):
        self.settings_ref.setMapSize(self.new_map_size)
        self.settings_ref.setRandType(self.new_rand_type)
        self.close()