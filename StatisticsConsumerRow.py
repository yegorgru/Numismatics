from tkinter import *
from PIL import Image

from Definitions import *


class StatisticsConsumerRow:
    def __init__(self, consumer):
        self.text_columns = [consumer[0], str(consumer[1]), str(consumer[2]), str(consumer[3]), str(consumer[4])]
        self.image = Image.open(PATH_IMAGE_WHITE)

    def click_action(self):
        print('#')