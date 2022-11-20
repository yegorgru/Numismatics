from tkinter import *
from PIL import Image, ImageTk
import io
from enum import Enum

from Definitions import *


class TokenType(Enum):
    CREATE_NEW = 1,
    TOKEN = 2


class TokenPreview:
    def __init__(self, controller, token, token_type=TokenType.TOKEN):
        self.controller = controller
        self.token_type = token_type
        if token_type == TokenType.CREATE_NEW:
            self.image = Image.open(PATH_IMAGE_CREATE)
            self.text = token[0]
            self.id = None
        else:
            self.id = token[0]
            self.text = str(token[1]) + ' ' + token[2] + ', ' + str(token[3])
            if token[4] is None:
                self.image = Image.open(PATH_IMAGE_EMPTY)
            else:
                img = token[4].read()
                pre_img = io.BytesIO(img)
                self.image = Image.open(pre_img)

    def click_action(self):
        if self.token_type == TokenType.CREATE_NEW:
            self.controller.create_new_coin()
        else:
            self.controller.load_coin(self.id)




