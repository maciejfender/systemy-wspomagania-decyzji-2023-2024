import tkinter as tk


class ScrollableCustomFrame(tk.Frame):

    def on_mousewheel(self,event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def __init__(self,master):
        super().__init__(master)
        self.master = master

        # Create a Canvas widget
        self.canvas = tk.Canvas(master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(master, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Function to enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create a frame inside the canvas to hold your content
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

    def get_frame_for_content(self):
        return self.frame

    def update_view_after_adding_elements(self):
        # Update the scrollable area
        self.frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


