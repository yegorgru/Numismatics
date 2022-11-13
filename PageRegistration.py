from Connection import *
from GUI.EntryWithPlaceholder import *

from Definitions import *


class PageRegistration(Frame):
    def register(self):
        register_code = connection.create_user(
            self.username_entry.get(), self.email_entry.get(), self.password_entry.get()
        )
        print(register_code)

    def load(self):
        print("Register page loaded")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller

        self.img = PhotoImage(file=PATH_IMAGE_LOGIN)
        Label(self, image=self.img, bg='white').place(x=50, y=50)

        frame = Frame(self, width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        heading = Label(frame, text='Register', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=0)

        self.username_entry = EntryWithPlaceholder(frame, "username")
        self.username_entry.place(x=30, y=70)
        Frame(frame, width=315, height=2, bg='black').place(x=25, y=97)

        self.email_entry = EntryWithPlaceholder(frame, "email")
        self.email_entry.place(x=30, y=130)
        Frame(frame, width=315, height=2, bg='black').place(x=25, y=157)

        self.password_entry = EntryWithPlaceholder(frame, "password", True)
        self.password_entry.place(x=30, y=190)
        Frame(frame, width=315, height=2, bg='black').place(x=25, y=217)

        self.register_btn = Button(
            frame, width=30, pady=7, text='Register', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.register()
        )
        self.register_btn.place(x=33, y=244)
        self.label = Label(
            frame, text="Already have an account?", fg='black', bg='white',
            font=('Microsoft YaHei UI Light', 9)
        )
        self.label.place(x=50, y=310)

        self.login_btn = Button(
            frame, width=5, text="Login", border=0, bg='white', cursor='hand2', fg='#57a1f8',
            command=lambda: controller.show_frame("PageLogin")
        )
        self.login_btn.place(x=230, y=310)