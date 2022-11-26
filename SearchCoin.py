from tkinter import *
from PIL import Image
import io

from Definitions import *


class SearchCoin:
    def __init__(self, controller, coin):
        self.controller = controller
        self.id = coin[0]
        if coin[4] is None:
            subj = ""
        else:
            subj = coin[4]
        self.text_columns = [
            str(coin[1]) + ' ' + coin[2] + ', ' + str(coin[3]), 'Subject: ' + subj, 'Owner: ' + coin[5]
        ]
        if coin[6] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        else:
            img = coin[6].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        self.controller.load_search_coin(self.id)
