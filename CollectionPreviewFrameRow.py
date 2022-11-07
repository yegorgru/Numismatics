from tkinter import *

from CollectionPreviewFrame import CollectionPreviewFrame


class CollectionPreviewFrameRow(Frame):
    def __init__(self, parent, controller, collections):
        Frame.__init__(self, parent, bg="white", width=1000, height=200)
        self.controller = controller
        self.configure(bg="yellow")

        for i in range(len(collections)):
            collection = CollectionPreviewFrame(self, controller, collections[i])
            collection.grid(row=0, column=i)

