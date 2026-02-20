
from Enums.TokenTypes import TokenTypes

class TokenRecord():
    def __init__(self, token_dict:dict, position:tuple, token_type:TokenTypes, record_key:int):
        self.token_dict = token_dict
        self.position = position
        self.record_key = record_key
        self.token_type = token_type
        self.name = self.token_dict["name"]

    def get_record_key(self) -> int:
        return self.record_key
        
    def get_position(self) -> tuple:
        return self.position

    def get_x_position(self) -> float:
        return self.position.x

    def get_y_position(self) -> float:
        return self.position.y

    def get_token_name(self) -> str:
        return self.name

    def get_token_type(self) -> TokenTypes:
        return self.token_type


        