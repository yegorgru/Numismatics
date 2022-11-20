from tkinter import filedialog as fd
import io
from PIL import Image


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
