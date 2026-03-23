from PyQt6.QtCore import Qt, QMimeData
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
    QGridLayout
)

from Enums.TokenTypes import TokenTypes
from widgets.GenericContainerWidget import TokenContainerWidget
from widgets.GenericContainerWidget import TokenRecordContainerWidget

import math
from functools import partial


from HextileNode import HextileNode
from toolbox.Toolbox import Toolbox
from TokenRecord import TokenRecord


class TokenLabel(QLabel):
    def __init__(self, toolbox, token_record=None, row=-1, col=-1, parent=None, grid_window=None):
        super().__init__(parent=parent)
        self.token_record = token_record
        self.grid_window = grid_window
        self.row = row
        self.col = col
        self.toolbox = toolbox


    def get_token_record(self) -> TokenRecord:
        return self.token_record

    def set_token_record(self, token_record:TokenRecord):
        self.token_record = token_record

    def get_row(self) -> int:
        return self.row

    def set_row(self, new_row:int):
        self.row = new_row

    def get_col(self) -> int:
        return self.col

    def set_col(self, new_col:int):
        self.col = new_col

    def mouseMoveEvent(self, event):
        if(event.buttons() == Qt.MouseButton.LeftButton):
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.DropAction.MoveAction)

    def mousePressEvent(self, event):
        if(event.buttons() == Qt.MouseButton.RightButton):
            self.token_window = TokenRecordContainerWidget(self.token_record, self.toolbox)
            self.scroll = QScrollArea()
            self.scroll.setWidget(self.token_window)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scroll.setWidgetResizable(True)
            self.scroll.show()




class GridWindow(QMainWindow):
    def __init__(self, hexNode:HextileNode, toolbox:Toolbox):
        super().__init__()
        self.setAcceptDrops(True)
        self.hexNode = hexNode
        self.record = self.hexNode.getTileRecord()
        self.toolbox = toolbox
        self.logger_ref = self.toolbox.get_logger_ref()
        self.settings_ref = self.toolbox.get_settings_ref()
        self.seed_ref = self.settings_ref.getSeedRef()
        self.map_ref = self.toolbox.get_hextile_map_ref()
        self.all_labels = []
        self.label_being_dragged = None
        self.setStyleSheet("background-color:white;");


        tile_size = int(self.settings_ref.getTileSize())
        self.rows = tile_size
        self.cols = tile_size
        

        self.title = "Grid Window"
        self.setWindowTitle(self.title)



        self.token_bar = QDockWidget("TokenBar", self)
        self.token_bar.setDockLocation(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.token_bar.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.token_bar.setMinimumHeight(500)
        self.token_bar.setMaximumWidth(200)
        self.token_bar.setStyleSheet("background-color:white;");


        self.token_bar_container = QWidget()
        self.token_bar_layout = QVBoxLayout(self.token_bar_container)


        self.token_bar.setWidget(self.token_bar_container)

        self.__populate_token_bar()


        self.main_widget = QWidget()
        self.token_grid = QGridLayout()
        self.main_widget.setLayout(self.token_grid)

        #self.scroll = QScrollArea()
        #self.scroll.setWidget(self.main_widget)

        self.map_ref.positionTokensOnTile()
        self.__add_tokens_to_layout()
        self.setCentralWidget(self.main_widget)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        widget = event.source()
        token_record = widget.get_token_record()
        if not token_record is None:
            pixmap = widget.pixmap()
            widget.clear()


            grid_widget = self.token_grid.parentWidget()
            drop_pos = grid_widget.mapFromGlobal(event.position().toPoint())

            closest_row = widget.get_row()
            closest_col = widget.get_col()
            min_dist = float('inf')

            for row in range(self.rows):
                for col in range(self.cols):
                    item = self.token_grid.itemAtPosition(row, col)
                    if not item or not item.widget():
                        continue

                    w = item.widget()
                    w_pos = w.pos()
                    w_center_x = w_pos.x() + w.width() / 2
                    w_center_y = w_pos.y() + w.height() / 2


                    dist = ((drop_pos.x() - w_center_x) ** 2 + (drop_pos.y() - w_center_y) ** 2) ** 0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_row = row
                        closest_col = col

            target_item = self.token_grid.itemAtPosition(closest_row, closest_col)
            if target_item and target_item.widget():
                target_item.widget().setPixmap(pixmap)
                token_record.set_position((closest_row, closest_col))
                target_item.widget().set_token_record(token_record)
            


        event.accept()

    def __add_tokens_to_layout(self):
        all_tokens = self.record.get_all_tokens()

        for i in range(0, self.cols+1):
            for j in range(0, self.rows+1):
                label = TokenLabel(self.toolbox, parent=self, row=i, col=j, grid_window=self)
                label.setStyleSheet("QLabel { border: 1px solid black; background-color: white; padding: 5px; }")
                label.setScaledContents(True)
                self.token_grid.addWidget(label, i, j)

        for token in all_tokens:
            x_pos = token.get_x_position()
            y_pos = token.get_y_position()
            label = self.token_grid.itemAtPosition(x_pos, y_pos).widget()#TokenLabel(self.toolbox, token_record=token, row=x_pos, col=y_pos, parent=self, grid_window=self)
            label.setStyleSheet("QLabel { border: 1px solid blue; background-color: white; padding: 5px; }")
            label.setScaledContents(True)
            pixmap = QPixmap(token.get_map_asset())
            label.set_token_record(token)
            label.setPixmap(pixmap)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.all_labels.append(label)



    def __populate_token_bar(self):
        token_refs_list = self.toolbox.get_list_of_token_refs()
        self.open_btns = []
        count = 0
        for ref in token_refs_list:
            layout = QHBoxLayout()
            title = ref.get_title_str()
            label = QLabel(title)
            open_btn = QPushButton("\u2304")
            open_btn.setMaximumWidth(20)
            open_btn.clicked.connect(partial(self.__open_token_dropdown, ref, open_btn,count))
            self.open_btns.append(open_btn)
            layout.addWidget(label)
            layout.addWidget(open_btn)
            self.token_bar_layout.addLayout(layout)
            count += 1

    def __open_token_dropdown(self, ref, open_btn, count):
        tokens = ref.get_tokens_list()
        layout = QVBoxLayout()
        for token in tokens:
            hlayout = QHBoxLayout()
            name = token["name"]
            widget = QLabel(name)
            img = QPushButton()
            pixmap = QPixmap(token["set_map_asset"])
            btn_icon = QIcon(pixmap)
            img.setIcon(btn_icon)
            img.clicked.connect(partial(self.__add_token_to_window, token))
            hlayout.addWidget(widget)
            hlayout.addWidget(img)
            layout.addLayout(hlayout)
        #count += 1
        self.token_bar_layout.insertLayout(count+1, layout)
        open_btn.setText("^")
        open_btn.clicked.disconnect()
        open_btn.clicked.connect(partial(self.__close_token_dropdown, open_btn, layout, ref, count))

    def __close_token_dropdown(self, open_btn, layout, ref, count):
        while layout.count():
            item = layout.takeAt(0)
            child_layout = item.layout()
            while child_layout.count():
                child_item = child_layout.takeAt(0)
                widget = child_item.widget()
                if not widget is None:
                    widget.deleteLater()
            del item
        layout.deleteLater()
        open_btn.setText("\u2304")
        open_btn.clicked.disconnect()
        open_btn.clicked.connect(partial(self.__open_token_dropdown, ref, open_btn, count))


    # Needs changed
#    def __init__(self, logger_ref, token_dict:dict, token_type:TokenTypes, record_key:int, position=(0,0)):
    def __add_token_to_window(self, token):
        token_record = TokenRecord(self.logger_ref, token, TokenTypes.PLAYER_CHARACTERS, token["key"], position=(600,400))
        self.hexNode.getTileRecord().add_player_character(token_record)

        pixmap = QPixmap(token_record.get_map_asset())

        label = self.token_grid.itemAtPosition(0, 0).widget()
        label.setStyleSheet("QLabel { border: 1px solid blue; background-color: white; padding: 5px; }")
        label.setScaledContents(True)
        label.set_token_record(token_record)
        label.setPixmap(pixmap)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)



    """def start_dragging_child(self, label:TokenLabel):
        self.label_being_dragged = label

    def end_dragging_child(self, global_position):
        local_point = self.mapFromGlobal(global_position)
        self.label_being_dragged.move(local_point.x(), local_point.y())
        token_record = self.label_being_dragged.get_token_record()
        token_record.set_position((local_point.x(), local_point.y()))
        self.label_being_dragged = None"""
        