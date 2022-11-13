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