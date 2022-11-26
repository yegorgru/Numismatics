from tkinter import *
from PIL import Image
import io

from Definitions import *


class SearchCollection:
    def __init__(self, controller, collection):
        self.controller = controller
        self.id = collection[0]
        self.text_columns = [collection[1], 'Owner: ' + collection[2], str(collection[3]) + ' coins']
        if collection[4] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = collection[4].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        self.controller.load_search_coins(self.id)
