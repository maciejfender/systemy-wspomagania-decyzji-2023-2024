import tkinter as tk
from tkinter import ttk


class GraphSettings(tk.Frame):
    def __init__(self, master, background='white', width=0, height=0):
        super().__init__(master, background=background, width=width, height=height)

