import bcrypt
import urllib
from enum import Enum

import requests

from sqlalchemy import create_engine, Column, Integer, String, select, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker


from PIL import Image  
import io  
import base64

from Enums.TokenTypes import TokenTypes


URL = "hmmmmm, something goes here"

class DatabaseMessages(Enum):
    NONE = -1
    SUCCESS = 0
    EXISTING_USER = 1
    EXISTING_EMAIL = 2
    CRITICAL_ERROR = 3
    INVAL_CREDS = 4
    DUPLICATE = 5
    NO_SESSION_FOUND = 6


class Database:
    def load_all_tokens_with_type(user_id:int, token_type:str):
        url = f"{URL}/load-all-tokens-with-type"
        response = requests.post(url, json={"user_id": user_id, "token_type": token_type})
        json_response = response.json()
        message = json_response["message"]
        if("ERROR" in message or "NONE" in message):
            return {}
        else:
            return eval(json_response["info"])


    def check_user(username:str, password:str):
        url = f"{URL}/check-account"
        response = requests.post(url, json={"username": username, "password": password})
        json_response = response.json()
        message = json_response["message"]
        if("ERROR" in message or "NONE" in message):
            return DatabaseMessages.CRITICAL_ERROR, -1
        elif("INVAL CREDENTIALS" in message):
            return DatabaseMessages.INVAL_CREDS, -1
        else:
            uid = json_response["id"]
            return DatabaseMessages.SUCCESS, uid
    
    def compress_image(image_path, quality=85):  
        with Image.open(image_path) as img:  
            if img.mode in ("RGBA", "P"):  
                img = img.convert("RGB")  
            img_byte_arr = io.BytesIO()  
            img.save(img_byte_arr, format="PNG", quality=quality) 
            return img_byte_arr.getvalue() 

    def update_token_map_asset(user_id:int, token_name:str, image_path:str):
        url = f"{URL}/update-token-map-asset"
        data = None
        with open(image_path, "rb") as img: 
            data = base64.b64encode(img.read()).decode("ascii")
        response = requests.post(url, json={"user_id": user_id, "token_name": token_name, "img_b64": data})
        json_response = response.json()
        message = json_response["message"]

    def update_token_name(user_id:int, old_name:str, new_name:str):
        url = f"{URL}/update-token-name"
        try:
            response = requests.post(url, json={"user_id": user_id, "old_name": old_name, "new_name": new_name})
            json_response = response.json()
            message = json_response["message"]
            if(not "SUCCESS" in message):
                return DatabaseMessages.CRITICAL_ERROR
            return DatabaseMessages.SUCCESS
        except Exception as e:
            #print(f"ERROR: {e}")
            return DatabaseMessages.CRITICAL_ERROR

    def update_token_small_fields(user_id:int, token_name:str, small_fields:dict):
        url = f"{URL}/update-token-small-fields"
        try:
            response = requests.post(url, json={"user_id": user_id, "token_name": token_name, "small_fields": str(small_fields)})
            json_response = response.json()
            message = json_response["message"]
            if(not "SUCCESS" in message):
                return DatabaseMessages.CRITICAL_ERROR
            return DatabaseMessages.SUCCESS
        except Exception as e:
            print(f"ERROR: {e}")
            return DatabaseMessages.CRITICAL_ERROR

    def update_token_large_fields(user_id:int, token_name:str, large_fields:dict):
        url = f"{URL}/update-token-large-fields"
        try:
            response = requests.post(url, json={"user_id": user_id, "token_name": token_name, "large_fields": str(large_fields)})
            json_response = response.json()
            message = json_response["message"]
            if(not "SUCCESS" in message):
                return DatabaseMessages.CRITICAL_ERROR
            return DatabaseMessages.SUCCESS
        except Exception as e:
            print(f"ERROR: {e}")
            return DatabaseMessages.CRITICAL_ERROR

    def add_new_token(user_id:int, user_token_key:int, token_name:str, token_type:str, json_small_fields:dict, json_large_fields:dict, map_asset="", images=[]):
        compressed_images = []
        for img in images:
            compressed_images.append(Database.compress_image(img))

        url = f"{URL}/add-token"
        response = requests.post(url, json={"user_id": user_id, "token_name": token_name, "token_type": token_type, "json_small_fields": str(json_small_fields), "json_large_fields": str(json_large_fields), "images": compressed_images, "map_asset": map_asset})
        json_response = response.json()
        message = json_response["message"]
        if("ERROR" in message or "NONE" in message):
            return DatabaseMessages.CRITICAL_ERROR
        elif("DUPLICATE" in message):
            return DatabaseMessages.DUPLICATE
        else:
            return DatabaseMessages.SUCCESS
        

    def add_host_info_to_db(hostname:str, user_id:int, password:str, port:int):
        url = f"{URL}/add-host"
        response = requests.post(url, json={"hostname": hostname, "user_id": user_id, "password": password, "port": port})
        json_response = response.json()
        message = json_response["message"]

    def add_map_to_db(user_id:int, map_name:str, map_dict:dict):
        url = f"{URL}/add-map"
        response = requests.post(url, json={"user_id": user_id, "map_name": map_name, "map_dict": str(map_dict)})

    def get_map_from_db(user_id:int, map_name:str):
        url = f"{URL}/get-map"
        response = requests.post(url, json={"user_id": user_id, "map_name": map_name})
        json_response = response.json()
        message = json_response["message"]

        if("SUCCESS" in message):
            info = json_response["info"]
            return eval(info)
        return {}

    def create_new_user(username:str, email:str, password:str):
        url = f"{URL}/create-account"
        response = requests.post(url, json={"username": username, "email": email, "password": password})
        json_response = response.json()
        message = json_response["message"]
        if("ERROR" in message):
            return DatabaseMessages.CRITICAL_ERROR, -1
        elif("INVAL CREDENTIALS" in message):
            return DatabaseMessages.INVAL_CREDS, -1
        else:
            uid = json_response["id"]
            return DatabaseMessages.SUCCESS, uid
