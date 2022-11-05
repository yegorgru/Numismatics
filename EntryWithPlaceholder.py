from tkinter import Entry


class EntryWithPlaceholder(Entry):
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.configure(show="")

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            if self.secret:
                self.configure(show="*")

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def has_input(self):
        return self['fg'] == self.default_fg_color

    def __init__(self, parent=None, placeholder="PLACEHOLDER", secret=False):
        self.secret = secret
        Entry.__init__(self, parent, width=20, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        if secret:
            self.configure(show="*")
        self.placeholder = placeholder
        self.placeholder_color = 'grey'
        self.default_fg_color = 'black'

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()