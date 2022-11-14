from Connection import *
from WindowCoinCreate import WindowCoinCreate
from GUI.GridManager import GridManager
from TokenPreview import *
import textwrap


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
        Label(collection_frame, image=self.settings_image, bg="#57a1f8", borderwidth=0).place(x=1645, y=30)

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

        self.coins = None
        self.coins_frame = None
        self.coins_manager = None

    def load(self):
        self.collection_id = self.controller.collection_id
        info = connection.get_collection_info(collection_id=self.collection_id)
        self.collection_name.configure(text=info[0])

        self.collection_description.configure(text=textwrap.fill(info[1], 60))

        img = info[2].read()
        pre_img = io.BytesIO(img)
        self.collection_image = Image.open(pre_img)
        self.collection_image = self.collection_image.resize((300, 300), Image.ANTIALIAS)
        self.collection_image = ImageTk.PhotoImage(self.collection_image)
        self.collection_image_label.configure(image=self.collection_image)

        self.load_coins()
        print("Collection Page page loaded")

    def load_coins(self):
        rs = connection.get_coins(self.collection_id)
        coins = [
            TokenPreview(self, ("New coin", ), TokenType.CREATE_NEW)
        ]
        for collection in rs:
            coins.append(TokenPreview(self, collection, TokenType.TOKEN))

        self.coins = GridManager(
            self, column_count=7, row_width=200, column_width=200, width=1920, height=630, objects=coins
        )
        self.coins.grid(row=2, column=0, sticky='news')

    def load_banknotes(self):
        print("#")

    def create_new_coin(self):
        new_coin_window = WindowCoinCreate(self)
        new_coin_window.grab_set()

    def load_coin(self, coin_id):
        new_coin_window = WindowCoinCreate(self)
        new_coin_window.grab_set()





