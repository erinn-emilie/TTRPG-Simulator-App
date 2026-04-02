import json

class SavedMaps():
    def __init__(self):
        self.JSON_FILE_PATH = "jsonfiles/SavedMaps.json"
        
        self.fetch_saved_maps()


    def fetch_saved_maps(self):
        self.all_saved_maps = {}
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.all_saved_maps = json.load(file)
        except FileNotFoundError:
            print("Couldn't find JSON file with maps!")
        except json.JSONDecodeError:
            print("JSON file with maps couldn't be decoded!")

    def find_map_by_name(self, map_name:str) -> dict:
        for maps in self.all_saved_maps:
            if maps == map_name:
                return self.all_saved_maps[maps]

        return None

    def find_tile_in_map(self, map_name:str, tile_key:int) -> dict:
        map_dict = self.find_tile_in_map() 
        if map_dict:
            for tile in map_dict:
                if tile == str(tile_key):
                    return map_dict[tile]
            return None
