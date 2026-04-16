
from Enums.TokenTypes import TokenTypes
import copy

class TokenRecord():
    def __init__(self, logger_ref, token_dict:dict, token_type:TokenTypes, position=(0,0)):
        self.logger_ref = logger_ref
        self.token_dict = copy.deepcopy(token_dict)
        self.position = position
        self.token_dict["x_position"] = self.position[0]
        self.token_dict["y_position"] = self.position[1]
        self.token_type = token_type
        self.token_dict["token_type"] = TokenTypes.get_str_from_token_type(self.token_type)
        self.save_location = self.token_dict["save_location"]
        self.name = self.token_dict["name"]
        self.key = self.token_dict["key"]
        self.default = True
        self.__log_new_token()

    def get_save_location(self) -> str:
        return self.save_location

    def get_name(self) -> str:
        return self.name

    def get_token_key(self) -> int:
        return self.key
        
    def get_position(self) -> tuple:
        return self.position

    def get_x_position(self) -> int:
        return self.position[0]

    def get_y_position(self) -> int:
        return self.position[1]

    def get_token_name(self) -> str:
        return self.name

    def get_token_type(self) -> TokenTypes:
        return self.token_type

    def get_map_asset(self):
        return self.token_dict["set_map_asset"]

    def get_excluded_tiles(self) -> dict:
        return self.token_dict["excluded_tiles"]

    def get_small_fields(self):
        return self.token_dict["small_fields"]

    def get_large_fields(self):
        return self.token_dict["large_fields"]

    def get_base_height_multiplier(self):
        return self.token_dict["base_height_multiplier"]

    def get_base_width_multiplier(self):
        return self.token_dict["base_width_multiplier"]

    def get_token_dict(self):
        return self.token_dict

    def get_large_assets(self):
        return self.token_dict["large_assets"]

    def get_default_status(self):
        return self.default

    def __log_new_token(self):
        if(self.logger_ref.get_writable_status()):
            change_line = self.name + " was added to the map"
            self.logger_ref.add_line(change_line)

    def __log_position_change(self, new_pos:tuple, old_pos:tuple):
        if(self.logger_ref.get_writable_status()):
            change_line = self.name + " moved from " + "(" + str(old_pos[0]) + ", " + str(old_pos[1]) + ") to (" + str(new_pos[0]) + ", " + str(new_pos[1]) + ")"
            self.logger_ref.add_line(change_line)

    def set_position(self, new_pos:tuple):
        self.__log_position_change(new_pos, self.position)
        self.position = new_pos
        self.token_dict["x_position"] = new_pos[0]
        self.token_dict["y_position"] = new_pos[1]


    def __log_value_changes(self, old_value, new_value, value_key):
        self.default = False
        if(self.logger_ref.get_writable_status()):
            change_line = self.name + "'s " + value_key + " value changes from " + old_value + " to " + new_value
            self.logger_ref.add_line(change_line)

    def __log_key_changes(self, old_key, new_key):
        self.default = False
        if(self.logger_ref.get_writable_status()):
            change_line = "The name of " + old_key + " for " + self.name + " changed to " + new_key
            self.logger_ref.add_line(change_line)


    def change_small_field_values(self, token_key, value_key, new_value):
        if(value_key == "name"):
            self.__log_value_changes(self.token_dict["name"], new_value, value_key)
            self.token_dict["name"] = new_value
        else:
            self.__log_value_changes(self.token_dict["small_fields"][value_key], new_value, value_key)
            self.token_dict["small_fields"][value_key] = new_value

    def change_small_field_keys(self, token_key, old_key, new_key):
        self.__log_value_changes(old_key, new_key)
        self.token_dict["small_fields"][new_key] = self.token_dict["small_fields"].pop(old_key)


    def change_lg_field_values(self, token_key, value_key, new_value):
        self.__log_key_changes(self.token_dict["large_fields"][value_key], new_value, value_key)
        plain_txt = new_value.toPlainText()
        self.token_dict["large_fields"][value_key] = plain_txt


    def change_lg_field_keys(self, token_key, old_key, new_key):
        self.__log_value_changes(old_key, new_key)
        self.token_dict["large_fields"][new_key] = self.token_dict["large_fields"].pop(old_key)
        