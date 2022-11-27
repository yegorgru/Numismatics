from Connection import *
from WindowCoinCreateEditSearch import WindowCoinCreateEditSearch
from WindowBanknoteCreateEditSearch import WindowBanknoteCreateEditSearch
from GUI.GridManager import GridManager
from PreviewToken import *
import textwrap

from WindowCollectionCreateEdit import WindowCollectionCreateEdit
from WindowMode import WindowMode


class PageCollection(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="white")
        self.controller = controller
        self.username = ""
        self.collection_id = -100

        collection_frame = Frame(self, width=1920, height=350, bg="#57a1f8")
        collection_frame.grid(row=0, column=0, sticky='nw')

        img = Image.open(PATH_IMAGE_EMPTY)
        img = img.resize((300, 300), Image.ANTIALIAS)
        self.collection_image = ImageTk.PhotoImage(img)
        self.collection_image_label = Label(collection_frame, image=self.collection_image, bg='white', borderwidth=0)
        self.collection_image_label.place(x=25, y=25)

        img2 = (Image.open(PATH_IMAGE_SETTINGS))
        img2 = img2.resize((70, 70), Image.ANTIALIAS)
        self.settings_image = ImageTk.PhotoImage(img2)
        self.settings_img = Label(collection_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0)
        self.settings_img.place(x=1645, y=30)
        self.settings_img.bind("<Button-1>", self.edit_collection)

        img3 = (Image.open(PATH_IMAGE_BACK_BUTTON))
        img3 = img3.resize((100, 100), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(img3)
        self.back_img = Label(collection_frame, image=self.back_image, bg="#57a1f8", borderwidth=0)
        self.back_img.place(x=1720, y=15)
        self.back_img.bind("<Button-1>", self.close)

        self.collection_name = Label(
            collection_frame, text="", fg='white', bg='#57a1f8',
            font=('Microsoft YaHei UI Light', 24, 'bold')
        )
        self.collection_name.place(x=470, y=30)

        self.collection_description = Label(
            collection_frame, text="", fg='white', bg='#57a1f8', justify=LEFT,
            font=('Microsoft YaHei UI Light', 16, 'bold')
        )
        self.collection_description.place(x=470, y=120)

        section_buttons_frame = Frame(self, width=1920, height=50, bg="#57a1f8")
        section_buttons_frame.grid(row=1, column=0, sticky='nw')
        self.coins_btn = Button(
            section_buttons_frame, width=30, text='Coins', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_coins()
        )
        self.coins_btn.grid(row=0, column=0)
        self.banknotes_btn = Button(
            section_buttons_frame, width=30, text='Banknotes', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_banknotes()
        )
        self.banknotes_btn.grid(row=0, column=1)

        self.tokens = None
        self.coins_frame = None
        self.coins_manager = None

    def load(self):
        self.load_collection_info()
        self.load_coins()
        print("Collection Page page loaded")

    def load_collection_info(self):
        self.collection_id = self.controller.collection_id
        info = connection.get_collection(collection_id=self.collection_id)
        self.collection_name.configure(text=info[0])

        if info[1] is not None:
            self.collection_description.configure(text=textwrap.fill(info[1], 60))

        if info[2] is None:
            self.collection_image = Image.open(PATH_IMAGE_EMPTY)
        else:
            img = info[2].read()
            pre_img = io.BytesIO(img)
            self.collection_image = Image.open(pre_img)
        self.collection_image = self.collection_image.resize((300, 300), Image.ANTIALIAS)
        self.collection_image = ImageTk.PhotoImage(self.collection_image)
        self.collection_image_label.configure(image=self.collection_image)

    def load_coins(self):
        rs = connection.get_coins_preview(self.collection_id)
        coins = [
            PreviewToken(self, ("New coin",), TokenType.CREATE_NEW_COIN)
        ]
        for coin in rs:
            coins.append(PreviewToken(self, coin, TokenType.COIN))

        self.tokens = GridManager(
            self, column_count=7, row_width=200, column_width=200, width=1920, height=630, objects=coins
        )
        self.tokens.grid(row=2, column=0, sticky='news')

    def close(self, e):
        self.controller.show_frame("PageHome")

    def load_banknotes(self):
        rs = connection.get_banknotes_preview(self.collection_id)
        banknotes = [
            PreviewToken(self, ("New banknote",), TokenType.CREATE_NEW_BANKNOTE)
        ]
        for banknote in rs:
            banknotes.append(PreviewToken(self, banknote, TokenType.BANKNOTE))

        self.tokens = GridManager(
            self, column_count=5, row_width=200, column_width=350, width=1920, height=630, objects=banknotes
        )
        self.tokens.grid(row=2, column=0, sticky='news')

    def create_new_coin(self):
        new_coin_window = WindowCoinCreateEditSearch(self, window_mode=WindowMode.CREATE_NEW)
        new_coin_window.grab_set()

    def create_new_banknote(self):
        new_banknote_window = WindowBanknoteCreateEditSearch(self, window_mode=WindowMode.CREATE_NEW)
        new_banknote_window.grab_set()

    def load_coin(self, coin_id):
        coin_window = WindowCoinCreateEditSearch(self, window_mode=WindowMode.VIEW, coin_id=coin_id)
        coin_window.grab_set()

    def load_banknote(self, banknote_id):
        banknote_window = WindowBanknoteCreateEditSearch(self, window_mode=WindowMode.VIEW, banknote_id=banknote_id)
        banknote_window.grab_set()

    def edit_collection(self, e):
        edit_window = WindowCollectionCreateEdit(self, WindowMode.EDIT)
        edit_window.grab_set()
        self.load()

