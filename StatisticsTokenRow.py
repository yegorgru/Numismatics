from tkinter import *
from PIL import Image
import io

from Definitions import *


class StatisticsTokenRow:
    def __init__(self, token, is_heading=False):
        self.text_columns = [token[1], str(token[2]), str(token[3])]
        if is_heading:
            self.image = Image.open(PATH_IMAGE_WHITE)
        elif token[0] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = token[0].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        print('#')