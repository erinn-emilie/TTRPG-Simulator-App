import json
import math
from PIL import Image, ImageDraw

class TileTypes():
    JSON_FILE_PATH = "jsonfiles/TileTypes.json"

    def __init__(self):
        self.tiles_dict = {}
        self.tile_key_map = {}
        self.tile_names_list = []
        self.total_tiles = 0
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.tiles_dict = json.load(file)
            self.__setup()
        except FileNotFoundError:
            print("Couldn't find JSON file with tile types!")
        except json.JSONDecodeError:
            print("JSON file with tile types couldn't be decoded!")

    def __setup(self):
        counter = 0
        for tile in self.tiles_dict:
            self.tile_key_map[tile] = self.tiles_dict[tile]["key"]
            if(counter != 0):
                self.tile_names_list.append(self.tiles_dict[tile]["name"])
            counter += 1
        self.total_tiles = counter-1

    def get_total_tiles(self) -> int:
        return self.total_tiles

    def change_tile_name(self, old_name, new_name):
        counter = -1
        for tile in self.tiles_dict:
            if(self.tiles_dict[tile]["name"] == old_name):
                self.tiles_dict[tile]["name"] = new_name
                self.tiles_dict[new_name.upper()] = self.tiles_dict.pop(old_name.upper())
                self.tile_names_list[counter] = new_name
                break
            else:
                self.tiles_dict[tile]["tile_weights"][new_name.upper()] = self.tiles_dict[tile]["tile_weights"].pop(old_name.upper())
            counter += 1
        self.__update_json_file()

    def __update_json_file(self):
        with open(self.JSON_FILE_PATH, 'w') as file: 
            json.dump(self.tiles_dict, file, indent=4)

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

    def add_new_tile(self, tile_name:str, tile_default_asset:str):
        self.__create_hexagonal_image_mask(tile_default_asset)
        formatted_tile_name = tile_name.upper()
        new_weight_row = {formatted_tile_name: 100}
        highest_key = -1
        for tile in self.tiles_dict:
            self.tiles_dict[tile]["tile_weights"].update(new_weight_row)
            highest_key = self.tiles_dict[tile]["key"]

        new_tile_dict = {
            formatted_tile_name: {
                "key": highest_key+1,
                "name": tile_name,
                "tile_weights": {},
                "default_background": "",
                "default_asset": tile_default_asset,
                "user_assets": {
                    "slot1": "",
                    "slot2": "",
                    "slot3": "",
                    "slot4": "",
                    "slot5": ""
                }
            }
        }

        for tile in self.tile_names_list:
            new_tile_dict[formatted_tile_name]["tile_weights"].update({tile.upper(): 100})

        self.tiles_dict.update(new_tile_dict)
        self.__update_json_file()


    def change_tile_weight(self, tile_name:str, tile_weight_name:str, new_weight:int):
        self.tiles_dict[tile_name.upper()]["tile_weights"][tile_weight_name.upper()] = new_weight
        self.__update_json_file()


    def change_tile_image(self, tile_name:str, img_path_str:str):
        self.__create_hexagonal_image_mask(img_path_str)
        try:
            self.tiles_dict[tile_name]["default_asset"] = img_path_str 
        except KeyError:
            print("this didnt work lol")

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



