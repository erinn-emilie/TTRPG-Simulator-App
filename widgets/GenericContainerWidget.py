from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QFileDialog,
    QMessageBox,
    QMainWindow,
    QCheckBox,
    QSizePolicy
    )

from toolbox.Database import Database
from toolbox.Database import DatabaseMessages

from PyQt6.QtGui import QPixmap


from functools import partial
from toolbox.Toolbox import Toolbox
import os

from PIL import Image  
import io  

class TileProbWindow(QMainWindow):
    def __init__(self, toolbox:Toolbox, tile_name:str):
        super().__init__()
        self.tile_name = tile_name
        self.toolbox = toolbox
        self.tile_types_ref = self.toolbox.get_tile_types_ref()
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.setWindowTitle(f"{tile_name} Probabilities")
        self.setStyleSheet("background-color: #F0F2A6")


        self.name_labels = []
        self.weight_labels = []
        self.new_tile_weights_dict = {}
        self.old_tile_weights_dict = {}

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setStyleSheet("background-color: #AA6373; color: #F0F2A6;")
        self.save_btn.clicked.connect(self.__save_changes)

        self.main_layout.addWidget(self.save_btn)

        self.__setup_layout()

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def __setup_layout(self):
        weights = self.tile_types_ref.get_tile_weights_by_name(self.tile_name)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.main_layout.addWidget(spacer)
        for tile in weights:
            if(tile.upper() == self.tile_name.upper()):
                continue
            row = QHBoxLayout()
            self.new_tile_weights_dict[tile] = ""
            name_label = QLabel(tile,  alignment=Qt.AlignmentFlag.AlignCenter)
            name_label.setMinimumWidth(75)
            name_label.setStyleSheet("background-color: #AA6373; color: #F0F2A6; border-radius: 15px")

            self.name_labels.append(name_label)
            weight = weights[tile]
            self.old_tile_weights_dict[tile] = weight
            weight_label = QLineEdit(str(weight))
            weight_label.setStyleSheet("color: #1A1B25;")
            weight_label.setMaximumWidth(100)
            weight_label.textEdited.connect(partial(self.__change_tile_weight, name_key=tile, label=weight_label))
            self.weight_labels.append(weight_label)

            row.addWidget(spacer)
            row.addWidget(name_label)
            row.addWidget(weight_label)
            row.addWidget(spacer)
            self.main_layout.addLayout(row)
        self.main_layout.addWidget(spacer)

    def __change_tile_weight(self, new_weight, name_key="", label=None):
        if(new_weight != ""):
            try: 
                weight = int(new_weight)
                self.new_tile_weights_dict[name_key] = weight
            except ValueError:
                old_weight = self.old_tile_weights_dict[name_key]
                label.setText(str(old_weight))


        self.new_tile_weights_dict[name_key] = new_weight

    def __save_changes(self):
        for tile in self.new_tile_weights_dict:
            if(self.new_tile_weights_dict[tile] != ""):
                try:
                    weight = self.new_tile_weights_dict[tile]
                    weight = int(weight)
                    self.tile_types_ref.change_tile_weight(self.tile_name, tile, weight)
                    self.new_tile_weights_dict[tile] = ""
                except ValueError:
                    self.new_tile_weights_dict[tile] = ""
                    continue
        self.close()



 
class TokenContainerWidget(QWidget):
    def __init__(self, token:dict, toolbox:Toolbox, token_ref, overhead_window):
        super().__init__()
        self.toolbox = toolbox
        self.account_ref = self.toolbox.get_account_ref()
        self.overhead_window = overhead_window
        self.token = token
        self.token_ref = token_ref

        self.internal_stylesheet = "background-color: #F0F2A6;"
        

        self.token_small_fields = self.token["small_fields"]
        self.token_large_fields = self.token["large_fields"]
        self.token_name = self.token["name"]
        self.token_key = self.token["key"]
        self.map_asset = self.token["set_map_asset"]

        self.all_labels = []

        #key, new value
        self.small_value_changes = {}
        #old key, new key
        self.small_key_changes = {}

        self.lg_value_changes = {}
        self.lg_key_changes = {}




        self.main_layout = QVBoxLayout()

        self.small_fields_layout = QVBoxLayout()
        self.large_fields_layout = QVBoxLayout()

        name_row = QHBoxLayout()
        name_label = QLineEdit(self.token_name)
        name_label.setReadOnly(True)
        name_label.setMaximumWidth(200)
        self.small_value_changes["name"] = ""
        name_label.textEdited.connect(partial(self.__edit_value_text, key="name"))
        self.all_labels.append(name_label)



        self.map_asset_label = QLabel()
        self.map_asset_pix = QPixmap()
        if(self.map_asset != ""):
            self.map_asset_pix.loadFromData(self.map_asset)
        self.map_asset_pix = self.map_asset_pix.scaledToWidth(100)
        self.map_asset_pix = self.map_asset_pix.scaledToHeight(100)
        self.map_asset_label.setPixmap(self.map_asset_pix)
        change_map_asset_btn = QPushButton("Change Map Asset")
        change_map_asset_btn.setMaximumWidth(200)
        change_map_asset_btn.clicked.connect(partial(self.__change_map_asset))


        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        name_row.addWidget(spacer)
        name_row.addWidget(self.map_asset_label)
        name_label.setStyleSheet(self.internal_stylesheet)
        name_row.addWidget(name_label)
    
        change_map_asset_btn.setStyleSheet(self.internal_stylesheet)
        name_row.addWidget(change_map_asset_btn)
        name_row.addWidget(spacer)


        location = token["save_location"]
        if(self.account_ref.get_logged_in()):
            database_checkbox = QCheckBox(text="Saved to account.")
            if("database" in location):
                database_checkbox.setChecked(True)
            database_checkbox.toggled.connect(partial(self.__change_save_location, checkbox=database_checkbox))
            name_row.addWidget(database_checkbox)



        self.main_layout.addLayout(name_row)


        self.total_images = 0
        self.images = self.token["large_assets"]
        self.image_labels = []
        self.del_img_btns = []
        upload_row = QHBoxLayout()
        upload_row.addWidget(spacer)

        self.img_backward_btn = QPushButton("<")
        self.img_backward_btn.setStyleSheet(self.internal_stylesheet)
        self.img_backward_btn.clicked.connect(self.__cycle_last_img)

        upload_row.addWidget(self.img_backward_btn)

        lg_img_row = QHBoxLayout()
        for image in self.images:
            img_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            img_label.setPixmap(pixmap)
            img_label.setMaximumHeight(500)
            img_label.setMaximumWidth(500)
            self.image_labels.append(img_label)
            del_btn = QPushButton("Remove Image")
            del_btn.setStyleSheet(self.internal_stylesheet)
            upload_row.addWidget(del_btn)
            self.del_img_btns.append(del_btn)
            del_btn.clicked.connect(partial(self.__delete_image, image, img_label))
            lg_img_row.addWidget(spacer)
            lg_img_row.addWidget(img_label)
            lg_img_row.addWidget(spacer)
            self.main_layout.addLayout(lg_img_row)



            self.total_images += 1

            

        for idx, label in enumerate(self.image_labels):
            if(idx != 0):
                label.hide()
                self.del_img_btns[idx].hide()


        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.__upload_image)
        self.upload_btn.setStyleSheet(self.internal_stylesheet)
        upload_row.addWidget(self.upload_btn)

        self.img_forward_btn = QPushButton(">")
        self.img_forward_btn.setStyleSheet(self.internal_stylesheet)
        self.img_forward_btn.clicked.connect(self.__cycle_next_img)
        upload_row.addWidget(self.img_forward_btn)

        upload_row.addWidget(spacer)

        

        self.main_layout.addLayout(upload_row)

        self.del_btns = []
        self.to_del_keys = []
        self.just_added = []
        self.hidden_fields = []

        self.total_sm_fields = 0
        self.total_lg_fields = 0


        for sm_field in self.token_small_fields:
            new_row = QHBoxLayout()
            field_name = QLineEdit(sm_field)
            field_name.setReadOnly(True)
            self.small_key_changes[sm_field] = ""
            field_name.textEdited.connect(partial(self.__edit_key_text, old_key=sm_field))

            value = str(self.token_small_fields[sm_field])
            field_value = QLineEdit(value)
            field_value.setReadOnly(True)
            self.small_value_changes[sm_field] = ""
            field_value.textEdited.connect(partial(self.__edit_value_text, key=sm_field))

            self.all_labels.append(field_name)
            self.all_labels.append(field_value)

            del_btn = QPushButton("X")
            del_btn.clicked.connect(partial(self.__queue_for_deletion, field_name, field_value, sm_field, del_btn))
            del_btn.hide()
            self.del_btns.append(del_btn)
   
            new_row.addWidget(spacer)
            field_name.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(field_name)
            field_value.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(field_value)
            del_btn.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(del_btn)   
            new_row.addWidget(spacer)
            self.small_fields_layout.addLayout(new_row)
            self.total_sm_fields += 1


        self.small_fields_layout.addLayout(new_row)

        add_sm_btn_row = QHBoxLayout()
        self.add_sm_btn = QPushButton("Add Small Field")
        self.add_sm_btn.setStyleSheet(self.internal_stylesheet)
        self.add_sm_btn.clicked.connect(self.__add_sm_field)
        self.add_sm_btn.hide()
        add_sm_btn_row .addWidget(self.add_sm_btn)
        self.small_fields_layout.addLayout(add_sm_btn_row)

        for lg_field in self.token_large_fields:
            new_col = QVBoxLayout()
            label_row = QHBoxLayout()
            label = QLineEdit(lg_field)
            label.setStyleSheet(self.internal_stylesheet)
            self.all_labels.append(label)
            label.setReadOnly(True)
            label_row.addWidget(label)
            new_col.addLayout(label_row)

            self.lg_key_changes[lg_field] = ""
            label.textEdited.connect(partial(self.__edit_key_text_lg, old_key=lg_field))

            text_row = QHBoxLayout()
            new_line = QPlainTextEdit(self.token_large_fields[lg_field])
            self.all_labels.append(new_line)
            new_line.setReadOnly(True)

            self.lg_value_changes[lg_field] = ""
            new_line.textChanged.connect(partial(self.__edit_value_text_lg, new_line, key=lg_field))

            del_btn = QPushButton("X")
            del_btn.clicked.connect(partial(self.__queue_for_deletion, label, new_line, lg_field, del_btn))
            del_btn.hide()
            self.del_btns.append(del_btn)

            new_line.setStyleSheet(self.internal_stylesheet)
            del_btn.setStyleSheet(self.internal_stylesheet)
            text_row.addWidget(new_line)
            text_row.addWidget(del_btn)
            new_col.addLayout(text_row)
            self.large_fields_layout.addLayout(new_col)
            self.total_lg_fields += 1


        add_lg_btn_row = QHBoxLayout()
        self.add_lg_btn = QPushButton("Add Large Field")
        self.add_lg_btn.setStyleSheet(self.internal_stylesheet)
        self.add_lg_btn.clicked.connect(self.__add_lg_field)
        self.add_lg_btn.hide()
        add_lg_btn_row .addWidget(self.add_lg_btn)
        self.large_fields_layout.addLayout(add_lg_btn_row)


        self.btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet(self.internal_stylesheet)
        self.edit_btn.clicked.connect(self.__edit_fields)
        self.btn_row.addWidget(self.edit_btn)

        self.del_token_btn = QPushButton("Delete")
        self.del_token_btn.setStyleSheet(self.internal_stylesheet)
        self.del_token_btn.clicked.connect(self.__delete_token)
        self.btn_row.addWidget(self.del_token_btn)
        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.internal_stylesheet)
        self.save_btn.clicked.connect(self.__save_fields)
        self.save_btn.hide()
        self.btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.internal_stylesheet)
        self.cancel_btn.clicked.connect(self.__cancel)
        self.cancel_btn.hide()
        self.btn_row.addWidget(self.cancel_btn)

        self.main_layout.addLayout(self.small_fields_layout)
        self.main_layout.addLayout(self.large_fields_layout)
        self.main_layout.addLayout(self.btn_row)
        self.setLayout(self.main_layout)


    def __upload_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select an image!")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            try:
                selected_files_list = file_dialog.selectedFiles()
                img_path = selected_files_list[0]
                data = b""
                with Image.open(img_path) as img:  
                    buffer = io.BytesIO()  
                    img.save(buffer, format='PNG')      
                    data = buffer.getvalue()

                self.token_ref.add_new_large_image(self.token_key, data)
                self.total_images += 1
                img_label = QLabel()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                img_label.setPixmap(pixmap)
                self.image_labels.append(img_label)
                del_btn = QPushButton("Remove Image")
                self.del_img_btns.append(del_btn)
                del_btn.clicked.connect(partial(self.__delete_image, data, img_label))
                self.main_layout.insertWidget(self.total_images, img_label)
                self.main_layout.insertWidget(self.total_images + 1, del_btn)
                for label in self.image_labels:
                    label.hide()
                img_label.show()
            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")


    def __change_map_asset(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select an image!")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            try:
                selected_files_list = file_dialog.selectedFiles()
                img_path = selected_files_list[0]
                data = b""
                with Image.open(img_path) as img:  
                    buffer = io.BytesIO()  
                    img.save(buffer, format='PNG')      
                    data = buffer.getvalue()
                self.token_ref.change_map_asset(self.token_key, data)
                self.map_asset = data
                self.map_asset_pix = QPixmap()
                if(self.map_asset != ""):
                    self.map_asset_pix.loadFromData(self.map_asset)
                self.map_asset_pix = self.map_asset_pix.scaledToWidth(100)
                self.map_asset_pix = self.map_asset_pix.scaledToHeight(100)
                self.map_asset_label.setPixmap(self.map_asset_pix)
            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")



    def __add_sm_field(self):
        sm_field = "New Field "
        new_row = QHBoxLayout()
        field_name = QLineEdit(sm_field)
        field_name.setReadOnly(False)
        self.small_key_changes[sm_field] = ""
        field_name.textEdited.connect(partial(self.__edit_key_text, old_key=sm_field))

        value = "New Value"
        field_value = QLineEdit(value)
        field_value.setReadOnly(False)
        self.small_value_changes[sm_field] = ""
        field_value.textEdited.connect(partial(self.__edit_value_text, key=sm_field))

        self.all_labels.append(field_name)
        self.all_labels.append(field_value)

        del_btn = QPushButton("X")
        del_btn.clicked.connect(partial(self.__queue_for_deletion, field_name, field_value, sm_field, del_btn))
        del_btn.show()
        self.del_btns.append(del_btn)
            
        new_row.addWidget(field_name)
        new_row.addWidget(field_value)
        new_row.addWidget(del_btn)
        self.small_fields_layout.insertLayout(self.total_sm_fields, new_row)
        self.total_sm_fields += 1


        self.token_ref.add_new_sm_field(self.token_key, sm_field, value)
        self.just_added.append(sm_field)


    def __add_lg_field(self):
        new_col = QVBoxLayout()
        label_row = QHBoxLayout()
        lg_field = "New Notes"
        label = QLineEdit(lg_field)
        self.all_labels.append(label)
        label.setReadOnly(False)
        label_row.addWidget(label)
        new_col.addLayout(label_row)

        self.lg_key_changes[lg_field] = ""
        label.textEdited.connect(partial(self.__edit_key_text_lg, old_key=lg_field))

        value = ""
        text_row = QHBoxLayout()
        new_line = QPlainTextEdit("")
        self.all_labels.append(new_line)
        new_line.setReadOnly(False)

        self.lg_value_changes[lg_field] = ""
        new_line.textChanged.connect(partial(self.__edit_value_text_lg, new_line, key=lg_field))

        del_btn = QPushButton("X")
        del_btn.clicked.connect(partial(self.__queue_for_deletion, label, new_line, lg_field, del_btn))
        del_btn.hide()
        self.del_btns.append(del_btn)

        text_row.addWidget(new_line)
        text_row.addWidget(del_btn)
        new_col.addLayout(text_row)
        self.large_fields_layout.insertLayout(self.total_lg_fields, new_col)
        self.total_lg_fields += 1

        self.token_ref.add_new_lg_field(self.token_key, lg_field, value)
        self.just_added.append(lg_field)
        


    def __queue_for_deletion(self, key_field, value_field, key, del_btn):
        key_field.hide()
        value_field.hide()
        del_btn.hide()
        self.to_del_keys.append(key)
        self.hidden_fields.append(key_field)
        self.hidden_fields.append(value_field)
        self.hidden_fields.append(del_btn)



    def __edit_value_text(self, new_value, key=""):
        self.small_value_changes[key] = new_value

    def __edit_value_text_lg(self, text_edit_box, key=""):
        self.lg_value_changes[key] = text_edit_box.document()


    def __edit_key_text(self, new_key, old_key=""):
        self.small_key_changes[old_key] = new_key

    def __edit_key_text_lg(self, new_key, old_key=""):
        self.lg_key_changes[old_key] = new_key

    def __edit_fields(self):
        for label in self.all_labels:
            label.setReadOnly(False)
        self.edit_btn.hide()
        self.save_btn.show()
        self.cancel_btn.show()
        self.add_sm_btn.show()
        self.add_lg_btn.show()
        for btn in self.del_btns:
            btn.show()

    def __save_fields(self):
        for key in self.small_value_changes:
            if(self.small_value_changes[key] != ""):
                self.token_ref.change_small_field_values(self.token_key, key, self.small_value_changes[key])
        for old_key in self.small_key_changes:
            if(self.small_key_changes[old_key] != ""):
                self.token_ref.change_small_field_keys(self.token_key, old_key, self.small_key_changes[old_key])
        for key in self.lg_value_changes:
            if(self.lg_value_changes[key] != ""):
                self.token_ref.change_lg_field_values(self.token_key, key, self.lg_value_changes[key])
        for old_key in self.lg_key_changes:
            if(self.lg_key_changes[old_key] != ""):
                self.token_ref.change_lg_field_keys(self.token_key, old_key, self.lg_key_changes[old_key])
        for label in self.all_labels:
            label.setReadOnly(True)
        for key in self.to_del_keys:
            self.token_ref.delete_field(self.token_key, key)
        self.hidden_fields.clear()
        self.to_del_keys.clear()
        self.just_added.clear()
        self.__cancel()

    def __cancel(self):
        self.edit_btn.show()
        self.save_btn.hide()
        self.cancel_btn.hide()
        self.add_sm_btn.hide()
        self.add_lg_btn.hide()
        self.__clear_changes()

    def __clear_changes(self):
        for item in self.small_value_changes:
            self.small_value_changes[item] = ""
        for item in self.small_key_changes:
            self.small_key_changes[item] = ""
        for item in self.lg_value_changes:
            self.lg_value_changes[item] = ""
        for item in self.lg_key_changes:
            self.lg_key_changes[item] = ""
        for item in self.hidden_fields:
            item.show()
        for item in self.just_added:
            self.token_ref.delete_field(self.token_key, item)
        for btn in self.del_btns:
            btn.hide()


    def __cycle_next_img(self):
        show_next_img = False
        for idx, label in enumerate(self.image_labels):
            if(show_next_img):
                label.show()
                self.del_img_btns[idx].show()
                show_next_img = False
                break
            if(label.isVisible()):
                show_next_img = True
                label.hide()
                self.del_img_btns[idx].hide()
        if(show_next_img):
            self.image_labels[0].show()
            self.del_img_btns[0].show()
            self.image_labels[len(self.image_labels)-1].hide()
            self.del_img_btns[len(self.image_labels)-1].hide()

    def __cycle_last_img(self):
        show_next_img = False
        counter = len(self.image_labels) - 1
        for label in reversed(self.image_labels):
            if(show_next_img):
                label.show()
                self.del_img_btns[counter].show()
                show_next_img = False
                break
            if(label.isVisible()):
                show_next_img = True
                label.hide()
                self.del_img_btns[counter].hide()
            counter -= 1
        if(show_next_img):
            self.image_labels[len(self.image_labels) - 1].show()
            self.image_labels[0].hide()
            self.del_img_btns[len(self.image_labels) - 1].show()
            self.del_img_btns[0].hide()


    def __delete_image(self, data, image_label):
        self.token_ref.remove_large_image(self.token_key, img_path)
        image_label.setParent(None)


    def __delete_token(self):
        answer = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to delete this token?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes:
            self.token_ref.delete_token(self.token_key)
            self.overhead_window.delete_token_widget(self)
        else:
            print("User clicked No (or closed the dialog)")


    def __change_save_location(self, status, checkbox=None):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Save Token")
        if(status):
            if(self.account_ref.get_logged_in()):
                self.token["save_location"] = "database"
                message = self.token_ref.change_token_save_location(self.token, local=False)
                if(message == DatabaseMessages.SUCCESS):
                    dlg.setText("Token saved to your account!")
                    dlg.exec()
                else:
                    dlg.setText("Something went wrong! Please try again!")
                    dlg.exec()
                    checkbox.setChecked(False)
            else:
                dlg.setText("Please log in or sign up to save a token to your account!")
                dlg.exec()
                checkbox.setChecked(False)
        else:
            message = self.token_ref.change_token_save_location(self.token, local=True)
            self.token["save_location"] = "local"



class TileContainerWidget(QWidget):
    def __init__(self, tile_name:str, toolbox:Toolbox, tile_img_path:str):
        super().__init__()
        self.toolbox = toolbox
        self.tile_types_ref = self.toolbox.get_tile_types_ref()
        self.old_tile_name = tile_name
        self.new_tile_name = ""
        self.tile_img_path = tile_img_path
        self.tile_probs_window = None
        self.btn_stylesheet = """background-color: #392061; color: #F0F2A6;"""

        self.main_layout = QHBoxLayout()

        self.tile_name_label = QLineEdit(self.old_tile_name)
        self.tile_name_label.setStyleSheet("color: #1A1B25;")
        self.tile_name_label.textEdited.connect(self.__change_tile_name)
        self.tile_name_label.setReadOnly(True)
        self.tile_name_label.setMaximumWidth(100)

        self.edit_name_btn = QPushButton("Edit Name")
        self.edit_name_btn.setStyleSheet(self.btn_stylesheet)
        self.edit_name_btn.clicked.connect(self.__set_tile_name_editable)
        self.save_name_btn = QPushButton("Save Edit")
        self.save_name_btn.setStyleSheet(self.btn_stylesheet)
        self.save_name_btn.clicked.connect(self.__save_tile_name)
        self.cancel_name_btn = QPushButton("Cancel Edit")
        self.cancel_name_btn.clicked.connect(self.__set_tile_name_uneditable)
        self.cancel_name_btn.setStyleSheet(self.btn_stylesheet)

        self.tile_img_pixmap = QPixmap()
        if(isinstance(self.tile_img_path, bytes)):
            self.tile_img_pixmap.loadFromData(self.tile_img_path)
        else:
            self.tile_img_pixmap = QPixmap(self.tile_img_path)
        self.tile_img_label = QLabel()
        self.tile_img_label.setPixmap(self.tile_img_pixmap)
        self.tile_img_label.setScaledContents(True)
        self.tile_img_label.setMaximumHeight(200)
        self.tile_img_label.setMaximumWidth(200)

        self.change_tile_img_btn = QPushButton("Change Tile Image")
        self.change_tile_img_btn.setStyleSheet("background-color: #392061; color: #F0F2A6; padding: 5px;")
        self.change_tile_img_btn.clicked.connect(self.__change_tile_img)

        self.main_layout.addStretch()

        self.edit_btn_layout = QHBoxLayout()
        self.edit_btn_layout.addWidget(self.edit_name_btn)
        self.edit_btn_layout.addWidget(self.save_name_btn)
        self.edit_btn_layout.addWidget(self.cancel_name_btn)
        self.save_name_btn.hide()
        self.cancel_name_btn.hide()

        self.edit_btn_v_layout = QVBoxLayout()
        self.edit_btn_v_layout.addStretch()
        self.edit_btn_v_layout.addLayout(self.edit_btn_layout)

        self.edit_tile_probs_btn = QPushButton("Edit Tile Probabilities")
        self.edit_tile_probs_btn.setStyleSheet(self.btn_stylesheet)
        self.edit_tile_probs_btn.clicked.connect(self.__edit_tile_probs)
        self.edit_btn_v_layout.addWidget(self.edit_tile_probs_btn)
        self.edit_btn_v_layout.addStretch()

        
        self.edit_btn_container_widget = QWidget()
        self.edit_btn_container_widget.setLayout(self.edit_btn_v_layout)

        self.main_layout.addWidget(self.edit_btn_container_widget)

        self.main_layout.addLayout(self.edit_btn_v_layout)

        self.main_layout.addSpacing(50)

        self.main_layout.addWidget(self.tile_name_label)
        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(self.tile_img_label)
        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(self.change_tile_img_btn)

        self.main_layout.addStretch()
        
        self.setLayout(self.main_layout)

    def __set_tile_name_editable(self):
        self.tile_name_label.setReadOnly(False)
        self.edit_name_btn.hide()
        self.save_name_btn.show()
        self.cancel_name_btn.show()

    def __set_tile_name_uneditable(self):
        self.tile_name_label.setReadOnly(True)
        self.edit_name_btn.show()
        self.save_name_btn.hide()
        self.cancel_name_btn.hide()

    def __change_tile_name(self, text):
        self.new_tile_name = text

    def __save_tile_name(self):
        if(self.new_tile_name != ""):
            self.tile_types_ref.change_tile_name(self.old_tile_name, self.new_tile_name)
            self.old_tile_name = self.new_tile_name
            self.new_tile_name = ""
        self.__set_tile_name_uneditable()

    def __change_tile_img(self):
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
                asset_path = f"assets/{img_name}"
                os.rename(img_path, asset_path)

                self.tile_img_path = asset_path
                self.tile_types_ref.change_tile_image(self.old_tile_name, asset_path)

                self.tile_img_pixmap = QPixmap(self.tile_img_path)
                self.tile_img_label = QLabel()
                self.tile_img_label.setPixmap(self.tile_img_pixmap)

            except FileNotFoundError:
                print("File couldn't be found")
            except FileExistsError:
                print("That file already exists in this location")

    def __edit_tile_probs(self):
        self.tile_probs_window = TileProbWindow(self.toolbox, self.old_tile_name)
        self.tile_probs_window.show()




        

class TokenRecordContainerWidget(QWidget):
    def __init__(self, token_record, toolbox:Toolbox, token_label=None):
        super().__init__()
        self.toolbox = toolbox
        self.account_ref = self.toolbox.get_account_ref()
        self.token_record = token_record
        self.token_label = token_label

        self.internal_stylesheet = "background-color: #F0F2A6;"
        

        self.token_small_fields = self.token_record.get_small_fields()
        self.token_large_fields = self.token_record.get_large_fields()
        self.token_name = self.token_record.get_token_name()
        self.token_key = self.token_record.get_token_key()
        self.map_asset = self.token_record.get_map_asset()



        self.all_labels = []

        #key, new value
        self.small_value_changes = {}
        #old key, new key
        self.small_key_changes = {}

        self.lg_value_changes = {}
        self.lg_key_changes = {}




        self.main_layout = QVBoxLayout()

        self.small_fields_layout = QVBoxLayout()
        self.large_fields_layout = QVBoxLayout()

        name_row = QHBoxLayout()
        name_label = QLineEdit(self.token_name)
        name_label.setReadOnly(True)
        name_label.setMaximumWidth(200)
        self.small_value_changes["name"] = ""
        name_label.textEdited.connect(partial(self.__edit_value_text, key="name"))
        self.all_labels.append(name_label)



        map_asset_label = QLabel()
        map_asset_pix = QPixmap()
        if(self.map_asset != ""):
            map_asset_pix.loadFromData(self.map_asset)
        map_asset_pix = map_asset_pix.scaledToWidth(100)
        map_asset_pix = map_asset_pix.scaledToHeight(100)
        map_asset_label.setPixmap(map_asset_pix)



        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        name_row.addWidget(spacer)
        name_row.addWidget(map_asset_label)
        name_label.setStyleSheet(self.internal_stylesheet)
        name_row.addWidget(name_label)

        del_token_btn = QPushButton("Delete From Map")
        del_token_btn.setStyleSheet(self.internal_stylesheet)
        del_token_btn.clicked.connect(self.__del_from_map)
        name_row.addWidget(del_token_btn)

        name_row.addWidget(spacer)




        self.main_layout.addLayout(name_row)


        self.total_images = 0
        self.images = self.token_record.get_large_assets()
        self.image_labels = []
        self.del_img_btns = []
        upload_row = QHBoxLayout()
        upload_row.addWidget(spacer)

        self.img_backward_btn = QPushButton("<")
        self.img_backward_btn.setStyleSheet(self.internal_stylesheet)
        self.img_backward_btn.clicked.connect(self.__cycle_last_img)

        upload_row.addWidget(self.img_backward_btn)

        lg_img_row = QHBoxLayout()
        for image in self.images:
            img_label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            img_label.setPixmap(pixmap)
            img_label.setMaximumHeight(500)
            img_label.setMaximumWidth(500)
            self.image_labels.append(img_label)

            lg_img_row.addWidget(spacer)
            lg_img_row.addWidget(img_label)
            lg_img_row.addWidget(spacer)
            self.main_layout.addLayout(lg_img_row)



            self.total_images += 1

            

        for idx, label in enumerate(self.image_labels):
            if(idx != 0):
                label.hide()
                self.del_img_btns[idx].hide()


        self.img_forward_btn = QPushButton(">")
        self.img_forward_btn.setStyleSheet(self.internal_stylesheet)
        self.img_forward_btn.clicked.connect(self.__cycle_next_img)
        upload_row.addWidget(self.img_forward_btn)

        upload_row.addWidget(spacer)

        

        self.main_layout.addLayout(upload_row)

        self.del_btns = []
        self.to_del_keys = []
        self.just_added = []
        self.hidden_fields = []

        self.total_sm_fields = 0
        self.total_lg_fields = 0


        for sm_field in self.token_small_fields:
            new_row = QHBoxLayout()
            field_name = QLineEdit(sm_field)
            field_name.setReadOnly(True)
            self.small_key_changes[sm_field] = ""
            field_name.textEdited.connect(partial(self.__edit_key_text, old_key=sm_field))

            value = str(self.token_small_fields[sm_field])
            field_value = QLineEdit(value)
            field_value.setReadOnly(True)
            self.small_value_changes[sm_field] = ""
            field_value.textEdited.connect(partial(self.__edit_value_text, key=sm_field))

            self.all_labels.append(field_name)
            self.all_labels.append(field_value)

            del_btn = QPushButton("X")
            del_btn.clicked.connect(partial(self.__queue_for_deletion, field_name, field_value, sm_field, del_btn))
            del_btn.hide()
            self.del_btns.append(del_btn)
   
            new_row.addWidget(spacer)
            field_name.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(field_name)
            field_value.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(field_value)
            del_btn.setStyleSheet(self.internal_stylesheet)
            new_row.addWidget(del_btn)   
            new_row.addWidget(spacer)
            self.small_fields_layout.addLayout(new_row)
            self.total_sm_fields += 1


        self.small_fields_layout.addLayout(new_row)



        for lg_field in self.token_large_fields:
            new_col = QVBoxLayout()
            label_row = QHBoxLayout()
            label = QLineEdit(lg_field)
            label.setStyleSheet(self.internal_stylesheet)
            self.all_labels.append(label)
            label.setReadOnly(True)
            label_row.addWidget(label)
            new_col.addLayout(label_row)

            self.lg_key_changes[lg_field] = ""
            label.textEdited.connect(partial(self.__edit_key_text_lg, old_key=lg_field))

            text_row = QHBoxLayout()
            new_line = QPlainTextEdit(self.token_large_fields[lg_field])
            self.all_labels.append(new_line)
            new_line.setReadOnly(True)

            self.lg_value_changes[lg_field] = ""
            new_line.textChanged.connect(partial(self.__edit_value_text_lg, new_line, key=lg_field))

            del_btn = QPushButton("X")
            del_btn.clicked.connect(partial(self.__queue_for_deletion, label, new_line, lg_field, del_btn))
            del_btn.hide()
            self.del_btns.append(del_btn)

            new_line.setStyleSheet(self.internal_stylesheet)
            del_btn.setStyleSheet(self.internal_stylesheet)
            text_row.addWidget(new_line)
            text_row.addWidget(del_btn)
            new_col.addLayout(text_row)
            self.large_fields_layout.addLayout(new_col)
            self.total_lg_fields += 1




        self.btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setStyleSheet(self.internal_stylesheet)
        self.edit_btn.clicked.connect(self.__edit_fields)
        self.btn_row.addWidget(self.edit_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.setStyleSheet(self.internal_stylesheet)
        self.save_btn.clicked.connect(self.__save_fields)
        self.save_btn.hide()
        self.btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(self.internal_stylesheet)
        self.cancel_btn.clicked.connect(self.__cancel)
        self.cancel_btn.hide()
        self.btn_row.addWidget(self.cancel_btn)

        self.main_layout.addLayout(self.small_fields_layout)
        self.main_layout.addLayout(self.large_fields_layout)
        self.main_layout.addLayout(self.btn_row)
        self.setLayout(self.main_layout)



    def __edit_value_text(self, new_value, key=""):
        self.small_value_changes[key] = new_value

    def __edit_value_text_lg(self, text_edit_box, key=""):
        self.lg_value_changes[key] = text_edit_box.document()


    def __edit_key_text(self, new_key, old_key=""):
        self.small_key_changes[old_key] = new_key

    def __edit_key_text_lg(self, new_key, old_key=""):
        self.lg_key_changes[old_key] = new_key

    def __cycle_next_img(self):
        show_next_img = False
        for idx, label in enumerate(self.image_labels):
            if(show_next_img):
                label.show()
                show_next_img = False
                break
            if(label.isVisible()):
                show_next_img = True
                label.hide()
        if(show_next_img):
            self.image_labels[0].show()
            self.image_labels[len(self.image_labels)-1].hide()
            self.del_img_btns[len(self.image_labels)-1].hide()

    def __cycle_last_img(self):
        show_next_img = False
        counter = len(self.image_labels) - 1
        for label in reversed(self.image_labels):
            if(show_next_img):
                label.show()
                show_next_img = False
                break
            if(label.isVisible()):
                show_next_img = True
                label.hide()
            counter -= 1
        if(show_next_img):
            self.image_labels[len(self.image_labels) - 1].show()
            self.image_labels[0].hide()

    def __queue_for_deletion(self, key_field, value_field, key, del_btn):
        key_field.hide()
        value_field.hide()
        del_btn.hide()
        self.to_del_keys.append(key)
        self.hidden_fields.append(key_field)
        self.hidden_fields.append(value_field)
        self.hidden_fields.append(del_btn)


    def __save_fields(self):
        for key in self.small_value_changes:
            if(self.small_value_changes[key] != ""):
                self.token_record.change_small_field_values(self.token_key, key, self.small_value_changes[key])
        for old_key in self.small_key_changes:
            if(self.small_key_changes[old_key] != ""):
                self.token_record.change_small_field_keys(self.token_key, old_key, self.small_key_changes[old_key])
        for key in self.lg_value_changes:
            if(self.lg_value_changes[key] != ""):
                self.token_record.change_lg_field_values(self.token_key, key, self.lg_value_changes[key])
        for old_key in self.lg_key_changes:
            if(self.lg_key_changes[old_key] != ""):
                self.token_record.change_lg_field_keys(self.token_key, old_key, self.lg_key_changes[old_key])
        for label in self.all_labels:
            label.setReadOnly(True)
        for key in self.to_del_keys:
            self.token_record.delete_field(self.token_key, key)
        self.hidden_fields.clear()
        self.to_del_keys.clear()
        self.just_added.clear()
        self.__cancel()

    def __cancel(self):
        self.edit_btn.show()
        self.save_btn.hide()
        self.cancel_btn.hide()
        self.add_sm_btn.hide()
        self.add_lg_btn.hide()
        self.__clear_changes()

    def __clear_changes(self):
        for item in self.small_value_changes:
            self.small_value_changes[item] = ""
        for item in self.small_key_changes:
            self.small_key_changes[item] = ""
        for item in self.lg_value_changes:
            self.lg_value_changes[item] = ""
        for item in self.lg_key_changes:
            self.lg_key_changes[item] = ""
        for item in self.hidden_fields:
            item.show()
        for item in self.just_added:
            self.token_record.delete_field(self.token_key, item)
        for btn in self.del_btns:
            btn.hide()

    def __edit_fields(self):
        for label in self.all_labels:
            label.setReadOnly(False)
        self.edit_btn.hide()
        self.save_btn.show()
        self.cancel_btn.show()
        self.add_sm_btn.show()
        self.add_lg_btn.show()
        for btn in self.del_btns:
            btn.show()

    def __del_from_map(self):
        self.token_label.delete_token()

