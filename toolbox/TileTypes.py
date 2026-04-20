import json
import math
from PIL import Image, ImageDraw
import copy

from toolbox.Database import Database

class TileTypes():
    JSON_FILE_PATH = "jsonfiles/TileTypes.json"
    CHANGES_FILE_PATH = "jsonfiles/Changes.json"

    def __init__(self, account_ref):
        self.tiles_dict = {}
        self.local_dict = {}
        self.changes = {}
        self.tile_key_map = {}
        self.tile_names_list = []
        self.total_tiles = 0
        self.account_ref = account_ref
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.tiles_dict = json.load(file)
                self.local_dict = copy.deepcopy(self.tiles_dict)
            with open(self.CHANGES_FILE_PATH, 'r') as file:
                self.changes = json.load(file)
            self.__setup()
        except FileNotFoundError:
            print("Couldn't find JSON file with tile types!")
        except json.JSONDecodeError:
            print("JSON file with tile types couldn't be decoded!")

    def __setup(self):
        counter = -1
        self.tile_names_list.clear()
        for tile in self.tiles_dict:
            if(not "key" in self.tiles_dict[tile]):
                self.tiles_dict[tile]["key"] = counter
            self.tile_key_map[tile] = self.tiles_dict[tile]["key"]
            if(counter != -1):
                self.tile_names_list.append(self.tiles_dict[tile]["name"])
            counter += 1
        self.total_tiles = counter

    def load_from_database(self):
        user_id = self.account_ref.get_account_id()
        db_dict = Database.load_all_tiles(user_id)
        for name in db_dict:
            db_dict[name]["tile_weights"] = eval(db_dict[name]["tile_weights"])

        for old_name in self.changes["NEW_NAMES"]:
            for tile in db_dict:
                new_name = self.changes["NEW_NAMES"][old_name]
                db_dict[tile]["tile_weights"][new_name.upper()] = db_dict[tile]["tile_weights"].pop(old_name.upper())
                Database.change_tile_weight(user_id, db_dict[tile]["name"], db_dict[tile]["tile_weights"])
        for local_name in self.local_dict:
            for tile in db_dict:
                if(not local_name in db_dict[tile]["tile_weights"]):
                    db_dict[tile]["tile_weights"][local_name] = 100
                    Database.change_tile_weight(user_id, db_dict[tile]["name"], db_dict[tile]["tile_weights"])

        self.changes["NEW_NAMES"].clear()
        self.__update_change_file()
        for tile in db_dict:
            self.tiles_dict[tile] = db_dict[tile]
        self.__setup()

    def get_total_tiles(self) -> int:
        return self.total_tiles

    def change_tile_name(self, old_name, new_name):
        local = True
        user_id = self.account_ref.get_account_id()
        if(self.tiles_dict[old_name.upper()]["save_location"] != "local"):
            local = False
        prev_dict = copy.deepcopy(self.tiles_dict)
        for tile in prev_dict:
            if(self.tiles_dict[tile]["name"] == old_name):
                if(local):
                    self.local_dict[tile]["name"] = new_name
                    self.local_dict[new_name.upper()] = self.local_dict.pop(old_name.upper())
                    self.local_dict[new_name.upper()]["default"] = False
                else:
                    Database.change_tile_name(user_id, new_name, old_name)
                self.tiles_dict[tile]["name"] = new_name
                self.tiles_dict[new_name.upper()] = self.tiles_dict.pop(old_name.upper())
                self.tiles_dict[new_name.upper()]["default"] = False
            else:
                self.tiles_dict[tile]["tile_weights"][new_name.upper()] = self.tiles_dict[tile]["tile_weights"].pop(old_name.upper())
                if(self.account_ref.get_logged_in()):
                    Database.change_tile_weight(user_id, tile, self.tiles_dict[tile]["tile_weights"])
                else:
                    self.local_dict[tile]["tile_weights"][new_name.upper()] = self.local_dict[tile]["tile_weights"].pop(old_name.upper())
                    if(old_name != "New Tile"):
                        self.changes["NEW_NAMES"][old_name] = new_name
        self.__setup()
        self.__update_json_file()
        self.__update_change_file()

    def __update_json_file(self):
        with open(self.JSON_FILE_PATH, 'w') as file: 
            json.dump(self.local_dict, file, indent=4)

    def __update_change_file(self):
        with open (self.CHANGES_FILE_PATH, 'w') as file:
            json.dump(self.changes, file, indent=4)

    def get_tile_names_list(self) -> list:
        return self.tile_names_list

    def get_tile_name_by_key(self, key) -> str:
        try: 
            for tile in self.tile_key_map:
                if self.tile_key_map[tile] == key:
                    return tile
            return "NONE"
        except KeyError:
            return "NONE"

    def get_tile_key_by_name(self, tileName) -> int:
        try: 
            return self.tile_key_map[tileName]
        except KeyError:
            return -1


    def get_tile_weight_by_name(self, rowTileName:str, colTileName:str) -> int:
        try: 
            return self.tiles_dict[rowTileName]["tile_weights"][colTileName]
        except KeyError:
            return 0

    def get_tile_weight_by_key(self, row:int, col:int) -> int:
        rowTileName = self.get_tile_name_by_key(row)
        colTileName = self.get_tile_name_by_key(col)
        return self.get_tile_weight_by_name(rowTileName, colTileName)

    def get_tile_weights_by_name(self, tileName:str) -> dict:
        try:
            return self.tiles_dict[tileName.upper()]["tile_weights"]
        except KeyError:
            return dict

    def get_tile_default_by_name(self, tileName:str):
        try:
            return self.tiles_dict[tileName.upper()]["default"]
        except KeyError:
            return False


    def get_default_tile_asset_by_name(self, tileName:str) -> str:
        try: 
            return self.tiles_dict[tileName]["default_asset"]
        except KeyError:
            return ""

    def get_default_tile_background_by_name(self, tileName:str) -> str:
        try:
            return self.tiles_dict[tileName]["default_background"]
        except KeyError:
            return ""

    def set_default_tile_background_by_name(self, tileName:str, tileBackground:str):
        if(self.tiles_dict[tileName]["save_location"] == "local"):
            self.local_dict[tileName]["default_background"] = tileBackground
            self.local_dict[tileName]["default"] = False
            self.__update_json_file()
        else:
            user_id = self.acccount_ref.get_account_id()
            Database.change_tile_background(user_id, tileName, tileBackground)
        self.tiles_dict[tileName]["default_background"] = tileBackground
        self.tiles_dict[tileName]["default"] = False
        self.__update_json_file()

    def add_new_tile(self, tile_name:str, tile_default_asset:str, local=True):
        self.__create_hexagonal_image_mask(tile_default_asset)
        formatted_tile_name = tile_name.upper()
        new_weight_row = {formatted_tile_name: 100}
        highest_key = -1
        user_id = self.account_ref.get_account_id()
        for tile in self.tiles_dict:
            self.tiles_dict[tile]["tile_weights"].update(new_weight_row)
            highest_key = self.tiles_dict[tile]["key"]
            if(self.account_ref.get_logged_in()):
                Database.change_tile_weight(user_id, self.tiles_dict[tile]["name"], self.tiles_dict[tile]["tile_weights"])
        
        for tile in self.local_dict:
            self.local_dict[tile]["tile_weights"].update(new_weight_row)

        new_tile_dict = {
            formatted_tile_name: {
                "key": highest_key+1,
                "name": tile_name,
                "tile_weights": {},
                "default_background": "",
                "default_asset": tile_default_asset,
                "default": False
            }
        }

        for tile in self.tile_names_list:
            new_tile_dict[formatted_tile_name]["tile_weights"].update({tile.upper(): 100})

        if(local):
            new_tile_dict[formatted_tile_name]["save_location"] = "local"
            self.local_dict.update(new_tile_dict)
        else:
            user_id = self.account_ref.get_account_id()
            new_tile_dict[formatted_tile_name]["save_location"] = "database"
            Database.add_tile(user_id, tile_name, new_tile_dict[formatted_tile_name]["tile_weights"], tile_default_asset, "")
        self.tiles_dict.update(new_tile_dict)
        self.__update_json_file()


    def change_tile_weight(self, tile_name:str, tile_weight_name:str, new_weight:int):
        self.tiles_dict[tile_name.upper()]["tile_weights"][tile_weight_name.upper()] = new_weight
        self.tiles_dict[tile_weight_name.upper()]["tile_weights"][tile_name.upper()] = new_weight
        if(self.tiles_dict[tile_name.upper()]["save_location"] == "local"):
            self.local_dict[tile_name.upper()]["tile_weights"][tile_weight_name.upper()] = new_weight
            self.local_dict[tile_weight_name.upper()]["tile_weights"][tile_name.upper()] = new_weight
            self.__update_json_file()
        else:
            user_id = self.account_ref.get_account_id()
            Database.change_tile_weight(user_id, tile_name, self.tiles_dict[tile_name.upper()]["tile_weights"])
            Database.change_tile_weight(user_id, tile_weight_name, self.tiles_dict[tile_weight_name.upper()]["tile_weights"])
        self.__setup()


    def change_tile_image(self, tile_name:str, img_path_str:str):
        self.__create_hexagonal_image_mask(img_path_str)
        if(self.tiles_dict[tile_name.upper()]["save_location"] == "local"):
            self.local_dict[tile_name.upper()]["default_asset"] = img_path_str
            self.local_dict[tile_name.upper()]["default"] = False
            self.__update_json_file()
        else:
            user_id = self.account_ref.get_account_id()
            Database.change_tile_img(user_id, tile_name, img_path_str)
        self.tiles_dict[tile_name.upper()]["default_asset"] = img_path_str 
        self.tiles_dict[tile_name.upper()]["default"] = False 

    def change_tile_img_current(self, tile_name:str, data):
        self.tiles_dict[tile_name.upper()]["default_asset"] = data


    def __create_hexagonal_image_mask(self, img_path_str:str):
        img = Image.open(img_path_str).convert("RGBA")
        width = 500
        height = 500
        img = img.resize((width,height))

        im_a = Image.new("L", img.size, 0)
    
        center_x = math.floor(width/2)
        center_y = math.floor(height/2)
        radius = 250      
        n_sides = 6
    
        points = []
        for i in range(n_sides):
            angle = 2 * math.pi * i / n_sides
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x,y))
    
        draw = ImageDraw.Draw(im_a)
        draw.polygon(points,fill=255)
        im_rgba = img.copy()
        im_rgba.putalpha(im_a)
        im_rgba.save(img_path_str)



