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
from StatisticsConsumerRow import StatisticsConsumerRow
from StatisticsTokenRow import StatisticsTokenRow

from tkinter.messagebox import showwarning


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
        self.statistics_btn = Button(
            section_buttons_frame, width=30, text='Statistics', bg='white', fg='black', border=0,
            font=('Microsoft YaHei UI Light', 15), command=lambda: self.show_statistics_tab()
        )
        self.statistics_btn.grid(row=0, column=3)

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

        self.statistics_frame = Frame(self, width=1920, height=100, bg="white")
        self.statistics_var = StringVar()
        self.statistics_combobox = ttk.Combobox(
            self.statistics_frame, width=40, textvariable=self.statistics_var,
            values=(STATISTICS_USER, STATISTICS_USER_TOP, STATISTICS_COIN, STATISTICS_COIN_TOP,
                    STATISTICS_BANKNOTE, STATISTICS_BANKNOTE_TOP),
            state='readonly'
        )
        self.statistics_combobox.current(0)
        self.statistics_combobox.grid(row=1, column=0, pady=(20, 0), sticky="we", padx=(20, 20))
        self.statistics_entry = EntryWithPlaceholder(self.statistics_frame, width=40, placeholder='Value')
        self.statistics_entry.grid(row=2, column=0, sticky="sw", padx=(20, 20), pady=(20, 0))
        br = Frame(self.statistics_frame, width=400, height=2, bg='black')
        br.grid(row=3, column=0, sticky="nw", pady=(0, 20), padx=(20, 20))
        self.show_statistics_btn = Button(
            self.statistics_frame, width=30, pady=7, text='Show', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.show_statistics()
        )
        self.show_statistics_btn.grid(row=4, column=0, sticky='we', padx=(20, 20))
        self.statistics_frame.grid(row=7, column=0, sticky='news')

        self.user_statistics_frame = Frame(self.statistics_frame, bg="white")
        Label(
            self.user_statistics_frame, text="Income", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=0, sticky="we", padx=(20, 20), pady=(20, 20))
        Label(
            self.user_statistics_frame, text="Spending", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=1, sticky="we", padx=(20, 20), pady=(20, 20))
        Label(
            self.user_statistics_frame, text="Deals", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=2, sticky="we", padx=(20, 20), pady=(20, 20))
        Label(
            self.user_statistics_frame, text="Tokens", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=3, sticky="we", padx=(20, 20), pady=(20, 20))
        Label(
            self.user_statistics_frame, text="Collections", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=4, sticky="we", padx=(20, 20), pady=(20, 20))

        self.user_statistics_income = Label(
            self.user_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.user_statistics_income.grid(row=1, column=0, sticky="we", padx=(20, 20), pady=(20, 20))
        self.user_statistics_spending = Label(
            self.user_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.user_statistics_spending.grid(row=1, column=1, sticky="we", padx=(20, 20), pady=(20, 20))
        self.user_statistics_deals = Label(
            self.user_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.user_statistics_deals.grid(row=1, column=2, sticky="we", padx=(20, 20), pady=(20, 20))
        self.user_statistics_tokens = Label(
            self.user_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.user_statistics_tokens.grid(row=1, column=3, sticky="we", padx=(20, 20), pady=(20, 20))
        self.user_statistics_collections = Label(
            self.user_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.user_statistics_collections.grid(row=1, column=4, sticky="we", padx=(20, 20), pady=(20, 20))
        self.user_statistics_frame.grid(row=5, column=0, sticky='we')

        self.user_statistics_top_frame_list = None

        self.token_statistics_frame = Frame(self.statistics_frame, bg="white")
        Label(
            self.token_statistics_frame, text="Total spending", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=0, sticky="we", padx=(20, 20), pady=(20, 20))
        Label(
            self.token_statistics_frame, text="Owners", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        ).grid(row=0, column=1, sticky="we", padx=(20, 20), pady=(20, 20))

        self.token_statistics_total_spending = Label(
            self.token_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.token_statistics_total_spending.grid(row=1, column=0, sticky="we", padx=(20, 20), pady=(20, 20))
        self.token_statistics_owners = Label(
            self.token_statistics_frame, text="", fg='black', bg='white', justify=CENTER,
            font=('Microsoft YaHei UI Light', 11, 'bold')
        )
        self.token_statistics_owners.grid(row=1, column=1, sticky="we", padx=(20, 20), pady=(20, 20))
        self.token_statistics_frame.grid(row=6, column=0, sticky='we')

        self.tokens_statistics_top_frame_list = None

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

    def show_statistics_tab(self):
        self.remove_elements()
        self.statistics_frame.grid()
        self.statistics_entry.configure(state=NORMAL)
        self.statistics_combobox.configure(state="readonly")
        self.statistics_combobox.current(0)
        self.statistics_entry.set_text(self.username)
        self.show_statistics()

    def show_statistics(self):
        self.remove_elements_statistics()
        stat = self.statistics_var.get()
        is_admin = connection.is_admin(self.username)
        if not is_admin:
            self.statistics_entry.configure(state=DISABLED)
            self.statistics_combobox.configure(state=DISABLED)
        if stat == STATISTICS_USER:
            self.user_statistics_frame.grid()
            self.load_statistics_user()
        elif stat == STATISTICS_USER_TOP:
            self.load_statistics_user_top()
        elif stat == STATISTICS_COIN:
            self.token_statistics_frame.grid()
            self.load_statistics_token(is_coin=True)
        elif stat == STATISTICS_COIN_TOP:
            self.load_statistics_token_top(is_coin=True)
        elif stat == STATISTICS_BANKNOTE:
            self.token_statistics_frame.grid()
            self.load_statistics_token(is_coin=False)
        elif stat == STATISTICS_BANKNOTE_TOP:
            self.load_statistics_token_top(is_coin=False)

    def load_statistics_user(self):
        user_name = self.statistics_entry.get_text()
        rs = connection.get_user_statistics(user_name)
        self.user_statistics_income.configure(text=rs[0])
        self.user_statistics_spending.configure(text=rs[1])
        self.user_statistics_deals.configure(text=rs[2])
        self.user_statistics_tokens.configure(text=rs[3])
        self.user_statistics_collections.configure(text=rs[4])

    def load_statistics_user_top(self):
        inp = self.statistics_entry.get_text().split(',')
        if len(inp) != 2 and len(inp) != 4:
            showwarning("Warning", "Incorrect input detected")
        elif len(inp) == 2:
            month_begin = 202201
            month_end = 210001
        elif len(inp) == 4:
            month_begin = int(inp[2])
            month_end = int(inp[3])
        rs = connection.get_user_statistics_top(inp[0], int(inp[1]), month_begin, month_end)
        users = list()
        heading = ("Name", "Income", "Spending", "Deals", "Tokens")
        users.append(StatisticsConsumerRow(heading))
        for user in rs:
            users.append(StatisticsConsumerRow(user))

        self.user_statistics_top_frame_list = ListManager(
            self, row_width=100, width=1920, height=700, objects=users
        )
        self.user_statistics_top_frame_list.grid(row=8, column=0, sticky='news')

    def load_statistics_token(self, is_coin):
        try:
            token_id = int(self.statistics_entry.get_text())
        except ValueError:
            showwarning("Warning", "Incorrect input")
            return
        if is_coin:
            rs = connection.get_coin_statistics(token_id)
        else:
            rs = connection.get_banknote_statistics(token_id)
        self.token_statistics_total_spending.configure(text=rs[0])
        self.token_statistics_owners.configure(text=rs[1])

    def load_statistics_token_top(self, is_coin):
        inp = self.statistics_entry.get_text().split(',')
        if is_coin:
            rs = connection.get_coin_statistics_top(inp[0], int(inp[1]))
        else:
            rs = connection.get_banknote_statistics_top(inp[0], int(inp[1]))
        tokens = list()
        heading = (None, "Token id", "Total spending", "Owners")
        tokens.append(StatisticsTokenRow(heading, is_heading=True))
        for user in rs:
            tokens.append(StatisticsTokenRow(user))

        self.tokens_statistics_top_frame_list = ListManager(
            self, row_width=100, width=1920, height=700, objects=tokens
        )
        self.tokens_statistics_top_frame_list.grid(row=9, column=0, sticky='news')

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
        self.statistics_frame.grid_remove()
        if self.user_statistics_top_frame_list is not None:
            self.user_statistics_top_frame_list.grid_remove()
        if self.tokens_statistics_top_frame_list is not None:
            self.tokens_statistics_top_frame_list.grid_remove()

    def remove_elements_statistics(self):
        self.user_statistics_frame.grid_remove()
        if self.user_statistics_top_frame_list is not None:
            self.user_statistics_top_frame_list.grid_remove()
        self.token_statistics_frame.grid_remove()
        if self.tokens_statistics_top_frame_list is not None:
            self.tokens_statistics_top_frame_list.grid_remove()

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


