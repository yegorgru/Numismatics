from tkinter import *
from tkinter import ttk

from GUI.EntryWithPlaceholder import EntryWithPlaceholder
from Connection import *
from WindowMode import WindowMode


class WindowCoinBeginDeal(Toplevel):
    def __init__(self, controller, coin_id):
        Toplevel.__init__(self)
        self.controller = controller
        self.coin_id = coin_id

        self.title('Sell details')
        self.geometry('500x250+300+100')
        self.resizable(False, False)
        self.configure(bg="white")

        self.deal_type_var = StringVar()
        self.deal_type_combobox = ttk.Combobox(self, width=40, textvariable=self.deal_type_var, state="readonly")
        self.deal_type_combobox.configure(values=('Sale', 'Auction'))
        self.deal_type_combobox.current(0)
        self.deal_type_combobox.grid(row=0, column=1, pady=(20, 0), sticky="w")

        self.price_entry = EntryWithPlaceholder(self, "Price")
        self.price_entry.grid(row=1, column=1, sticky="w", pady=(20, 0))
        br = Frame(self, width=400, height=2, bg='black')
        br.grid(row=2, column=1, sticky="w", pady=(0, 20))

        frame_btn = Frame(self, bg="white", width=400, height=200)
        frame_btn.grid(row=3, column=1)
        self.create_deal_btn = Button(
            frame_btn, width=30, pady=7, text='Create Deal', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.create_deal()
        )
        self.create_deal_btn.grid(row=0, column=1, sticky="w", pady=(20, 20))
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def destroy(self) -> None:
        Toplevel.destroy(self)
        self.controller.set_mode(WindowMode.VIEW)
        self.controller.load()

    def create_deal(self):
        try:
            price = int(self.price_entry.get())
            deal_type = self.deal_type_var.get()
        except ValueError:
            self.price_entry.set_text("1")
            return
        connection.create_deal(
            self.coin_id, price, deal_type
        )
        self.destroy()


