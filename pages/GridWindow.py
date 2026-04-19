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
    QMessageBox,
    QPushButton
)

import base64
from Enums.TokenTypes import TokenTypes
from widgets.GenericContainerWidget import TokenContainerWidget
from widgets.GenericContainerWidget import TokenRecordContainerWidget

import math
from functools import partial
import os


from HextileNode import HextileNode
from toolbox.Toolbox import Toolbox
from TokenRecord import TokenRecord




          



class QMapWidget(QWidget):
    def __init__(self, toolbox:Toolbox, background_img_path):
        super().__init__()
        self.toolbox = toolbox
        self.screen_width = self.toolbox.get_screen_width()
        self.screen_height = self.toolbox.get_screen_height()
        self.settings_ref = self.toolbox.get_settings_ref()
        self.tile_size = self.settings_ref.getTileSize()
        self.background_img_path = background_img_path

    def reload_tile_size(self):
        self.tile_size = self.settings_ref.getTileSize()

    def set_background_img(self, new_background_img):
        self.background_img_path = new_background_img

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

    def keyPressEvent(self, event):
        print("Map Widget")


class TokenLabel(QLabel):
    def __init__(self, toolbox:Toolbox, token_record:TokenRecord, grid_window, parent=None):
        super().__init__(parent=parent)
        self.toolbox = toolbox
        self.settings_ref = self.toolbox.get_settings_ref()
        self.token_record = token_record
        self.grid_window = grid_window
        self.token_record_window = None
        self.scroll = None
        self.dragging = False
        self.old_x = 0
        self.old_y = 0
        
    def get_token_record(self) -> TokenRecord:
        return self.token_record

    def mousePressEvent(self, event):
        self.grid_window.deselect_token_label()
        if(event.button() == Qt.MouseButton.LeftButton):
            pos = self.mapToGlobal(event.position())
            self.old_x = pos.x()
            self.old_y = pos.y()
            self.dragging = True
        if(event.button() == Qt.MouseButton.RightButton):
            if(self.token_record_window is None):
                self.scroll = QScrollArea()
                self.scroll.setWidgetResizable(True)
                self.token_record_window = TokenRecordContainerWidget(self.token_record, self.toolbox, self)
                self.scroll.setWidget(self.token_record_window)
            self.scroll.show()
        event.accept()

    def mouseReleaseEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            if(self.dragging):
                self.dragging = False
                global_pos = self.mapToGlobal(event.position())
                x = global_pos.x()
                y = global_pos.y()
                tile_size = self.settings_ref.getTileSize()
                if(abs(self.old_x - x) < tile_size and abs(self.old_y - y) < tile_size):
                    self.grid_window.select_token_label(self)
                else:
                    self.grid_window.move_token_label(self, global_pos)
        event.accept()

    def delete_token(self):
        self.grid_window.delete_token(self, self.token_record)
        self.scroll.close()
        self.token_record_window = None

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

        self.selected_label = None

        self.middle_x = 0
        self.middle_y = 0

        self.snap_positions = []


        self.main_widget = QWidget()
        
        self.toolbar = QToolBar()
        self.__compute_snap_positions()
        self.__setup_token_dropdowns()

        self.change_tile_size = QPushButton("Tile Size")
        self.change_tile_size.clicked.connect(self.__change_tile_size)
        self.toolbar.addWidget(self.change_tile_size)

        self.change_background_btn = QPushButton("Background Image")
        self.change_background_btn.clicked.connect(self.__change_background_img)
        self.toolbar.addWidget(self.change_background_btn)


        self.map_widget = QMapWidget(self.toolbox, self.background_img_path)

        self.__initial_token_setup()


        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.map_widget)


        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)
        self.showMaximized()


    def __change_tile_size(self):
        old_tile_size = self.settings_ref.getTileSize()
        tile_size, ok = QInputDialog.getText(self, "Tile Size", str(old_tile_size))
        if ok and tile_size:
            try:
                new_tile_size = int(tile_size)
                self.tile_size = new_tile_size
                self.settings_ref.setTileSize(new_tile_size)
                self.map_widget.reload_tile_size()
                self.__compute_snap_positions()
                self.__move_existing_tokens()
                self.map_widget.update()
            except ValueError:
                print("Value error")


    def __change_background_img(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select an image!")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            try:
                selected_files_list = file_dialog.selectedFiles()
                img_path = selected_files_list[0]
                img_name = os.path.basename(img_path)

                img_name = img_name.replace(".jpg", ".png")
                img_name = img_name.replace(".jpeg", ".png")
                cur_dir = os.getcwd()
                asset_dir = os.path.join(cur_dir, "assets")
                asset_path = os.path.join(asset_dir, img_name)
                os.rename(img_path, asset_path)

                self.map_widget.set_background_img(asset_path)
                self.tile_types_ref.set_default_tile_background_by_name(self.old_tile_name, asset_path)
                self.map_widget.update()
            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")

    def delete_token(self, token_label, token_record):
        token_label.deleteLater()
        self.tile_record.remove_empty_position(token_record.get_position())
        self.tile_record.delete_token_record(token_record)

    def deselect_token_label(self):
        self.selected_label = None

    def select_token_label(self, label):
        self.selected_label = label

    def move_token_label(self, label, global_pos):
        local_pos = self.mapFromGlobal(global_pos)
        local_x = local_pos.x()
        local_y = local_pos.y()

        closest_pos = None
        closest_dist = float('inf')
        radius = self.tile_size // 2

        for x, y in self.snap_positions:
            dx = local_x - x
            dy = local_y - y
            dist = (dx**2 + dy**2)**(1/2)

            if dist < closest_dist and dist <= radius ** 2:
                closest_dist = dist
                closest_pos = (x, y)

        if closest_pos:
            new_x, new_y = closest_pos
            token_record = label.get_token_record()
            old_pos = token_record.get_position()

            if not self.tile_record.check_position_filled((new_x, new_y)):
                token_record.set_position((new_x, new_y))
                self.tile_record.remove_empty_position((new_x, new_y))
                self.tile_record.add_empty_position(old_pos)
                label.move(QPoint(new_x - label.width(), new_y - label.height()))

    def __compute_snap_positions(self):
        self.snap_positions.clear()
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
            title = title[0:1].upper() + title[1:len(title)]
            title_str = title + " Tokens"
            icon_str = ref.get_asset_str()
            icon = QIcon(icon_str)
            combo = QComboBox()
            token_type = ref.get_token_type()
            combo.currentTextChanged.connect(partial(self.__token_selected, token_ref=ref, combo=combo, token_type=token_type))
            combo.addItem(icon, title_str)
            for token in ref.get_tokens_list():
                name = token["name"]
                icon = None
                data = token["set_map_asset"]
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                icon = QIcon(pixmap)
                combo.addItem(icon, name)
            self.toolbar.addWidget(combo)

    def __initial_token_setup(self):
        token_records = self.tile_record.get_token_records()
        for token_record in token_records:
            token_label = TokenLabel(self.toolbox, token_record, self, parent=self.map_widget)
            save_location = token_record.get_save_location()
            pixmap = QPixmap()
            data = token_record.get_map_asset()
            pixmap.loadFromData(data)
            scaled_pixmap = pixmap.scaled(
                self.tile_size, self.tile_size,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode =Qt.TransformationMode.SmoothTransformation
            )

            token_label.setPixmap(scaled_pixmap)
            token_label.resize(self.tile_size, self.tile_size)
            token_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            x_pos = token_record.get_x_position()
            y_pos = token_record.get_y_position()
            token_label.move(x_pos, y_pos)

            self.token_labels.append(token_label)


    def __token_selected(self, text, token_ref=None, combo=None, token_type=None):
        if(not "Tokens" in text):
            token = token_ref.get_token_by_name(text)
            token_record = TokenRecord(self.logger_ref, token, token_type, position=(self.middle_x, self.middle_y))
            self.tile_record.add_token_record(token_record)
            token_label = TokenLabel(self.toolbox, token_record, self, parent=self.map_widget)
            data = token_record.get_map_asset()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            scaled_pixmap = pixmap.scaled(
                self.tile_size, self.tile_size,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode =Qt.TransformationMode.SmoothTransformation
            )



            token_label.setPixmap(scaled_pixmap)
            token_label.resize(self.tile_size, self.tile_size)
            token_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            token_label.move(self.middle_x, self.middle_y)

            token_label.show()
            self.token_labels.append(token_label)
            combo.setCurrentIndex(0)


    def __move_existing_tokens(self):
        for token_label in self.token_labels:
            min_dist = 100000
            token_record = token_label.get_token_record()
            cur_pos = token_record.get_position()
            cur_x = cur_pos[0]
            cur_y = cur_pos[1]
            new_x = cur_x
            new_y = cur_y
            for pos in self.snap_positions:
                x = pos[0]
                y = pos[1]
                x_diff = abs(cur_x - x)
                y_diff = abs(cur_y - y)
                if(x_diff < 1 and y_diff < 1):
                    dist = ((x_diff ** 2) + (y_diff ** 2)) ** 0.5
                    if(dist < min_dist):
                        min_dist = dist
                        new_x = x
                        new_y = y
            pixmap = token_label.pixmap()
            scaled_pixmap = pixmap.scaled(
                self.tile_size, self.tile_size,
                aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                transformMode =Qt.TransformationMode.SmoothTransformation
            )
            token_label.setPixmap(scaled_pixmap)
            token_label.resize(self.tile_size, self.tile_size)
            token_label.move(new_x, new_y)

    def keyPressEvent(self, event):
        print("Parent")
        if(not self.selected_label is None):
            if event.key() == Qt.Key.Key_Left:
                print("left")
            if event.key() == Qt.Key.Key_Right:
                print("right")

