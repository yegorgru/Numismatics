from tkinter import *
from PIL import Image
import io

from Definitions import *


class DealPreview:
    def __init__(self, controller, deal):
        # 5: cd.price, 6: cd.date_end
        self.controller = controller
        self.id = deal[0]
        self.text_columns = [str(deal[1]) + ' ' + deal[2] + ', ' + str(deal[3])]
        if deal[4] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = deal[4].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        self.controller.load_deal(self.id)




