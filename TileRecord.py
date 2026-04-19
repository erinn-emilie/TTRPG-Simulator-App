from Enums.TokenTypes import TokenTypes
from TokenRecord import TokenRecord

class TileRecord():
    def __init__(self, tile_type:str, background_img_path=""):
        self.tile_type = tile_type
        self.all_token_records = []
        self.background_img_path = background_img_path
        self.empty_positions = []
        self.default = True

    def set_default_status(self, status):
        self.default = status

    def get_default_status(self):
        return self.default

    def get_background_img_path(self) -> str:
        return self.background_img_path

    def set_background_img_path(self, new_path:str):
        self.background_img_path = new_path

    def add_token_record(self, record:TokenRecord):
        self.all_token_records.append(record)

    def delete_token_record(self, record:TokenRecord):
        self.all_token_records.remove(record)

    def get_token_records(self) -> list:
        return self.all_token_records

    def get_tile_type(self) -> str:
        return self.tile_type

    def set_tile_type(self, new_type:str):
        self.tile_type = new_type

    def check_position_filled(self, pos:tuple):
        if pos in self.empty_positions:
            return False
        return True

    def fill_empty_positions(self, pos_list:list):
        self.empty_positions = pos_list

    def remove_empty_position(self, pos:tuple):
        if pos in self.empty_positions:
            print("removed")
            self.empty_positions.remove(pos)

    def add_empty_position(self, pos:tuple):
        self.empty_positions.append(pos)
