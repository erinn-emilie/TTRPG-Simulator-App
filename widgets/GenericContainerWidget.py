from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QFileDialog
    )

from functools import partial
from toolbox.Toolbox import Toolbox
import os

 
class TokenContainerWidget(QWidget):
    def __init__(self, token:dict, toolbox:Toolbox, token_class_ref):
        super().__init__()
        self.toolbox = toolbox
        self.token = token
        self.token_class_ref = token_class_ref
        self.setStyleSheet("""
            background-color: pink;
        """)

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
        self.small_value_changes["name"] = ""
        name_label.textEdited.connect(partial(self.__edit_value_text, key="name"))
        name_row.addWidget(name_label)
        self.all_labels.append(name_label)

        self.main_layout.addLayout(name_row)

        map_asset_row = QHBoxLayout()
        map_asset_label = QLabel()
        map_asset_pix = QPixmap(self.map_asset)
        map_asset_label.setPixmap(map_asset_pix)
        map_asset_row.addWidget(map_asset_label)
        change_map_asset_btn = QPushButton("Change Map Asset")
        change_map_asset_btn.clicked.connect(partial(self.__change_map_asset))
        map_asset_row.addWidget(change_map_asset_btn)
        self.main_layout.addLayout(map_asset_row)

        self.total_images = 0
        self.images = self.token["large_assets"]
        self.image_labels = []
        self.del_img_btns = []
        for image in self.images:
            img_label = QLabel()
            pixmap = QPixmap(image)
            img_label.setPixmap(pixmap)
            self.image_labels.append(img_label)
            del_btn = QPushButton("Remove Image")
            self.del_img_btns.append(del_btn)
            del_btn.clicked.connect(partial(self.__delete_image, image, img_label))
            self.main_layout.addWidget(img_label)
            self.main_layout.addWidget(del_btn)


            self.total_images += 1

            

        for idx, label in enumerate(self.image_labels):
            if(idx != 0):
                label.hide()
                self.del_img_btns[idx].hide()


        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.__upload_image)
        self.main_layout.addWidget(self.upload_btn)


        self.img_forward_btn = QPushButton(">")
        self.main_layout.addWidget(self.img_forward_btn)
        self.img_forward_btn.clicked.connect(self.__cycle_next_img)
        self.img_backward_btn = QPushButton("<")
        self.main_layout.addWidget(self.img_backward_btn)
        self.img_backward_btn.clicked.connect(self.__cycle_last_img)

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


            
            new_row.addWidget(field_name)
            new_row.addWidget(field_value)
            new_row.addWidget(del_btn)
            self.small_fields_layout.addLayout(new_row)
            self.total_sm_fields += 1


        self.small_fields_layout.addLayout(new_row)

        add_sm_btn_row = QHBoxLayout()
        self.add_sm_btn = QPushButton("Add Small Field")
        self.add_sm_btn.clicked.connect(self.__add_sm_field)
        self.add_sm_btn.hide()
        add_sm_btn_row .addWidget(self.add_sm_btn)
        self.small_fields_layout.addLayout(add_sm_btn_row)

        for lg_field in self.token_large_fields:
            new_col = QVBoxLayout()
            label_row = QHBoxLayout()
            label = QLineEdit(lg_field)
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

            text_row.addWidget(new_line)
            text_row.addWidget(del_btn)
            new_col.addLayout(text_row)
            self.large_fields_layout.addLayout(new_col)
            self.total_lg_fields += 1


        add_lg_btn_row = QHBoxLayout()
        self.add_lg_btn = QPushButton("Add Large Field")
        self.add_lg_btn.clicked.connect(self.__add_lg_field)
        self.add_lg_btn.hide()
        add_lg_btn_row .addWidget(self.add_lg_btn)
        self.large_fields_layout.addLayout(add_lg_btn_row)


        self.btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.__edit_fields)
        self.btn_row.addWidget(self.edit_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.__save_fields)
        self.save_btn.hide()
        self.btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
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
                img_name = os.path.basename(img_path)

                img_name = img_name.replace(".jpg", ".png")
                img_name = img_name.replace(".jpeg", ".png")
                cur_dir = os.getcwd()
                asset_dir = os.path.join(cur_dir, "assets")
                asset_path = os.path.join(asset_dir, img_name)
                os.rename(img_path, asset_path)
                self.token_class_ref.add_new_large_image(self.token_key, asset_path)
                self.total_images += 1
                img_label = QLabel()
                pixmap = QPixmap(asset_path)
                img_label.setPixmap(pixmap)
                self.image_labels.append(img_label)
                del_btn = QPushButton("Remove Image")
                self.del_img_btns.append(del_btn)
                del_btn.clicked.connect(partial(self.__delete_image, asset_path, img_label))
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
                img_name = os.path.basename(img_path)

                img_name = img_name.replace(".jpg", ".png")
                img_name = img_name.replace(".jpeg", ".png")
                cur_dir = os.getcwd()
                asset_dir = os.path.join(cur_dir, "assets")
                asset_path = os.path.join(asset_dir, img_name)
                os.rename(img_path, asset_path)
                self.token_class_ref.change_map_asset(self.token_key, asset_path)
                self.total_images += 1
                img_label = QLabel()
                pixmap = QPixmap(asset_path)
                img_label.setPixmap(pixmap)
                self.image_labels.append(img_label)
                self.main_layout.insertWidget(self.total_images, img_label)
                for label in self.image_labels:
                    label.hide()
                img_label.show()
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

        self.token_class_ref.add_new_sm_field(self.token_key, sm_field, value)
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

        self.token_class_ref.add_new_lg_field(self.token_key, lg_field, value)
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
                self.token_class_ref.change_small_field_values(self.token_key, key, self.small_value_changes[key])
        for old_key in self.small_key_changes:
            if(self.small_key_changes[old_key] != ""):
                self.token_class_ref.change_small_field_keys(self.token_key, old_key, self.small_key_changes[old_key])
        for key in self.lg_value_changes:
            if(self.lg_value_changes[key] != ""):
                self.token_class_ref.change_lg_field_values(self.token_key, key, self.lg_value_changes[key])
        for old_key in self.lg_key_changes:
            if(self.lg_key_changes[old_key] != ""):
                self.token_class_ref.change_lg_field_keys(self.token_key, old_key, self.lg_key_changes[old_key])
        for label in self.all_labels:
            label.setReadOnly(True)
        for key in self.to_del_keys:
            self.token_class_ref.delete_field(self.token_key, key)
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
            self.token_class_ref.delete_field(self.token_key, item)
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


    def __delete_image(self, img_path, image_label):
        if os.path.exists(img_path):
            os.remove(img_path)
            self.token_class_ref.remove_large_image(self.token_key, img_path)
            image_label.hide()
        else:
          print("The file does not exist") 


        

class TileContainerWidget(QWidget):
    def __init__(self, tile_name:str, toolbox:Toolbox, tile_image_path:str):
        super().__init__()
        self.toolbox = toolbox
        self.tile_types_ref = self.toolbox.get_tile_types_ref()
        self.main_layout = QVBoxLayout()


        self.tile_name_prompt_label = QLabel("Tile Name:")

        self.old_tile_name = tile_name
        self.new_tile_name = ""
        self.tile_name_label = QLineEdit(self.old_tile_name)
        self.tile_name_label.setReadOnly(True)
        self.tile_name_label.textEdited.connect(self.__tile_name_edited)
        self.tile_name_label.setMaximumWidth(200)
        self.tile_name_prompt_label.setMaximumWidth(200)


        self.tile_image_pixmap = QPixmap(tile_image_path)
        self.tile_image_label = QLabel()
        self.tile_image_label.setPixmap(self.tile_image_pixmap)
        self.tile_image_label.setScaledContents(True)
        self.tile_image_label.setMaximumWidth(300)
        self.tile_image_label.setMaximumHeight(300)
        self.tile_name_row = QHBoxLayout()
        self.tile_name_row.addWidget(self.tile_name_prompt_label)
        self.tile_name_row.addWidget(self.tile_name_label)
        self.tile_name_row.addWidget(self.tile_image_label)
        self.main_layout.addLayout(self.tile_name_row)
        self.setLayout(self.main_layout)

    def enable_tile_name_label(self):
        self.tile_name_label.setReadOnly(False)

    def disable_tile_name_label(self):
        self.tile_name_label.setReadOnly(True)

    def __tile_name_edited(self,text):
        self.new_tile_name = text

    def cancel_tile_name_edit(self):
        self.new_tile_name = ""

    def save_new_tile_name(self):
        if(self.new_tile_name != ""):
            self.tile_types_ref.change_tile_name(self.old_tile_name, self.new_tile_name)
            self.old_tile_name = self.new_tile_name
            self.new_tile_name = ""




class TokenRecordContainerWidget(QWidget):
    def __init__(self, token_record, toolbox:Toolbox):
        super().__init__()
        self.toolbox = toolbox
        self.token_record = token_record
        self.setStyleSheet("""
            background-color: pink;
        """)

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
        self.small_value_changes["name"] = ""
        
        name_label.textEdited.connect(partial(self.__edit_value_text, key="name"))
        name_row.addWidget(name_label)
        self.all_labels.append(name_label)

        self.main_layout.addLayout(name_row)

        map_asset_row = QHBoxLayout()
        map_asset_label = QLabel()
        map_asset_pix = QPixmap(self.map_asset)
        map_asset_label.setPixmap(map_asset_pix)
        map_asset_row.addWidget(map_asset_label)
        change_map_asset_btn = QPushButton("Change Map Asset")
        map_asset_row.addWidget(change_map_asset_btn)
        self.main_layout.addLayout(map_asset_row)

        self.total_images = 0
        self.images = self.token_record.get_large_assets()
        self.image_labels = []
        for image in self.images:
            img_label = QLabel()
            pixmap = QPixmap(image)
            img_label.setPixmap(pixmap)
            self.image_labels.append(img_label)

            self.main_layout.addWidget(img_label)

            self.total_images += 1

            

        for idx, label in enumerate(self.image_labels):
            if(idx != 0):
                label.hide()



        self.img_forward_btn = QPushButton(">")
        self.main_layout.addWidget(self.img_forward_btn)
        self.img_forward_btn.clicked.connect(self.__cycle_next_img)
        self.img_backward_btn = QPushButton("<")
        self.main_layout.addWidget(self.img_backward_btn)
        self.img_backward_btn.clicked.connect(self.__cycle_last_img)

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


            
            new_row.addWidget(field_name)
            new_row.addWidget(field_value)
            new_row.addWidget(del_btn)
            self.small_fields_layout.addLayout(new_row)
            self.total_sm_fields += 1


        self.small_fields_layout.addLayout(new_row)

        add_sm_btn_row = QHBoxLayout()
        self.add_sm_btn = QPushButton("Add Small Field")
        #self.add_sm_btn.clicked.connect(self.__add_sm_field)
        self.add_sm_btn.hide()
        add_sm_btn_row .addWidget(self.add_sm_btn)
        self.small_fields_layout.addLayout(add_sm_btn_row)

        for lg_field in self.token_large_fields:
            new_col = QVBoxLayout()
            label_row = QHBoxLayout()
            label = QLineEdit(lg_field)
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

            text_row.addWidget(new_line)
            text_row.addWidget(del_btn)
            new_col.addLayout(text_row)
            self.large_fields_layout.addLayout(new_col)
            self.total_lg_fields += 1


        add_lg_btn_row = QHBoxLayout()
        self.add_lg_btn = QPushButton("Add Large Field")
        #self.add_lg_btn.clicked.connect(self.__add_lg_field)
        self.add_lg_btn.hide()
        add_lg_btn_row .addWidget(self.add_lg_btn)
        self.large_fields_layout.addLayout(add_lg_btn_row)


        self.btn_row = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.__edit_fields)
        self.btn_row.addWidget(self.edit_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.__save_fields)
        self.save_btn.hide()
        self.btn_row.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
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
