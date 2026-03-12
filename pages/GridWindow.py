from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QPixmap, QColor, QIcon
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


class PaintWidget(QWidget):
    def __init__(self, toolbox):
        super().__init__()
        self.toolbox = toolbox
        self.settings_ref = self.toolbox.get_settings_ref()
        self.rows = 0
        self.cols = 0
        self.total_boxes = 0
        self.__setup()

    def __setup(self):
        width = self.width()
        height = self.height()
        tile_size = self.settings_ref.getTileSize()
        for x in range(0, width, math.ceil(tile_size)):
            self.rows += 1
        for y in range(0, height, math.ceil(tile_size)):
            self.cols += 1

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)

        width = self.width()
        height = self.height()

        tile_size = self.settings_ref.getTileSize()

        self.rows = 0
        self.cols = 0

        for x in range(0, width, math.ceil(tile_size)):
            #painter.drawLine(x, 0, x, height)
            self.rows += 1
        for y in range(0, height, math.ceil(tile_size)):
            #painter.drawLine(0, y, width, y)
            self.cols += 1

        self.total_boxes = self.rows * self.cols

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_total_boxes(self):
        return self.total_boxes

class TokenLabel(QLabel):
    def __init__(self, toolbox, token_record:TokenRecord, parent=None):
        super().__init__(parent=parent)
        self.token_record = token_record
        self.toolbox = toolbox
        self.dragging = False


    def get_token_record(self) -> TokenRecord:
        return self.token_record

    def change_token_record(self, token_record:TokenRecord):
        self.token_record = token_record


    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            self.dragging = True
            self.parent().start_dragging_child(self)
        if(event.button() == Qt.MouseButton.RightButton):
            ref = self.__find_token_ref(self.token_record.get_token_type())
            self.scroll = QScrollArea()
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.scroll.setWidgetResizable(True)
            widget = TokenRecordContainerWidget(self.token_record, self.toolbox, ref)
            self.scroll.setWidget(widget)
            self.scroll.show()

        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if(self.dragging):
            self.dragging = False
            global_position = self.mapToGlobal(event.position().toPoint())
            print(global_position)
            self.parent().end_dragging_child(global_position)
        return super().mouseReleaseEvent(event)

    def __find_token_ref(self, token_type):
        match(token_type):
            case TokenTypes.PLAYER_CHARACTERS:
                return self.toolbox.get_player_characters_ref()
            case TokenTypes.NON_PLAYER_CHARACTERS:
                return self.toolbox.get_nonplayer_characters_ref()
            case TokenTypes.ANIMALS:
                return self.toolbox.get_animals_ref()
            case TokenTypes.MONSTERS:
                return self.toolbox.get_monsters_ref()
            case TokenTypes.BUILDINGS:
                return self.toolbox.get_buildings_ref()
            case TokenTypes.STRUCTURES:
                return self.toolbox.get_structures_ref()
            case TokenTypes.NATURE:
                return self.toolbox.get_nature_ref()

class GridWindow(QMainWindow):
    def __init__(self, hexNode:HextileNode, toolbox:Toolbox):
        super().__init__()
        self.hexNode = hexNode
        self.record = self.hexNode.getTileRecord()
        self.toolbox = toolbox
        self.settings_ref = self.toolbox.get_settings_ref()
        self.seed_ref = self.settings_ref.getSeedRef()
        self.all_labels = []
        self.label_being_dragged = None
        self.setStyleSheet("background-color:white;");


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


        self.main_widget = PaintWidget(self.toolbox)
        self.token_grid = QGridLayout()
        self.main_widget.setLayout(self.token_grid)

        self.__position_tokens()
        self.__add_tokens_to_layout()
        self.setCentralWidget(self.main_widget)

    '''def resizeEvent(self, event):
        super().resizeEvent(event)
        self.__add_tokens_to_layout()'''


    def __position_tokens(self):
        rows = self.main_widget.get_rows()
        cols = self.main_widget.get_cols()

        all_tokens = self.record.get_all_tokens()
        for token in all_tokens:
            x = self.seed_ref.getOtherRandInt(0, cols)
            y = self.seed_ref.getOtherRandInt(0, rows)

            while(not self.record.check_position((x, y))):
                x = self.seed_ref.getOtherRandInt(0, cols)
                y = self.seed_ref.getOtherRandInt(0, rows)

            token.set_position((x,y))

    def __add_tokens_to_layout(self):
        rows = self.main_widget.get_rows()
        cols = self.main_widget.get_cols()

        width = self.width()
        height = self.height()

        all_tokens = self.record.get_all_tokens()



        # 200 px x 200 px
        # 16 total boxes
        # 4 boxes in each row, 4 rows (sqrt)
        # width of each box is 200 / 4
        # height of each box is 200 / 4

        for i in range(0, cols+1):
            for j in range(0, rows+1):
                self.token_grid.addWidget(TokenLabel(self.toolbox, None, parent=self), i, j)

        for token in all_tokens:
            x_pos = token.get_x_position()
            y_pos = token.get_y_position()
            label = TokenLabel(self.toolbox, token, parent=self)
            label.setScaledContents(True)
            label.resize(math.ceil(width/cols), math.ceil(height/rows))
            pixmap = QPixmap(token.get_map_asset())
            label.setPixmap(pixmap)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            old_widget = self.token_grid.itemAtPosition(x_pos, y_pos)
            if old_widget:
                widget = old_widget.widget()
                if widget:
                    self.token_grid.removeWidget(widget)
                    widget.deleteLater()
            self.token_grid.addWidget(label, x_pos, y_pos)
            self.all_labels.append(label)

    '''def __position_tokens(self):
        all_tokens = self.record.get_all_tokens()
        start_width = math.ceil(self.width()/2)
        end_width = math.ceil(self.width())
        start_height = 0
        end_height = math.ceil(self.height())
        for token in all_tokens:
            x = self.seed_ref.getOtherRandInt(start_width, end_width)
            y = self.seed_ref.getOtherRandInt(start_height, end_height)

            while(not self.record.check_position((x, y))):
                x = self.seed_ref.getOtherRandInt(start_width, end_width)
                y = self.seed_ref.getOtherRandInt(start_height, end_height)
            token.set_position((x, y))'''



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


    '''def __paint_tokens_on_window(self):
        all_tokens = self.record.get_all_tokens()
        tile_size = math.ceil(self.settings_ref.getTileSize())
        for token in all_tokens:
            height_mult = token.get_base_height_multiplier()
            width_mult = token.get_base_width_multiplier()
            x_pos = token.get_x_position()
            y_pos = token.get_y_position()
            label = TokenLabel(self.toolbox, token, parent=self)
            label.resize((tile_size*width_mult), (tile_size*height_mult))
            label.setScaledContents(True)
            pixmap = QPixmap(token.get_map_asset())
            label.setPixmap(pixmap)
            label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            label.move(x_pos, y_pos)
            self.all_labels.append(label)'''

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
        count += 1
        self.token_bar_layout.insertLayout(count, layout)
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
            count -= 1
            del item
        open_btn.setText("\u2304")
        open_btn.clicked.disconnect()
        open_btn.clicked.connect(partial(self.__open_token_dropdown, ref, open_btn, count))


    def __add_token_to_window(self, token):
        token_record = TokenRecord(token, TokenTypes.PLAYER_CHARACTERS, token["key"], position=(600,400))
        self.hexNode.getTileRecord().add_player_character(token)
        tile_size = math.ceil(self.settings_ref.getTileSize())


        height_mult = token_record.get_base_height_multiplier()
        width_mult = token_record.get_base_width_multiplier()
        label = TokenLabel(self.toolbox, token_record, parent=self)
        label.resize((tile_size), (tile_size))
        label.setScaledContents(True)
        pixmap = QPixmap(token_record.get_map_asset())
        label.setPixmap(pixmap)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        label.move(600, 400)
        label.show()
        self.all_labels.append(label)


    def start_dragging_child(self, label:TokenLabel):
        self.label_being_dragged = label

    def end_dragging_child(self, global_position):
        local_point = self.mapFromGlobal(global_position)
        self.label_being_dragged.move(local_point.x(), local_point.y())
        token_record = self.label_being_dragged.get_token_record()
        token_record.set_position((local_point.x(), local_point.y()))
        self.label_being_dragged = None
        