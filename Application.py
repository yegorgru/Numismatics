from tkinter import *
import ctypes

from PageRegistration import PageRegistration
from PageLogin import PageLogin
from PageHome import PageHome
from PageCollection import PageCollection

ctypes.windll.shcore.SetProcessDpiAwareness(2)  # for correct work on Windows with different display settings


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title('Login')
        self.geometry('925x500+300+200')
        self.configure(bg="#fff")
        self.resizable(False, False)

        self.frames = {}
        for F in (PageLogin, PageRegistration, PageHome, PageCollection):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageLogin")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.load()


