from tkinter import *
from PIL import Image
import io

from Definitions import *


class StatisticsConsumerRow:
    def __init__(self, consumer, is_heading=False):
        self.text_columns = [consumer[1], str(consumer[2]), str(consumer[3]), str(consumer[4]), str(consumer[5])]
        if is_heading:
            self.image = Image.open(PATH_IMAGE_WHITE)
        elif consumer[0] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        else:
            img = consumer[0].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        print('#')