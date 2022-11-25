from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
import os
from tkinter.messagebox import showinfo

from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from GUI.TextWithPlaceholder import TextWithPlaceholder
from Connection import *
from Utils import *
from Definitions import *
from WindowMode import WindowMode
from WindowCoinBeginDeal import WindowCoinBeginDeal
from WindowCoinDeal import WindowCoinDeal


class WindowCoinCreateEdit(Toplevel):
    def __init__(self, controller, window_mode, coin_id=None):
        Toplevel.__init__(self)
        self.mode = window_mode
        self.controller = controller
        self.collection_id = controller.collection_id
        self.coin_id = coin_id

        self.geometry('1600x800+200+100')
        self.resizable(False, False)
        self.configure(bg="white")

        self.value_entry = EntryWithPlaceholder(self, "Value")
        self.value_entry.grid(row=0, column=1, sticky="w", pady=(20, 0))
        br = Frame(self, width=400, height=2, bg='black')
        br.grid(row=1, column=1, sticky="w", pady=(0, 20))

        self.currency_var = StringVar()
        self.currency_combobox = ttk.Combobox(self, width=40, textvariable=self.currency_var)
        rs = connection.get_currencies()
        self.currency_combobox.configure(values=tuple_with_delimiter(rs, ' | '))
        self.currency_combobox.current(0)
        self.currency_combobox.grid(row=2, column=1, pady=(20, 0), sticky="w")
        br2 = Frame(self, width=400, height=2, bg='white')
        br2.grid(row=3, column=1, sticky="w", pady=(0, 20))

        self.year_entry = EntryWithPlaceholder(self, "Year")
        self.year_entry.grid(row=4, column=1, sticky="w", pady=(20, 0))
        br3 = Frame(self, width=400, height=2, bg='black')
        br3.grid(row=5, column=1, sticky="w", pady=(0, 20))

        self.subject = TextWithPlaceholder(self, placeholder="Subject", width=40, height=3)
        self.subject.grid(column=1, row=5, rowspan=4, sticky="w", pady=(20, 20))
        br15 = Frame(self, width=400, height=2, bg='black')
        br15.grid(row=9, column=1, sticky="w", pady=(0, 20))

        img = Image.open(PATH_IMAGE_EMPTY)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.coin_image_obverse = Label(self, image=self.image, bg='white', borderwidth=0)
        self.coin_image_obverse.grid(row=10, column=1, sticky="w", pady=(20, 20))
        self.image_value_obverse = None

        img2 = Image.open(PATH_IMAGE_EMPTY)
        img2 = img2.resize((400, 400), Image.ANTIALIAS)
        self.image2 = ImageTk.PhotoImage(img2)
        self.coin_image_reverse = Label(self, image=self.image2, bg='white', borderwidth=0)
        self.coin_image_reverse.grid(row=10, column=2, sticky="w", pady=(20, 20))
        self.image_value_reverse = None

        self.diameter_entry = EntryWithPlaceholder(self, "Diameter")
        self.diameter_entry.grid(row=0, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br7 = Frame(self, width=400, height=2, bg='black')
        br7.grid(row=1, column=2, padx=(20, 20), pady=(0, 20))

        self.weight_entry = EntryWithPlaceholder(self, "Weight")
        self.weight_entry.grid(row=2, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br8 = Frame(self, width=400, height=2, bg='black')
        br8.grid(row=3, column=2, padx=(20, 20), pady=(0, 20))

        self.material_var = StringVar()
        self.material_combobox = ttk.Combobox(self, width=40,  textvariable=self.material_var)
        rs = connection.get_material_names()
        self.material_combobox.configure(values=tuple_list_to_tuple(rs))
        self.material_combobox.current(0)
        self.material_combobox.grid(row=4, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br5 = Frame(self, width=400, height=2, bg='white')
        br5.grid(row=5, column=2, padx=(20, 20), pady=(0, 20))

        self.type_var = StringVar()
        self.type_combobox = ttk.Combobox(self, width=40,  textvariable=self.type_var)
        rs = connection.get_token_types()
        self.type_combobox.configure(values=tuple_list_to_tuple(rs))
        self.type_combobox.current(0)
        self.type_combobox.grid(row=6, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br6 = Frame(self, width=400, height=2, bg='white')
        br6.grid(row=7, column=2, padx=(20, 20), pady=(0, 20))

        self.edge_var = StringVar()
        self.edge_combobox = ttk.Combobox(self, width=40, textvariable=self.edge_var)
        rs = connection.get_edge_types()
        self.edge_combobox.configure(values=tuple_list_to_tuple(rs))
        self.edge_combobox.current(0)
        self.edge_combobox.grid(row=8, column=2, padx=(83, 20), pady=(20, 0), sticky="w")
        br9 = Frame(self, width=400, height=2, bg='white')
        br9.grid(row=9, column=2, padx=(20, 20), pady=(0, 20))

        self.description = TextWithPlaceholder(self, placeholder="Description", width=40, height=5)
        self.description.grid(column=3, row=0, rowspan=5, sticky="w", pady=(0, 20))
        br4 = Frame(self, width=400, height=2, bg='black')
        br4.grid(row=5, column=3, sticky="w", pady=(0, 20))

        if self.collection_id is not None:
            self.collection_var = StringVar()
            self.collection_combobox = ttk.Combobox(self, width=40,  textvariable=self.collection_var)
            rs = connection.get_collection_names(controller.collection_id)
            self.collection_combobox.configure(values=tuple_list_to_tuple(rs[0]))
            self.collection_combobox.current(self.collection_combobox["values"].index(rs[1]))
            self.collection_combobox.grid(row=6, column=3, pady=(20, 0), sticky="w")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.frame_btn = Frame(self, bg="white", width=400, height=400)
        self.frame_btn.grid(row=10, column=3)
        self.sell_delete_btn = Button(
            self.frame_btn, width=30, pady=7, text='', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.sell_delete()
        )
        self.sell_delete_btn.grid(row=0, column=1, sticky="w", pady=(20, 20))
        self.create_edit_save_btn = Button(
            self.frame_btn, width=30, pady=7, text='', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.create_edit_save()
        )
        self.create_edit_save_btn.grid(row=1, column=1, sticky="w", pady=(20, 20))
        self.frame_btn.grid_columnconfigure(0, weight=1)
        self.frame_btn.grid_columnconfigure(2, weight=1)

        self.frame_btn_sale = Frame(self, bg="white", width=400, height=400)
        self.frame_btn_sale.grid(row=10, column=3)
        self.amount_entry = EntryWithPlaceholder(self.frame_btn_sale, "Amount")
        self.value_entry.grid(row=0, column=1, sticky="w", pady=(20, 0))
        br99 = Frame(self.frame_btn_sale, width=400, height=2, bg='black')
        br99.grid(row=1, column=1, sticky="w", pady=(0, 20))
        self.make_offer_btn = Button(
            self.frame_btn_sale, width=30, pady=7, text='Make offer', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11, 'bold'), command=lambda: self.make_offer()
        )
        self.make_offer_btn.grid(row=2, column=1, sticky="w", pady=(20, 20))
        self.frame_btn_sale.grid_columnconfigure(0, weight=1)
        self.frame_btn_sale.grid_columnconfigure(2, weight=1)
        self.frame_btn_sale.grid_remove()

        self.coin_image_obverse.bind("<Button-1>", self.set_image_obverse)
        self.coin_image_reverse.bind("<Button-1>", self.set_image_reverse)

        self.set_mode(self.mode)

    def destroy(self) -> None:
        Toplevel.destroy(self)
        self.controller.load_coins()

    def sell_delete(self):
        if self.mode == WindowMode.VIEW:
            new_deal_window = WindowCoinBeginDeal(self, self.coin_id)
            new_deal_window.grab_set()
        elif self.mode == WindowMode.ON_SALE:
            deal_window = WindowCoinDeal(self, self.coin_id)
            deal_window.grab_set()
        else:
            answer = askyesno('Coin delete confirmation', 'Are you sure? Information about coin will be lost')
            if answer:
                connection.delete_coin(self.coin_id)
                self.controller.load_coins()
                self.destroy()

    def after_w_coin_deal(self, destroy):
        if destroy:
            self.destroy()

    def create_edit_save(self):
        if self.mode == WindowMode.ON_SALE:
            showinfo("Info", "You can't edit coin when it's on sale")
            return
        elif self.mode == WindowMode.VIEW:
            self.set_mode(WindowMode.EDIT)
            return
        is_error = False
        try:
            value = int(self.value_entry.get())
        except ValueError:
            self.value_entry.set_text("1")
            is_error = True
        currency = self.currency_var.get().split(" | ")
        try:
            year = int(self.year_entry.get())
        except ValueError:
            self.year_entry.set_text("2000")
            is_error = True
        subject = self.subject.get_text()
        try:
            diameter = float(self.diameter_entry.get())
        except ValueError:
            self.diameter_entry.set_text("10.0")
            is_error = True
        try:
            weight = float(self.weight_entry.get())
        except ValueError:
            self.weight_entry.set_text("2.0")
            is_error = True
        material = self.material_var.get()
        type_name = self.type_var.get()
        edge = self.edge_var.get()
        description = self.description.get_text()
        collection_name = self.collection_var.get()
        if is_error:
            return
        if self.mode == WindowMode.CREATE_NEW:
            connection.create_coin(value=value, currency_name=currency[0], currency_country=currency[1], year=year,
                                   token_type=type_name, material=material, image_obverse=self.image_value_obverse,
                                   image_reverse=self.image_value_reverse, description=description, subject=subject,
                                   diameter=diameter, weight=weight, edge=edge, collection_name=collection_name)
            self.controller.load_coins()
            self.destroy()
        elif self.mode == WindowMode.EDIT:
            connection.update_coin(value=value, currency_name=currency[0], currency_country=currency[1], year=year,
                                   token_type=type_name, material=material, image_obverse=self.image_value_obverse,
                                   image_reverse=self.image_value_reverse, description=description, subject=subject,
                                   diameter=diameter, weight=weight, edge=edge, coin_id=self.coin_id,
                                   collection_name=collection_name)
            self.set_mode(WindowMode.VIEW)

    def set_image_obverse(self, e):
        if self.mode == WindowMode.VIEW:
            return
        file = open_image("Set obverse")
        if not file:
            return
        img = Image.open(file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(img)
        self.coin_image_obverse.configure(image=self.image)
        file = open(file, 'rb')
        file = io.BytesIO(file.read())
        file.seek(0, os.SEEK_END)
        self.image_value_obverse = file.getvalue()

    def set_image_reverse(self, e):
        if self.mode == WindowMode.VIEW:
            return
        file = open_image("Set reverse")
        if not file:
            return
        img = Image.open(file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        self.image2 = ImageTk.PhotoImage(img)
        self.coin_image_reverse.configure(image=self.image2)
        file = open(file, 'rb')
        file = io.BytesIO(file.read())
        file.seek(0, os.SEEK_END)
        self.image_value_reverse = file.getvalue()

    def set_enable_state(self, enabled):
        if enabled:
            self.value_entry.config(state=NORMAL)
            self.currency_combobox.config(state="readonly")
            self.year_entry.config(state=NORMAL)
            self.subject.config(state=NORMAL)
            self.diameter_entry.config(state=NORMAL)
            self.weight_entry.config(state=NORMAL)
            self.material_combobox.config(state="readonly")
            self.type_combobox.config(state="readonly")
            self.edge_combobox.config(state="readonly")
            self.description.config(state=NORMAL)
            self.collection_combobox.config(state="readonly")
        else:
            self.value_entry.config(state=DISABLED)
            self.currency_combobox.config(state=DISABLED)
            self.year_entry.config(state=DISABLED)
            self.subject.config(state=DISABLED)
            self.diameter_entry.config(state=DISABLED)
            self.weight_entry.config(state=DISABLED)
            self.material_combobox.config(state=DISABLED)
            self.type_combobox.config(state=DISABLED)
            self.edge_combobox.config(state=DISABLED)
            self.description.config(state=DISABLED)
            self.collection_combobox.config(state=DISABLED)

    def load(self):
        rs = connection.get_coin(self.coin_id)
        if rs[0] is not None:
            self.value_entry.set_text(str(rs[0]))
        if rs[1] is not None:
            self.currency_combobox.current(self.currency_combobox["values"].index(rs[1] + ' | ' + rs[2]))
        if rs[3] is not None:
            self.year_entry.set_text(str(rs[3]))
        if rs[4] is not None:
            self.type_combobox.current(self.type_combobox["values"].index(rs[4]))
        if rs[5] is not None:
            self.material_combobox.current(self.material_combobox["values"].index(rs[5]))

        if rs[6] is not None:
            img = image_from_blob(rs[6])
            img = img.resize((400, 400), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(img)
            self.coin_image_obverse.config(image=self.image)
            self.image_value_obverse = rs[6]

        if rs[7] is not None:
            img2 = image_from_blob(rs[7])
            img2 = img2.resize((400, 400), Image.ANTIALIAS)
            self.image2 = ImageTk.PhotoImage(img2)
            self.coin_image_reverse.config(image=self.image2)
            self.image_value_reverse = rs[7]

        if rs[8] is not None:
            self.description.set_text(rs[8])
        if rs[9] is not None:
            self.subject.set_text(rs[9])
        if rs[10] is not None:
            self.diameter_entry.set_text(str(rs[10]))
        if rs[11] is not None:
            self.weight_entry.set_text(str(rs[11]))
        if rs[12] is not None:
            self.edge_combobox.current(self.edge_combobox["values"].index(rs[12]))
        if rs[13] is not None:
            self.set_mode(WindowMode.ON_SALE)

    def set_mode(self, mode):
        self.mode = mode
        if self.mode == WindowMode.CREATE_NEW:
            self.create_edit_save_btn.config(text="CREATE")
            self.sell_delete_btn.grid_remove()
            self.set_enable_state(True)
            self.title('Create coin')
        elif self.mode == WindowMode.VIEW:
            self.create_edit_save_btn.config(text="EDIT")
            self.sell_delete_btn.config(text="SELL")
            self.load()
            self.set_enable_state(False)
            self.title('View coin')
        elif self.mode == WindowMode.EDIT:
            self.create_edit_save_btn.config(text="SAVE")
            self.sell_delete_btn.config(text="DELETE")
            self.set_enable_state(True)
            self.title('Edit coin')
        elif self.mode == WindowMode.ON_SALE:
            self.sell_delete_btn.config(text="SALE DETAILS")
        elif self.mode == WindowMode.SALE_VIEW:
            self.frame_btn.grid_remove()
        elif self.mode == WindowMode.SALE_VIEW or self.mode == WindowMode.AUCTION_VIEW:
            self.frame_btn.grid_remove()
            self.frame_btn_sale.grid()
            if self.mode == WindowMode.SALE_VIEW:
                price = connection.get_sale_price(self.coin_id)
                self.amount_entry.set_text(price)
                self.amount_entry.config(state=DISABLED)

    def make_offer(self):
        if self.mode == WindowMode.SALE_VIEW:
            try:
                amount = int(self.amount_entry.get())
            except ValueError:
                price = connection.get_sale_price(self.coin_id)
                self.amount_entry.set_text(price)
                return
            connection.make_sale_offer(self.controller.user_id, amount)
        elif self.mode == WindowMode.AUCTION_VIEW:
            try:
                amount = int(self.amount_entry.get())
            except ValueError:
                price = connection.get_auction_price(self.coin_id)
                self.amount_entry.set_text(price[0] + price[1])
                return
            connection.make_auction_offer(self.controller.user_id, amount)





