from tkinter import filedialog as fd
import io
from PIL import Image
import os

from Definitions import *


def open_image(title='Open a file'):
    filetypes = (
        ('JPG', '*.jpg'),
        ('PNG', '*.png')
    )

    return fd.askopenfilename(
        title=title,
        initialdir='/',
        filetypes=filetypes)


def tuple_list_to_tuple(tuple_list):
    tup = tuple()
    for i in tuple_list:
        tup += tuple(i)
    return tup


def tuple_with_delimiter(tuple_list, delimiter):
    tup = tuple()
    for i in tuple_list:
        s = str()
        for j in i:
            s += str(j) + delimiter
        s = s[:len(s) - len(delimiter)]
        tup += (s, )
    return tup


def image_from_blob(blob):
    img = blob.read()
    pre_img = io.BytesIO(img)
    return Image.open(pre_img)


def get_general_image_bytes():
    file = open(PATH_IMAGE_COLLECTION_GENERAL, 'rb')
    file = io.BytesIO(file.read())
    file.seek(0, os.SEEK_END)
    return file.getvalue()


