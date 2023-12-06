import tkinter as tk


class CustomAbstractFrame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, background="gray", width=100, height=80)

        self.__row_counter = 0
        self.__column_counter = 0

    def _new_row(self):
        self.__row_counter += 1
        return self.__row_counter

    def _col(self):
        return self.__column_counter

    
    def _row(self):
        return self.__row_counter

    
    def _new_col(self):
        self.__column_counter += 1
        return self.__column_counter

    def _reset_row(self):
        self.__row_counter = 0

    def _reset_col(self):
        self.__column_counter = 0


FooterAbstractFrame = CustomAbstractFrame
HeaderAbstractFrame = CustomAbstractFrame
RightAbstractFrame = CustomAbstractFrame
