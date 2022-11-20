from tkinter import *
from PIL import Image
import io
from enum import Enum

from Definitions import *


class CollectionType(Enum):
    CREATE_NEW = 1,
    COLLECTION = 2


class CollectionPreview:
    def __init__(self, controller, collection, collection_type=CollectionType.COLLECTION):
        self.controller = controller
        self.collection_type = collection_type
        if collection_type == CollectionType.CREATE_NEW:
            self.image = Image.open(PATH_IMAGE_CREATE)
        elif collection[1] is None:
            self.image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = collection[1].read()
            pre_img = io.BytesIO(img)
            self.image = Image.open(pre_img)
        self.text = collection[0]
        self.id = collection[2]

    def click_action(self):
        if self.collection_type == CollectionType.CREATE_NEW:
            self.controller.create_new_collection()
        else:
            self.controller.load_collection(self.id)




