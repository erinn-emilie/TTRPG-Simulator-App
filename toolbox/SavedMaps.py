import json
from toolbox.Database import Database

class SavedMaps():
    def __init__(self, account_ref):
        self.JSON_FILE_PATH = "jsonfiles/SavedMaps.json"
        self.active_save_name = ""
        self.active_save_dict = {}
        self.all_saved_maps = {}
        self.account_ref = account_ref
        self.all_saved_maps = {}
        self.fetch_saved_maps()


    def set_active_save_dict(self, save_dict:dict):
        self.active_save_dict = save_dict

    def get_active_save_dict(self) -> dict:
        return self.active_save_dict


    def set_active_save_name(self, save_name:str):
        self.active_save_name = save_name

    def get_active_save_name(self) -> str:
        return self.active_save_name

    def get_all_saved_maps(self):
        return self.all_saved_maps


    def fetch_saved_maps(self):
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.all_saved_maps = json.load(file)
        except FileNotFoundError:
            print("Couldn't find JSON file with maps!")
        except json.JSONDecodeError:
            print("JSON file with maps couldn't be decoded!")


    def fetch_from_database(self):
        user_id = self.account_ref.get_account_id()
        db_maps = Database.get_all_maps(user_id)
        for map_name in db_maps:
            self.all_saved_maps[map_name] = db_maps[map_name]

    def __write_saved_maps(self):
        try:
            with open(self.JSON_FILE_PATH, 'w') as file:
                json.dump(self.all_saved_maps, file, indent=4)
        except FileNotFoundError:
            print("Couldn't find JSON file with maps!")

    def add_saved_map(self, map_name, map_dict, local=True):
        if(local):
            self.__write_saved_maps()
        else:
            user_id = self.account_ref.get_account_id()
            public_key = Database.add_map_to_db(user_id, map_name, map_dict)
            map_dict["public_key"] = public_key
        self.all_saved_maps[map_name] = map_dict



    def remove_saved_map(self, map_name, local=True):
        del self.all_saved_maps[map_name]
        if(local):
            self.__write_saved_maps()
        else:
            user_id = self.account_ref.get_account_id()
            Database.remove_map_from_db(user_id, map_name)


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
