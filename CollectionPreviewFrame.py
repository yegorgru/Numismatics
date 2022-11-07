from tkinter import *
from PIL import Image, ImageTk
import io


class CollectionPreviewFrame(Frame):
    PLUS_COLLECTION = "_________________PLUS"
    GENERAL_COLLECTION = "General"

    def click_slot(self, e):
        print(self.collection_name, "clicked!")
        if self.collection_name == self.PLUS_COLLECTION:
            self.controller.create_new_collection()
        else:
            print(1)

    def __init__(self, parent, controller, collection):
        Frame.__init__(self, parent, bg="white", width=200, height=200)
        self.controller = controller
        self.is_plus = collection[0] == self.PLUS_COLLECTION
        if collection[0] == self.GENERAL_COLLECTION:
            img = Image.open("assets/general.jpg")
        elif self.is_plus:
            img = Image.open("assets/plus.png")
        elif collection[1] is None:
            img = Image.open("assets/empty_image.png")
        else:
            img = collection[1].read()  # reading the first BLOB result
            pre_img = io.BytesIO(img)
            img = Image.open(pre_img)
        img = img.resize((150, 150), Image.ANTIALIAS)
        self.profile_image = ImageTk.PhotoImage(img)
        self.img_label = Label(self, image=self.profile_image, bg='white', borderwidth=0)
        self.img_label.grid(row=0, column=0)
        self.collection_name = collection[0]
        if self.is_plus:
            text = "New collection"
        else:
            text = self.collection_name
        self.heading = Label(self, width=20,  text=text, fg='black', bg='white', font=('Microsoft YaHei UI Light', 12, 'bold'))
        self.heading.grid(row=1, column=0)

        self.bind("<Button-1>", self.click_slot)
        self.img_label.bind("<Button-1>", self.click_slot)
        self.heading.bind("<Button-1>", self.click_slot)

