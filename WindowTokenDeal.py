from tkinter import *
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno

from Connection import *
from Utils import *
from Definitions import *


class WindowTokenDeal(Toplevel):
    def __init__(self, controller, token_id, is_coin):
        Toplevel.__init__(self)
        self.controller = controller
        self.token_id = token_id
        self.is_coin = is_coin

        self.title('Sell details')
        self.geometry('700x400+300+100')
        self.resizable(False, False)
        self.configure(bg="white")

        img = Image.open(PATH_IMAGE_EMPTY_PROFILE)
        img = img.resize((90, 90), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        self.img_label = Label(self, image=self.profile_image, bg='white', borderwidth=0)
        self.img_label.grid(row=0, column=1)

        self.profile_name = Label(
            self, text="", fg='black', bg='white',
            font=('Microsoft YaHei UI Light', 18, 'bold')
        )
        self.profile_name.grid(row=0, column=2)

        self.price = Label(
            self, text="", fg='black', bg='white',
            font=('Microsoft YaHei UI Light', 18, 'bold')
        )
        self.price.grid(row=0, column=3)

        frame_btn = Frame(self, bg="white", width=400, height=200)
        frame_btn.grid(row=1, column=2)
        self.refresh_btn = Button(
            frame_btn, width=30, pady=7, text='Refresh', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.load()
        )
        self.cancel_btn = Button(
            frame_btn, width=30, pady=7, text='Cancel Deal', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.cancel()
        )
        self.approve_btn = Button(
            frame_btn, width=30, pady=7, text='Approve Deal', bg='#57a1f8', fg='white', border=0,
            font=('Microsoft YaHei UI Light', 11), command=lambda: self.approve_deal()
        )
        self.refresh_btn.grid(row=0, column=1, sticky="w", pady=(20, 20))
        self.cancel_btn.grid(row=1, column=1, sticky="w", pady=(20, 20))
        self.approve_btn.grid(row=2, column=1, sticky="w", pady=(20, 20))
        frame_btn.grid_columnconfigure(0, weight=1)
        frame_btn.grid_columnconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.load()

    def destroy(self, destroy=False) -> None:
        Toplevel.destroy(self)
        self.controller.after_w_token_deal(destroy)

    def load(self):
        if self.is_coin:
            rs = connection.get_deal_coin_details(self.token_id)
        else:
            rs = connection.get_deal_banknote_details(self.token_id)
        if rs is None:
            img = Image.open(PATH_IMAGE_EMPTY_PROFILE)
            self.profile_name.configure(text='Offers not found')
            self.price.configure(text='0 $')
            self.approve_btn.grid_remove()
        else:
            self.profile_name.configure(text=rs[1])
            self.price.configure(text=str(rs[2]) + ' $')
            if rs[0] is not None:
                img = image_from_blob(rs[0])
            else:
                img = Image.open(PATH_IMAGE_EMPTY_PROFILE)
            self.approve_btn.grid()
        img = img.resize((90, 90), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.profile_image)

    def approve_deal(self):
        answer = askyesno('Approve deal confirmation', 'You won\'t be able to cancel deal')
        if answer:
            if self.is_coin:
                connection.approve_coin_deal(self.token_id)
            else:
                connection.approve_banknote_deal(self.token_id)
            self.destroy(True)

    def cancel(self):
        answer = askyesno('Cancel deal confirmation', 'Confirm if you want to cancel deal')
        if answer:
            if self.is_coin:
                connection.cancel_coin_deal(self.token_id)
            else:
                connection.cancel_banknote_deal(self.token_id)
            self.destroy(True)


