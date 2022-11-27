from Connection import *
from WindowCollectionCreateEdit import WindowCollectionCreateEdit
from GUI.GridManager import GridManager
from PreviewCollection import *
from WindowMode import WindowMode
from PIL import Image, ImageTk
from tkinter import ttk
from PreviewDeal import PreviewDeal
from GUI.ListManager import ListManager
from WindowTokenDeal import WindowTokenDeal
from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from SearchUser import SearchUser
from SearchCollection import SearchCollection
from SearchToken import SearchToken
from WindowCoinCreateEditSearch import WindowCoinCreateEditSearch
from WindowBanknoteCreateEditSearch import WindowBanknoteCreateEditSearch
from WindowConsumerEdit import WindowConsumerEdit


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
        self.profile_img = Label(account_frame, image=self.profile_image, bg='white', borderwidth=0)
        self.profile_img.place(x=5, y=5)

        img2 = (Image.open(PATH_IMAGE_SETTINGS))
        img2 = img2.resize((70, 70), Image.ANTIALIAS)
        self.settings_image = ImageTk.PhotoImage(img2)
        self.settings_img = Label(account_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0)
        self.settings_img.place(x=1645, y=15)
        self.settings_img.bind("<Button-1>", self.edit_user)

        img3 = (Image.open(PATH_IMAGE_BACK_BUTTON))
        img3 = img3.resize((100, 100), Image.ANTIALIAS)
        self.back_image = ImageTk.PhotoImage(img3)
        self.back_img = Label(account_frame, image=self.back_image, bg="#57a1f8", borderwidth=0)
        self.back_img.place(x=1720, y=0)
        self.back_img.bind("<Button-1>", self.close)

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
            section_buttons_frame, width=30, text='My deals', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.load_deals()
        )
        self.deals_btn.grid(row=0, column=1)
        self.search_page_btn = Button(
            section_buttons_frame, width=30, text='Search', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.show_search_tab()
        )
        self.search_page_btn.grid(row=0, column=2)

        self.collections = None
        self.collections_frame = None
        self.collection_manager = None

        self.deals_var = StringVar()
        self.deals_combobox = ttk.Combobox(self, width=40, textvariable=self.deals_var, state='readonly')
        self.deals_combobox.configure(values=('Active deals', 'Previous deals'))
        self.deals_combobox.current(0)
        self.deals_combobox.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="w")
        self.deals_combobox.grid_remove()
        self.deals_var.trace('w', self.load_deals)
        self.deals = None
        self.results = None

        self.search_top_frame = Frame(self, width=1920, height=100, bg="white")
        Label(
            self.search_top_frame, text="Search user/collection", fg='black', bg='white', justify=LEFT,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=0, sticky="we", padx=(20, 20))
        self.search_entry = EntryWithPlaceholder(self.search_top_frame, placeholder='Name')
        self.search_entry.grid(row=1, column=0, sticky="sw", padx=(20, 20))
        br = Frame(self.search_top_frame, width=400, height=2, bg='black')
        br.grid(row=2, column=0, sticky="nw", pady=(0, 20), padx=(20, 20))
        self.search_btn = Button(
            self.search_top_frame, width=30, pady=7, text='Search', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.search_by_name()
        )
        self.search_btn.grid(row=3, column=0, sticky='we', padx=(20, 20))
        Label(
            self.search_top_frame, text="OR", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=1, sticky='we', padx=(20, 20))
        Label(
            self.search_top_frame, text="Search by token details", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=2, sticky='we', padx=(20, 20))
        self.search_token_var = StringVar()
        self.search_token_combobox = ttk.Combobox(self.search_top_frame, width=40, textvariable=self.search_token_var,
                                                  values=('Coin', 'Banknote'), state='readonly')
        self.search_token_combobox.current(0)
        self.search_token_combobox.grid(row=1, column=2, pady=(20, 0), sticky="we", padx=(20, 20))
        self.search_token_btn = Button(
            self.search_top_frame, width=30, pady=7, text='Search by details', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.search_by_details()
        )
        self.search_token_btn.grid(row=3, column=2, sticky='we', padx=(20, 20))
        self.search_top_frame.grid(row=5, column=0, sticky='we')

    def load(self):
        self.controller.geometry("1920x1080+0+0")
        self.controller.state('zoomed')
        self.username = self.controller.username
        self.load_consumer_info()
        self.load_collections()
        print("Home Page page loaded")

    def load_consumer_info(self):
        self.profile_name.configure(text=self.username)
        rs = connection.get_consumer(self.username)
        if rs[3] is not None:
            img = image_from_blob(rs[3])
            img = img.resize((90, 90), Image.ANTIALIAS)
            self.profile_image = ImageTk.PhotoImage(img)
            self.profile_img.configure(image=self.profile_image)

    def load_collections(self):
        self.remove_elements()
        rs = connection.get_collections_preview(self.username)
        collections = [
            PreviewCollection(self, ("New collection", None, None), CollectionType.CREATE_NEW)
        ]
        for collection in rs:
            collections.append(PreviewCollection(self, collection, CollectionType.COLLECTION))

        self.collections = GridManager(
            self, column_count=7, row_width=200, column_width=200, width=1920, height=800, objects=collections
        )
        self.collections.grid(row=2, column=0, sticky='news')

    def show_search_tab(self):
        self.remove_elements()
        self.search_top_frame.grid()

    def load_deals(self, *args):
        self.remove_elements()
        self.deals_combobox.grid()
        is_active = self.deals_var.get() == 'Active deals'
        rs = connection.get_user_deals_coin_preview(self.username, is_active)
        deals = list()
        for deal in rs:
            deals.append(PreviewDeal(self, deal, is_active, is_coin=True))
        rs = connection.get_user_deals_banknote_preview(self.username, is_active)
        for deal in rs:
            deals.append(PreviewDeal(self, deal, is_active, is_coin=False))

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

    def load_coin_deal(self, coin_id):
        deal_window = WindowTokenDeal(self, coin_id, is_coin=True)
        deal_window.grab_set()

    def load_banknote_deal(self, banknote_id):
        deal_window = WindowTokenDeal(self, banknote_id, is_coin=False)
        deal_window.grab_set()

    def after_w_token_deal(self, *args):
        self.load_deals()

    def after_w_banknote_deal(self, *args):
        self.load_deals()

    def remove_elements(self):
        if self.collections is not None:
            self.collections.grid_remove()
        self.deals_combobox.grid_remove()
        if self.deals is not None:
            self.deals.grid_remove()
        self.search_top_frame.grid_remove()
        if self.results is not None:
            self.results.grid_remove()

    def search_by_name(self):
        self.show_search_tab()
        input_name = self.search_entry.get()
        users = connection.search_users(input_name)
        collections = connection.search_collections(input_name)
        search_results = list()
        for user in users:
            search_results.append(SearchUser(self, user))
        for coll in collections:
            search_results.append(SearchCollection(self, coll))

        self.results = ListManager(
            self, row_width=200, width=1920, height=750, objects=search_results
        )
        self.results.grid(row=6, column=0, sticky='news', pady=(20, 0))

    def search_by_details(self):
        if self.search_token_var.get() == 'Coin':
            window = WindowCoinCreateEditSearch(self, window_mode=WindowMode.SEARCH, coin_id=None,
                                                offer_username=self.username)
        else:
            window = WindowBanknoteCreateEditSearch(self, window_mode=WindowMode.SEARCH, banknote_id=None,
                                                    offer_username=self.username)
        window.grab_set()

    def load_search_user(self, user_id):
        self.show_search_tab()
        collections = connection.search_user_collections(user_id)
        search_results = list()
        for coll in collections:
            search_results.append(SearchCollection(self, coll))

        self.results = ListManager(
            self, row_width=200, width=1920, height=750, objects=search_results
        )
        self.results.grid(row=6, column=0, sticky='news', pady=(20, 0))

    def load_search_collection(self, collection_id):
        self.show_search_tab()
        coins = connection.search_collection_coins(collection_id)
        search_results = list()
        for coin in coins:
            search_results.append(SearchToken(self, coin, is_coin=True))

        banknotes = connection.search_collection_banknotes(collection_id)
        for banknote in banknotes:
            search_results.append(SearchToken(self, banknote, is_coin=False))

        self.results = ListManager(
            self, row_width=200, width=1920, height=750, objects=search_results
        )
        self.results.grid(row=6, column=0, sticky='news', pady=(20, 0))

    def load_search_coin(self, coin_id):
        coin_window = WindowCoinCreateEditSearch(self, window_mode=WindowMode.SEARCH_RESULT, coin_id=coin_id,
                                                 offer_username=self.username)
        coin_window.grab_set()

    def load_search_banknote(self, banknote_id):
        banknote_window = WindowBanknoteCreateEditSearch(self, window_mode=WindowMode.SEARCH_RESULT,
                                                         banknote_id=banknote_id, offer_username=self.username)
        banknote_window.grab_set()

    def set_search_results(self, rs, is_coins):
        self.show_search_tab()
        search_results = list()
        for res in rs:
            search_results.append(SearchToken(self, res, is_coin=is_coins))

        self.results = ListManager(
            self, row_width=200, width=1920, height=750, objects=search_results
        )
        self.results.grid(row=6, column=0, sticky='news', pady=(20, 0))

    def edit_user(self, *args):
        window = WindowConsumerEdit(self)
        window.grab_set()

    def close(self, e):
        self.username = None
        self.controller.username = None
        self.controller.title('Login')
        self.controller.geometry('925x500+300+200')
        self.controller.state('normal')
        self.controller.show_frame("PageLogin")


