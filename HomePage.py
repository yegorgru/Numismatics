from tkinter import *
from PIL import Image, ImageTk

from Connection import *
from EntryWithPlaceholder import *


class HomePage(Frame):
    def load(self):
        self.profile_name.configure(text=self.controller.username)
        self.controller.state('zoomed')
        self.controller.geometry("1920x1080+0+0")
        print("Home Page page loaded")

    def load_collections(self):
        print("loading collections")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller
        account_frame = Frame(self, width=1920, height=100, bg="#57a1f8")
        account_frame.place(x=0, y=0)

        img = (Image.open("assets/empty_profile.png"))
        img = img.resize((90, 90), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        Label(account_frame, image=self.profile_image, bg='white', borderwidth=0).place(x=5, y=5)

        img2 = (Image.open("assets/output-onlinepngtools.png"))
        img2 = img2.resize((70, 70), Image.ANTIALIAS)
        self.settings_image = ImageTk.PhotoImage(img2)
        Label(account_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0).place(x=1445, y=15)

        self.profile_name = Label(
            account_frame, text="", fg='white', bg='#57a1f8',
            font=('Microsoft YaHei UI Light', 24, 'bold')
        )
        self.profile_name.place(x=120, y=25)

        self.collections_btn = Button(
            self, width=30, pady=7, text='Login', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.load_collections()
        )
        self.collections_btn.place(x=5, y=105)



