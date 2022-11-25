from tkinter import *
from PIL import Image, ImageTk

from GUI.ScrollableFrame import ScrollableFrame


class FrameListCell(Frame):
    def click_slot(self, e):
        self.object.click_action()

    def __init__(self, parent, obj, width=200, height=200):
        Frame.__init__(self, parent, bg="white", width=width, height=height)
        self.object = obj

        img = obj.image.resize((int(height*0.75), int(height*0.75)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.img_label = Label(self, image=self.image, bg='white', borderwidth=5)
        self.img_label.grid(row=0, column=0)

        self.text_columns = obj.text_columns
        self.heading = Label(self, width=20,  text=self.text_columns[0], fg='black', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.heading.grid(row=0, column=1)

        self.bind("<Button-1>", self.click_slot)
        self.img_label.bind("<Button-1>", self.click_slot)
        self.heading.bind("<Button-1>", self.click_slot)


class ListManager(Frame):
    def __init__(self, parent, row_width, height, width, objects):
        Frame.__init__(self, parent, bg="white", width=width, height=height)
        self.scrollable_frame = ScrollableFrame(self, height=height)
        for obj in objects:
            FrameListCell(
                self.scrollable_frame.scrollable_frame, height=row_width, width=width, obj=obj
            ).pack()
        self.scrollable_frame.pack(fill=BOTH)