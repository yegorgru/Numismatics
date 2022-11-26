from tkinter import *


class EntryWithPlaceholder(Entry):
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.configure(show="")

    def set_text(self, text):
        self.delete('0', 'end')
        self['fg'] = self.default_fg_color
        self.insert(0, text)

    def foc_in(self, *args):
        if self["state"] == NORMAL and self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            if self.secret:
                self.configure(show="*")

    def foc_out(self, *args):
        if self["state"] == NORMAL and not self.get():
            self.put_placeholder()

    def has_input(self):
        return self['fg'] == self.default_fg_color

    def check(self, *args):
        if len(self.get()) <= self.max_len:
            self.old_value = self.get()
        else:
            self.var.set(self.old_value)

    def get_text(self):
        if self.has_input():
            return self.get()
        else:
            return ""

    def __init__(self, parent=None, placeholder="PLACEHOLDER", secret=False, width=20, bg='white'):
        self.secret = secret
        Entry.__init__(self, parent, width=width, fg='black', border=0, bg=bg, font=('Microsoft YaHei UI Light', 11),
                       disabledbackground="white")
        if secret:
            self.configure(show="*")
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = 'black'

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.var = StringVar()
        self.max_len = width
        self.configure(textvariable=self.var)
        self.var.trace('w', self.check)

        self.put_placeholder()
        self.old_value = self.get()