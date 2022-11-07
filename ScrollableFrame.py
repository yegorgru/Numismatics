import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    def __init__(self, container, height):
        super().__init__(container)
        self.configure(bg="white")
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")

            )
        )
        self.scrollable_frame.configure(bg="white")
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, height=height, bg="white")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")