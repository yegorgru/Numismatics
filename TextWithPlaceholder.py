from tkinter import *


class TextWithPlaceholder(Text):
    def put_placeholder(self):
        self.insert(INSERT, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        print(0000)
        if self['fg'] == self.placeholder_color:
            self.delete("1.0", END)
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if len(self.get("1.0", "end-1c")) == 0:
            self.put_placeholder()

    def check(self, *args):
        string = self.get("1.0", "end-1c")
        breaks = string.count('\n')
        char_number = len(string) - breaks
        print(char_number)
        print("breaks", breaks)
        if char_number > self.max_char_number:
            self.delete("1.0", END)
            self.insert(INSERT, string[:self.max_char_number])

    def get_text(self):
        return self.get("1.0", "end-1c").replace('\n', ' ')

    def __init__(self, parent=None, placeholder="PLACEHOLDER", width=30, height=5):
        Text.__init__(
            self, parent, width=width, height=height, fg='black', border=0, bg='white',
            font=('Microsoft YaHei UI Light', 11)
        )
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = 'black'

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.bind('<KeyRelease>', self.check)
        self.max_char_number = width * height

        self.put_placeholder()
