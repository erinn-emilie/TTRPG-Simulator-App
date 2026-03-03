
from Enums.TokenTypes import TokenTypes
import copy

class TokenRecord():
    def __init__(self, token_dict:dict, token_type:TokenTypes, record_key:int, position=(0,0)):
        self.token_dict = copy.deepcopy(token_dict)
        self.position = position
        self.token_dict["x_position"] = self.position[0]
        self.token_dict["y_position"] = self.position[1]
        self.record_key = record_key
        self.token_type = token_type
        self.name = self.token_dict["name"]
        self.key = self.token_dict["key"]

    def get_record_key(self) -> int:
        return self.record_key

    def get_token_key(self) -> int:
        return self.key
        
    def get_position(self) -> tuple:
        return self.position

    def get_x_position(self) -> float:
        return self.position[0]

    def get_y_position(self) -> float:
        return self.position[1]

    def get_token_name(self) -> str:
        return self.name

    def get_token_type(self) -> TokenTypes:
        return self.token_type

    def get_map_asset(self) -> str:
        return self.token_dict["set_map_asset"]

    def get_excluded_tiles(self) -> list:
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

    def set_position(self, new_pos:tuple):
        self.position = new_pos
        self.token_dict["x_position"] = new_pos[0]
        self.token_dict["y_position"] = new_pos[1]


    def change_small_field_values(self, token_key, value_key, new_value):
        if(value_key == "name"):
            self.token_dict["name"] = new_value
        else:
            self.token_dict["small_fields"][value_key] = new_value

    def change_small_field_keys(self, token_key, old_key, new_key):
        self.token_dict["small_fields"][new_key] = self.token_dict["small_fields"].pop(old_key)


    def change_lg_field_values(self, token_key, value_key, new_value):
        plain_txt = new_value.toPlainText()
        self.token_dict["large_fields"][value_key] = plain_txt


    def change_lg_field_keys(self, token_key, old_key, new_key):
        self.token_dict["large_fields"][new_key] = self.token_dict["large_fields"].pop(old_key)
        