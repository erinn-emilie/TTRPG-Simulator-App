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
    QComboBox
)

from Enums.TokenTypes import TokenTypes
from widgets.GenericContainerWidget import TokenContainerWidget
from widgets.GenericContainerWidget import TokenRecordContainerWidget

import math
from functools import partial


from HextileNode import HextileNode
from toolbox.Toolbox import Toolbox
from TokenRecord import TokenRecord

class QMapWidget(QWidget):
    def __init__(self, screen_width, screen_height, tile_size, background_img_path):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = tile_size
        self.background_img_path = background_img_path

    def paintEvent(self, event):
        painter = QPainter(self)

        pixmap = QPixmap(self.background_img_path)

        pen = QPen(QColor(0, 0, 0), 1)
        painter.setPen(pen)
        painter.drawPixmap(self.rect(), pixmap)

        left = 0
        right = self.screen_width
        top = 0
        bottom = self.screen_height

        lines = []

        for x in range(0, self.screen_width, self.tile_size):
            lines.append(QLineF(x, top, x, bottom))

        for y in range(0, self.screen_height, self.tile_size):
            lines.append(QLineF(left, y, right, y))

        painter.drawLines(lines)


class TokenLabel(QLabel):
    def __init__(self, toolbox:Toolbox, token_record:TokenRecord, grid_window, parent=None):
        super().__init__(parent=parent)
        self.toolbox = toolbox
        self.token_record = token_record
        self.grid_window = grid_window
        self.dragging = False
        
    def get_token_record(self) -> TokenRecord:
        return self.token_record

    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            self.dragging = True
        event.accept()

    def mouseReleaseEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            if(self.dragging):
                self.dragging = False
                global_pos = self.mapToGlobal(event.position())
                self.grid_window.move_token_label(self, global_pos)
        event.accept()

class GridWindow(QMainWindow):
    def __init__(self, hex_node:HextileNode, toolbox:Toolbox):
        super().__init__()
        self.toolbox = toolbox
        self.token_labels = []
        self.logger_ref = self.toolbox.get_logger_ref()
        self.settings_ref = self.toolbox.get_settings_ref()
        self.tile_size = self.settings_ref.getTileSize()
        self.hex_node = hex_node
        self.tile_record = self.hex_node.getTileRecord()
        self.tile_type = self.tile_record.get_tile_type()

        self.tile_types_ref = self.toolbox.get_tile_types_ref() 
        self.background_img_path = self.tile_types_ref.get_default_tile_background_by_name(self.tile_type)

        self.screen_width = self.toolbox.get_screen_width()
        self.screen_height = self.toolbox.get_screen_height()

        self.middle_x = 0
        self.middle_y = 0

        self.snap_positions = []


        self.main_widget = QWidget()
        
        self.toolbar = QToolBar()
        self.__compute_snap_positions()
        self.__setup_token_dropdowns()


        self.map_widget = QMapWidget(self.screen_width, self.screen_height, self.tile_size, self.background_img_path)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.map_widget)


        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)


    def move_token_label(self, label, global_pos):
        local_pos = self.mapFromGlobal(global_pos)
        local_x = local_pos.x()
        local_y = local_pos.y()

        new_x = -1
        new_y = -1

        min_dist = 100000
        for pos in self.snap_positions:
            x = pos[0]
            y = pos[1]

            dist = (((local_x - x) ** 2) + ((local_y - y) ** 2)) ** 0.5

            if(dist < min_dist):
                min_dist = dist
                new_x = x
                new_y = y

        if(new_x > -1 and new_y > -1):
            token_record = label.get_token_record()
            old_pos = token_record.get_position()
            new_pos = (new_x, new_y)
            token_record.set_position(new_pos)
            if(not self.tile_record.check_position_filled(new_pos)):
                self.tile_record.remove_empty_position(new_pos)
                self.tile_record.add_empty_position(old_pos)
                point = QPoint(new_x, new_y)
                label.move(point)


    def __compute_snap_positions(self):
        rows = int(self.screen_height / self.tile_size)
        cols = int(self.screen_width / self.tile_size)
        middle_row = int(rows/2)
        middle_col = int(cols/2)
        x_count = 0
        y_count = 0

        for x in range(0, self.screen_width, self.tile_size):
            x_count += 1
            y_count = 0
            for y in range(0, self.screen_height, self.tile_size):
                y_count += 1
                self.snap_positions.append((x, y))

                if(x_count == middle_col and y_count == middle_row):
                    self.middle_x = x
                    self.middle_y = y
        self.tile_record.fill_empty_positions(self.snap_positions)


    def __setup_token_dropdowns(self):
        token_refs_list = self.toolbox.get_list_of_token_refs()
        for ref in token_refs_list:
            title = ref.get_title_str()
            title_str = "Choose a " + title
            icon_str = ref.get_asset_str()
            icon = QIcon(icon_str)
            combo = QComboBox()
            token_type = ref.get_token_type()
            combo.currentTextChanged.connect(partial(self.__token_selected, token_ref=ref, combo=combo, token_type=token_type))
            combo.addItem(icon, title_str)
            for token in ref.get_tokens_list():
                name = token["name"]
                asset_str = token["set_map_asset"]
                icon = QIcon(asset_str)
                combo.addItem(icon, name)
            self.toolbar.addWidget(combo)


    def __token_selected(self, text, token_ref=None, combo=None, token_type=None):
        if(not "Choose a" in text):
            token = token_ref.get_token_by_name(text)
            token_record = TokenRecord(self.logger_ref, token, token_type, position=(self.middle_x, self.middle_y))
            self.tile_record.add_token_record(token_record)
            token_label = TokenLabel(self.toolbox, token_record, self, parent=self.map_widget)
            asset_path = token_record.get_map_asset()
            pixmap = QPixmap(asset_path)
            pixmap = pixmap.scaled(self.tile_size, self.tile_size)



            token_label.setPixmap(pixmap)
            token_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            token_label.move(self.middle_x, self.middle_y)

            token_label.show()
            self.token_labels.append(token_label)
            combo.setCurrentIndex(0)


