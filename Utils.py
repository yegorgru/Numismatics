from tkinter import filedialog as fd


def open_image():
    filetypes = (
        ('JPG', '*.jpg'),
        ('PNG', '*.png')
    )

    return fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)


def tuple_list_to_tuple(tuple_list):
    tup = tuple()
    for i in tuple_list:
        tup += tuple(i)
    return tup
