import tkinter as tk


class CustomAbstractFrame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, background="pink", width=100, height=80)


FooterAbstractFrame = CustomAbstractFrame
HeaderAbstractFrame = CustomAbstractFrame
RightAbstractFrame = CustomAbstractFrame
