from tkinter import *
from PIL import Image
import io

from Definitions import *


class SearchUser:
    def __init__(self, controller, user):
        self.controller = controller
        self.id = user[0]
        self.text_columns = [user[1], str(user[2]) + ' coins']
        if user[3] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        else:
            img = user[3].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)

    def click_action(self):
        self.controller.load_search_user(self.id)
