from tkinter import *
from PIL import Image
import io

from Definitions import *


class PreviewDeal:
    def __init__(self, controller, deal, is_active, is_coin):
        self.controller = controller
        self.is_active = is_active
        self.id = deal[0]
        self.is_coin = is_coin
        if deal[1] is None:
            heading = 'Token was deleted by owner'
        else:
            heading = str(deal[1]) + ' ' + deal[2] + ', ' + str(deal[3])
        self.text_columns = [
            heading, str(deal[5]) + ' $', 'Date: ' + str(deal[6])
        ]
        if not is_active:
            self.text_columns.append('Seller: ' + deal[7])
            self.text_columns.append('Buyer: ' + deal[8])
        if deal[4] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = deal[4].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        if self.is_active:
            if self.is_coin:
                self.controller.load_coin_deal(self.id)
            else:
                self.controller.load_banknote_deal(self.id)




