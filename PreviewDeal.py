from tkinter import *
from PIL import Image
import io

from Definitions import *


class PreviewDeal:
    def __init__(self, controller, deal, is_active):
        self.controller = controller
        self.is_active = is_active
        self.id = deal[0]
        self.text_columns = [
            str(deal[1]) + ' ' + deal[2] + ', ' + str(deal[3]), str(deal[5]) + ' $', 'Date: ' + str(deal[6])
        ]
        if not is_active:
            self.text_columns.append('Buyer: ' + deal[7])
        if deal[4] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = deal[4].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        if self.is_active:
            self.controller.load_deal(self.id)




