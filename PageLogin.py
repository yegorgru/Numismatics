from Connection import *
from GUI.EntryWithPlaceholder import *

from Definitions import *

class PageLogin(Frame):
    def login(self):
        user = self.user_entry.get()
        password = self.password_entry.get()
        login_result = connection.user_exist(user, password)
        if login_result[0]:
            self.controller.username = login_result[1]
            self.controller.show_frame("PageHome")
        else:
            print("Fail")

    def load(self):
        print("Login page loaded")

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller

        self.img = PhotoImage(file=PATH_IMAGE_LOGIN)
        Label(self, image=self.img, bg='white').place(x=50, y=50)

        frame = Frame(self, width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        heading = Label(frame, text='Login', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.user_entry = EntryWithPlaceholder(frame, "username / email")
        self.user_entry.place(x=30, y=80)
        Frame(frame, width=315, height=2, bg='black').place(x=25, y=107)

        self.password_entry = EntryWithPlaceholder(frame, "password", True)
        self.password_entry.place(x=30, y=140)
        Frame(frame, width=315, height=2, bg='black').place(x=25, y=167)

        self.login_btn = Button(
            frame, width=30, pady=7, text='Login', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.login()
        )
        self.login_btn.place(x=33, y=194)
        self.label = Label(
            frame, text="Don't have an account?", fg='black', bg='white',
            font=('Microsoft YaHei UI Light', 9)
        )
        self.label.place(x=60, y=260)

        self.register_btn = Button(
            frame, width=8, text="Register", border=0, bg='white', cursor='hand2', fg='#57a1f8',
            command=lambda: controller.show_frame("PageRegistration")
        )
        self.register_btn.place(x=225, y=260)