from tkinter import *
from PIL import Image, ImageTk

from Connection import *
from ScrollableFrame import ScrollableFrame
from CollectionManager import CollectionManager
from CreateCollectionWindow import CreateCollectionWindow


class HomePage(Frame):
    def load(self):
        self.username = self.controller.username
        self.profile_name.configure(text=self.username)
        print(self.controller.winfo_screenwidth())
        print(self.controller.winfo_screenheight())
        self.controller.geometry("1920x1080+0+0")
        self.controller.state('zoomed')
        self.load_collections()
        print("Home Page page loaded")

    def load_collections(self):
        self.collections = Frame(self, width=1920, height=800, bg="black")
        self.collections.grid(row=2, column=0, sticky='news')
        self.collections_frame = ScrollableFrame(self.collections, height=800)
        self.collection_manager = CollectionManager(self)
        self.collection_manager.pack_collections(self.collections_frame.scrollable_frame,
                                                 connection.get_collections(self.username), 5)
        self.collections_frame.pack(fill=BOTH)

    def create_new_collection(self):
        new_collection_window = CreateCollectionWindow(self)
        new_collection_window.grab_set()

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.username = ""

        account_frame = Frame(self, width=1920, height=100, bg="#57a1f8")
        account_frame.grid(row=0, column=0, sticky='nw')

        img = Image.open("assets/empty_profile.png")
        img = img.resize((90, 90), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        Label(account_frame, image=self.profile_image, bg='white', borderwidth=0).place(x=5, y=5)

        img2 = (Image.open("assets/settings.png"))
        img2 = img2.resize((70, 70), Image.ANTIALIAS)
        self.settings_image = ImageTk.PhotoImage(img2)
        Label(account_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0).place(x=1445, y=15)

        self.profile_name = Label(
            account_frame, text="", fg='white', bg='#57a1f8',
            font=('Microsoft YaHei UI Light', 24, 'bold')
        )
        self.profile_name.place(x=120, y=25)

        section_buttons_frame = Frame(self, width=1920, height=50, bg="#57a1f8")
        section_buttons_frame.grid(row=1, column=0, sticky='nw')
        self.collections_btn = Button(
            section_buttons_frame, width=30, text='Collections', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_collections()
        )
        self.collections_btn.grid(row=0, column=0)
        self.deals_btn = Button(
            section_buttons_frame, width=30, text='Deals', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_collections()
        )
        self.deals_btn.grid(row=0, column=1)

        self.collections = None
        self.collections_frame = None
        self.collection_manager = None




