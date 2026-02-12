import json

class Tokens():
    def __init__(self, json_file_path):
        self.JSON_FILE_PATH = json_file_path
        self.tokens_dict = {}
        self.tokens_list = []
        self.default_token_setup = {}
        self.total_tokens = 0
        try:
            with open(self.JSON_FILE_PATH, 'r') as file: 
                self.tokens_dict = json.load(file)
            self.__setup()
        except FileNotFoundError:
            print("Couldn't find JSON file with player characters!")
        except json.JSONDecodeError:
            print("JSON file with player characters couldn't be decoded!")

    def __setup(self):
        self.default_token_setup = self.tokens_dict["DEFAULT"]
        counter = -1
        for token in self.tokens_dict:
            if(counter != -1):
                self.tokens_list.append(self.tokens_dict[token])
            counter += 1
        self.total_tokens = counter


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

    def create_new_token(self) -> dict:
        default_token = self.tokens_dict["DEFAULT"]
        self.total_tokens += 1
        new_name = "new token"
        new_token = {}
        for field in default_token:
            new_token[field] = default_token[field]
        new_token["name"] = new_name
        new_token["key"] = self.total_tokens
        self.tokens_dict[new_name.upper()] = new_token
        self.__update_json_file()
        return self.tokens_dict[new_name.upper()]

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


    def change_small_field_values(self, token_key, value_key, new_value):
        for token in self.tokens_dict:
            if(self.tokens_dict[token]["key"] == token_key):
                self.tokens_dict[token]["small_fields"][value_key] = new_value
                break
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


    def __update_json_file(self):
        with open(self.JSON_FILE_PATH, 'w') as file: 
            json.dump(self.tokens_dict, file, indent=4)
            