from PyQt6.QtWidgets import (
    QMainWindow
)

from Toolbox import Toolbox
from Enums.TokenTypes import TokenTypes


class CustomTokenExploreWindow(QMainWindow):
    def __init__(self, toolbox_ref:Toolbox, token_set_type:TokenTypes):
        super().__init__()
        self.title = TokenTypes.get_str_from_token_type(token_set_type) + " Token Page"

        self.setWindowTitle(self.title)