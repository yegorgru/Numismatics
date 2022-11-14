from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import io
import os

from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from GUI.TextWithPlaceholder import TextWithPlaceholder
from Connection import *
from Utils import *
from Definitions import *


class WindowCoinCreate(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.controller = controller
        self.username = controller.username

        self.title('New coin')
        self.geometry('1600x800+200+100')
        self.resizable(False, False)
        self.configure(bg="white")

        self.value_entry = EntryWithPlaceholder(self, "Value")
        self.value_entry.grid(row=0, column=1, sticky="w", pady=(20, 0))
        br = Frame(self, width=400, height=2, bg='black')
        br.grid(row=1, column=1, sticky="w", pady=(0, 20))

        self.currency_entry = EntryWithPlaceholder(self, "Currency")
        self.currency_entry.grid(row=2, column=1, sticky="w", pady=(20, 0))
        br2 = Frame(self, width=400, height=2, bg='black')
        br2.grid(row=3, column=1, sticky="w", pady=(0, 20))

        self.year_entry = EntryWithPlaceholder(self, "Year")
        self.year_entry.grid(row=4, column=1, sticky="w", pady=(20, 0))
        br3 = Frame(self, width=400, height=2, bg='black')
        br3.grid(row=5, column=1, sticky="w", pady=(0, 20))

        self.subject = TextWithPlaceholder(self, placeholder="Subject", width=40, height=3)
        self.subject.grid(column=1, row=5, rowspan=4, sticky="w", pady=(20, 20))
        br15 = Frame(self, width=400, height=2, bg='black')
        br15.grid(row=9, column=1, sticky="w", pady=(0, 20))

        img = Image.open(PATH_IMAGE_EMPTY)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.coin_image = Label(self, image=self.image, bg='white', borderwidth=0)
        self.coin_image.grid(row=10, column=1, sticky="w", pady=(20, 20))
        self.image_value = None

        self.diameter_entry = EntryWithPlaceholder(self, "Diameter")
        self.diameter_entry.grid(row=0, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br7 = Frame(self, width=400, height=2, bg='black')
        br7.grid(row=1, column=2, padx=(20, 20), pady=(0, 20))

        self.weight_entry = EntryWithPlaceholder(self, "Weight")
        self.weight_entry.grid(row=2, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br8 = Frame(self, width=400, height=2, bg='black')
        br8.grid(row=3, column=2, padx=(20, 20), pady=(0, 20))

        self.material_var = StringVar()
        self.material_combobox = ttk.Combobox(self, width=40,  textvariable=self.material_var)
        rs = connection.get_material_names()
        self.material_combobox.configure(values=tuple_list_to_tuple(rs))
        self.material_combobox.current(0)
        self.material_combobox.grid(row=4, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br5 = Frame(self, width=400, height=2, bg='white')
        br5.grid(row=5, column=2, padx=(20, 20), pady=(0, 20))

        self.type_var = StringVar()
        self.type_combobox = ttk.Combobox(self, width=40,  textvariable=self.type_var)
        rs = connection.get_token_types()
        self.type_combobox.configure(values=tuple_list_to_tuple(rs))
        self.type_combobox.current(0)
        self.type_combobox.grid(row=6, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br6 = Frame(self, width=400, height=2, bg='white')
        br6.grid(row=7, column=2, padx=(20, 20), pady=(0, 20))

        self.edge_var = StringVar()
        self.edge_combobox = ttk.Combobox(self, width=40, textvariable=self.edge_var)
        rs = connection.get_edge_types()
        self.edge_combobox.configure(values=tuple_list_to_tuple(rs))
        self.edge_combobox.current(0)
        self.edge_combobox.grid(row=8, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br9 = Frame(self, width=400, height=2, bg='white')
        br9.grid(row=9, column=2, padx=(20, 20), pady=(0, 20))

        frame_btn = Frame(self, bg="white", width=400, height=100)
        frame_btn.grid(row=10, column=3)
        self.add_btn = Button(
            frame_btn, width=30, pady=7, text='Create', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.create()
        )
        self.add_btn.grid(row=0, column=1, sticky="w", pady=(20, 20))
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)

        self.description = TextWithPlaceholder(self, placeholder="Description", width=40, height=5)
        self.description.grid(column=3, row=0, rowspan=5, sticky="w", pady=(0, 20))
        br4 = Frame(self, width=400, height=2, bg='black')
        br4.grid(row=5, column=3, sticky="w", pady=(0, 20))

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.coin_image.bind("<Button-1>", self.set_image)

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
        self.coin_image.configure(image=self.image)
        file = open(file, 'rb')
        file = io.BytesIO(file.read())
        file.seek(0, os.SEEK_END)
        self.image_value = file.getvalue()

