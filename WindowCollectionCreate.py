from tkinter import *
from PIL import Image, ImageTk
import io
import os

from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from GUI.TextWithPlaceholder import TextWithPlaceholder
from Connection import *
from GUI.Utils import *
from Definitions import *


class WindowCollectionCreate(Toplevel):
    def create(self):
        connection.create_collection(
            self.username, self.name_entry.get(), self.description.get_text(), self.image_value
        )
        self.controller.load_collections()
        self.destroy()

    def set_image(self, e):
        file = open_image()
        if not file:
            return
        img = Image.open(file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.collection_image.configure(image=self.image)
        file = open(file, 'rb')
        file = io.BytesIO(file.read())
        file.seek(0, os.SEEK_END)
        self.image_value = file.getvalue()

    def __init__(self, controller):
        Toplevel.__init__(self)
        self.controller = controller
        self.username = controller.username

        self.title('New collection')
        self.geometry('500x800+300+100')
        self.resizable(False, False)
        self.configure(bg="white")

        img = Image.open(PATH_IMAGE_EMPTY)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.collection_image = Label(self, image=self.image, bg='white', borderwidth=0)
        self.collection_image.grid(row=0, column=1, sticky="w", pady=(20, 20))
        self.image_value = None

        self.name_entry = EntryWithPlaceholder(self, "Collection name")
        self.name_entry.grid(row=1, column=1, sticky="w", pady=(20, 0))

        br = Frame(self, width=400, height=2, bg='black')
        br.grid(row=2, column=1, sticky="w", pady=(0, 20))

        self.description = TextWithPlaceholder(self, placeholder="Description", width=40, height=5)
        self.description.grid(column=1, row=3, sticky="w", pady=(20, 0))

        br2 = Frame(self, width=400, height=2, bg='black')
        br2.grid(row=4, column=1, sticky="w", pady=(0, 20))

        frame_btn = Frame(self, bg="white", width=400, height=100)
        frame_btn.grid(row=5, column=1)
        self.add_btn = Button(
            frame_btn, width=30, pady=7, text='Create', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.create()
        )
        self.add_btn.grid(row=0, column=1, sticky="w", pady=(20, 20))
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.collection_image.bind("<Button-1>", self.set_image)



