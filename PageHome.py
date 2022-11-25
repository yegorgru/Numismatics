from Connection import *
from WindowCollectionCreateEdit import WindowCollectionCreateEdit
from GUI.GridManager import GridManager
from CollectionPreview import *
from WindowMode import WindowMode
from PIL import Image, ImageTk
from tkinter import ttk
from DealPreview import DealPreview
from GUI.ListManager import ListManager
from WindowCoinDeal import WindowCoinDeal


class PageHome(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.username = ""

        account_frame = Frame(self, width=1920, height=100, bg="#57a1f8")
        account_frame.grid(row=0, column=0, sticky='nw')

        img = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        img = img.resize((90, 90), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        Label(account_frame, image=self.profile_image, bg='white', borderwidth=0).place(x=5, y=5)

        img2 = (Image.open(PATH_IMAGE_SETTINGS))
        img2 = img2.resize((70, 70), Image.ANTIALIAS)
        self.settings_image = ImageTk.PhotoImage(img2)
        Label(account_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0).place(x=1645, y=15)

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
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_deals()
        )
        self.deals_btn.grid(row=0, column=1)

        self.collections = None
        self.collections_frame = None
        self.collection_manager = None

        self.deals_var = StringVar()
        self.deals_combobox = ttk.Combobox(self, width=40, textvariable=self.deals_var, state='readonly')
        self.deals_combobox.configure(values=('Active deals', 'Previous deals'))
        self.deals_combobox.current(0)
        self.deals_combobox.grid(row=3, column=0, pady=(20, 20), sticky="w")
        self.deals_combobox.grid_remove()
        self.deals_var.trace('w', self.load_deals)
        self.deals = None

    def load(self):
        self.username = self.controller.username
        self.profile_name.configure(text=self.username)
        self.controller.geometry("1920x1080+0+0")
        self.controller.state('zoomed')
        self.load_collections()
        print("Home Page page loaded")

    def load_collections(self):
        if self.collections is not None:
            self.collections.grid_remove()
        self.deals_combobox.grid_remove()
        if self.deals is not None:
            self.deals.grid_remove()
        rs = connection.get_collections_preview(self.username)
        collections = [
            CollectionPreview(self, ("New collection", None, None), CollectionType.CREATE_NEW)
        ]
        for collection in rs:
            collections.append(CollectionPreview(self, collection, CollectionType.COLLECTION))

        self.collections = GridManager(
            self, column_count=7, row_width=200, column_width=200, width=1920, height=800, objects=collections
        )
        self.collections.grid(row=2, column=0, sticky='news')

    def load_deals(self, *args):
        if self.collections is not None:
            self.collections.grid_remove()
        self.deals_combobox.grid()
        if self.deals is not None:
            self.deals.grid_remove()
        rs = connection.get_user_deals_preview(self.username, self.deals_var.get() == 'Active deals')
        print(rs)
        deals = list()
        for deal in rs:
            deals.append(DealPreview(self, deal))

        self.deals = ListManager(
            self, row_width=200, width=1920, height=750, objects=deals
        )
        self.deals.grid(row=4, column=0, sticky='news')

    def create_new_collection(self):
        new_collection_window = WindowCollectionCreateEdit(self, WindowMode.CREATE_NEW)
        new_collection_window.grab_set()

    def load_collection(self, collection_id):
        self.controller.collection_id = collection_id
        self.controller.show_frame("PageCollection")

    def load_deal(self, coin_id):
        deal_window = WindowCoinDeal(self, coin_id)
        deal_window.grab_set()

    def after_w_coin_deal(self, *args):
        self.load_deals()






