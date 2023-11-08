import tkinter as tk


class ReadFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        label = tk.Label(self, text="Cześć")
        label.pack()

    def show_message_loaded_data(self):
        label = tk.Label(self, text="Cześć")
        label.pack()
