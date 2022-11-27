from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno, showinfo, showwarning

from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from Connection import *
from Utils import *
from Definitions import *


class WindowConsumerEdit(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)

        self.controller = controller

        self.title('Edit user info')
        self.geometry('500x750+300+100')
        self.resizable(False, False)
        self.configure(bg="white")

        img = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.profile_image = Label(self, image=self.image, bg='white', borderwidth=0)
        self.profile_image.grid(row=0, column=1, sticky="w", pady=(20, 20))
        self.image_value = None

        self.name_entry = EntryWithPlaceholder(self, "Collection name")
        self.name_entry.grid(row=1, column=1, sticky="w", pady=(20, 0))
        br = Frame(self, width=400, height=2, bg='black')
        br.grid(row=2, column=1, sticky="w", pady=(0, 20))

        self.email_entry = EntryWithPlaceholder(self, "Email", width=30)
        self.email_entry.grid(row=3, column=1, sticky="w", pady=(20, 0))
        br2 = Frame(self, width=400, height=2, bg='black')
        br2.grid(row=4, column=1, sticky="w", pady=(0, 20))

        self.password_entry = EntryWithPlaceholder(self, "Password")
        self.password_entry.grid(row=5, column=1, sticky="w", pady=(20, 0))
        br3 = Frame(self, width=400, height=2, bg='black')
        br3.grid(row=6, column=1, sticky="w", pady=(0, 20))

        frame_btn = Frame(self, bg="white", width=400, height=200)
        frame_btn.grid(row=7, column=1)
        self.save_btn = Button(
            frame_btn, width=30, pady=7, text='Save', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.save()
        )
        self.save_btn.grid(row=1, column=1, sticky="w", pady=(20, 20))
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.profile_image.bind("<Button-1>", self.set_image)
        self.consumer_id = None
        self.load()

    def save(self):
        name = self.name_entry.get_text()
        email = self.email_entry.get_text()
        password = self.password_entry.get_text()
        if connection.update_consumer(name, email, password, self.image_value, self.consumer_id) != UserCode.SUCCESS:
            print()
            showwarning("Incorrect update info operation", "Incorrect input recognised!")
        else:
            self.controller.username = name
            self.controller.controller.username = name
            self.controller.load_consumer_info()
            self.destroy()

    def set_image(self, e):
        file = open_image()
        if not file:
            return
        img = Image.open(file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.profile_image.configure(image=self.image)
        file = open(file, 'rb')
        file = io.BytesIO(file.read())
        file.seek(0, os.SEEK_END)
        self.image_value = file.getvalue()

    def load(self):
        rs = connection.get_consumer(self.controller.username)
        self.name_entry.set_text(rs[0])
        self.email_entry.set_text(rs[1])
        self.password_entry.set_text(rs[2])
        if rs[3] is not None:
            img = rs[3].read()
            pre_img = io.BytesIO(img)
            img = Image.open(pre_img)
            img = img.resize((400, 400), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(img)
            self.profile_image.configure(image=self.image)
        self.consumer_id = rs[4]
