from tkinter import *
from PIL import Image, ImageTk

from GUI.ScrollableFrame import ScrollableFrame


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


class FrameCell(Frame):
    def click_slot(self, e):
        self.object.click_action()

    def __init__(self, parent, object, width=200, height=200):
        Frame.__init__(self, parent, bg="white", width=width, height=height)
        self.object = object
        img = object.image.resize((int(width*0.75), int(height*0.75)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.img_label = Label(self, image=self.image, bg='white', borderwidth=0)
        self.img_label.grid(row=0, column=0)
        self.heading = Label(self, width=20,  text=object.text, fg='black', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.heading.grid(row=1, column=0)

        self.bind("<Button-1>", self.click_slot)
        self.img_label.bind("<Button-1>", self.click_slot)
        self.heading.bind("<Button-1>", self.click_slot)


class RowManager(Frame):
    def __init__(self, parent, objects, row_width=200, column_width=200):
        Frame.__init__(self, parent, bg="white", width=column_width * len(objects), height=row_width)
        for i in range(len(objects)):
            cell = FrameCell(self, object=objects[i], width=column_width, height=row_width)
            cell.grid(row=0, column=i)


class GridManager(Frame):
    def __init__(self, parent, column_count, row_width, column_width, height, width, objects):
        Frame.__init__(self, parent, bg="white", width=width, height=height)
        self.scrollable_frame = ScrollableFrame(self, height=height)
        for row in chunker(objects, column_count):
            RowManager(self.scrollable_frame.scrollable_frame, row_width=row_width, column_width=column_width, objects=row).pack()
        self.scrollable_frame.pack(fill=BOTH)
