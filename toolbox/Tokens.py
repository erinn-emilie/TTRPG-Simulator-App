import json
import copy

from toolbox.Database import Database
from Enums.TokenTypes import TokenTypes

class Tokens():
    def __init__(self, json_file_path, asset_path, token_type, account_ref, local=True):
        self.JSON_FILE_PATH = json_file_path
        self.ASSET_PATH = asset_path
        self.account_ref = account_ref
        self.tokens_dict = {}
        self.tokens_list = []
        self.default_token_setup = {}
        self.total_tokens = 0
        self.token_type = token_type
        self.title_str = self.JSON_FILE_PATH.lower().replace(".json", "").replace("jsonfiles/", "")
        self.tokens_dict = {}
        if(local):
            self.load_from_json()
        else:
            self.load_from_database()

    def load_from_json(self):
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.tokens_dict = json.load(file)
            self.__setup()
        except FileNotFoundError:
            print("Couldn't find JSON file with tokens!")
        except json.JSONDecodeError:
            print("JSON file with tokens couldn't be decoded!")

    def load_from_database(self):
        self.tokens_dict = Database.load_all_tokens_with_type(self.account_ref.get_account_id(), TokenTypes.get_str_from_token_type(self.token_type))
        self.__setup()


    def __setup(self):
        #self.tokens_list.clear()
        self.default_token_setup = self.tokens_dict["DEFAULT"]
        counter = 0
        for token in self.tokens_dict:
            if(token != "DEFAULT"):
                self.tokens_list.append(self.tokens_dict[token])
                counter += 1
        self.total_tokens = counter

    def get_asset_str(self):
        return self.ASSET_PATH

    def get_title_str(self):
        return self.title_str

    def get_token_type(self):
        return self.token_type

    def get_num_of_tokens(self):
        return self.total_tokens

    def get_random_token_by_value(self, idx):
        if(idx < len(self.tokens_list)):
            return self.tokens_list[idx]
        return None



    def change_map_asset(self, token_key, img_path):
         for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                old_map_asset = self.tokens_dict[token]["set_map_asset"]
                self.tokens_dict[token]["set_map_asset"] = img_path
                old_map_assets_list = self.tokens_dict[token]["old_map_assets"]
                old_map_assets_list.append(old_map_asset)
                self.tokens_dict[token]["old_map_assets"] = old_map_assets_list
                self.__update_json_file()
                break


    def add_new_large_image(self, token_key, img_path):
         for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict[token]["large_assets"].append(img_path)
                self.__update_json_file()
                break

    def remove_large_image(self, token_key, img_path):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                for idx, image in enumerate(self.tokens_dict[token]["large_assets"]):
                    if(image == img_path):
                        del self.tokens_dict[token]["large_assets"][idx]
                        break
                break
        self.__update_json_file()

    def create_new_token(self, local=True) -> dict:
        default_token = self.tokens_dict["DEFAULT"]
        user_id = self.account_ref.get_account_id()
        self.total_tokens += 1
        new_name = "new token"
        new_token = copy.deepcopy(default_token)
        new_token["name"] = new_name
        new_token["key"] = self.total_tokens
        self.tokens_list.append(new_token)
        self.tokens_dict[new_name.upper()] = new_token
        if(local):
            self.tokens_dict[new_name.upper()]["save_location"] = "local"
            self.__update_json_file()
        else:
            Database.add_new_token(user_id, self.total_tokens, new_name, self.token_type, new_token["small_fields"], new_token["large_fields"])
        return self.tokens_dict[new_name.upper()]

    def delete_token(self, token_key):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict.pop(token)
                break
        self.__update_json_file()
    def get_tokens_list(self) -> list:
        return self.tokens_list


    def get_token_by_name(self, name:str) -> dict:
        for token in self.tokens_dict:
            if(token == name.upper()):
                return self.tokens_dict[token]
        return self.default_token_setup

    def get_token_by_key(self, key:int) -> dict:
        for token in self.tokens_list:
            if(token["key"] == key):
                return token
        return self.default_token_setup

    def __check_local(self, value):
        if value == "local":
            return True
        return False

    def change_small_field_values(self, token_key, value_key, new_value):
        local = True
        user_id = self.account_ref.get_account_id()
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                local = self.__check_local(self.tokens_dict[token]["save_location"])
                if(value_key == "name"):
                    if(not local):
                        Database.update_token_name(user_id, self.tokens_dict[token]["name"], new_value)
                    self.tokens_dict[token]["name"] = new_value
                    self.tokens_dict[new_value.upper()] = self.tokens_dict.pop(token)
                else:
                    self.tokens_dict[token]["small_fields"][value_key] = new_value
                    if(not local):
                        Database.update_small_fields(user_id, self.tokens_dict)
                break
        if(local):
            self.__update_json_file()

    def change_small_field_keys(self, token_key, old_key, new_key):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict[token]["small_fields"][new_key] = self.tokens_dict[token]["small_fields"].pop(old_key)
                break
        self.__update_json_file()


    def change_lg_field_values(self, token_key, value_key, new_value):
        plain_txt = new_value.toPlainText()
        print(plain_txt)
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict[token]["large_fields"][value_key] = plain_txt
                break
        self.__update_json_file()


    def change_lg_field_keys(self, token_key, old_key, new_key):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict[token]["large_fields"][new_key] = self.tokens_dict[token]["large_fields"].pop(old_key)
                break
        self.__update_json_file()


    def delete_field(self, token_key, retired_key) -> bool:
        found = False
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                if(retired_key in self.tokens_dict[token]["small_fields"]):
                    del self.tokens_dict[token]["small_fields"][retired_key]
                    found = True
                else:
                    if(retired_key in self.tokens_dict[token]["large_fields"]):
                        del self.tokens_dict[token]["large_fields"][retired_key]
                        found = True
                break
        if(found):
            self.__update_json_file()
        return found

    def add_new_sm_field(self, token_key, new_key, new_value):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                inc = 1
                while(new_key in self.tokens_dict[token]["small_fields"]):
                    new_key += str(inc)
                    inc += 1
                self.tokens_dict[token]["small_fields"][new_key] = new_value
        self.__update_json_file()

    def add_new_lg_field(self, token_key, new_key, new_value):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                inc = 1
                while(new_key in self.tokens_dict[token]["large_fields"]):
                    new_key += str(inc)
                    inc += 1
                self.tokens_dict[token]["large_fields"][new_key] = new_value
        self.__update_json_file()

    def import_token(self, token_dict: dict):
        token_name = token_dict["name"].upper()
        self.tokens_dict[token_name] = token_dict

        found = False
        for i, token in enumerate(self.tokens_list):
            if token["key"] == token_dict["key"]:
                self.tokens_list[i] = token_dict
                found = True
                break

        if not found:
            self.tokens_list.append(token_dict)

        self.total_tokens = len(self.tokens_list)
        self.__update_json_file()

    def __update_json_file(self):
        with open(self.JSON_FILE_PATH, 'w') as file: 
            json.dump(self.tokens_dict, file, indent=4)
            