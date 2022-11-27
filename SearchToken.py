from tkinter import *
from PIL import Image
import io

from Definitions import *


class SearchToken:
    def __init__(self, controller, token, is_coin):
        self.controller = controller
        self.id = token[0]
        self.is_coin = is_coin
        if token[4] is None:
            subj = ""
        else:
            subj = token[4]
        self.text_columns = [
            str(token[1]) + ' ' + token[2] + ', ' + str(token[3]), 'Subject: ' + subj, 'Owner: ' + token[5]
        ]
        if token[7] is not None:
            self.text_columns.append('ON SALE')
        else:
            self.text_columns.append('NOT ON SALE')
        if token[6] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        else:
            img = token[6].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        if self.is_coin:
            self.controller.load_search_coin(self.id)
        else:
            self.controller.load_search_banknote(self.id)
