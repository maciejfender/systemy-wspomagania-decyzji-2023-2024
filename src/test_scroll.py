import tkinter as tk

from components.ScrollableCustomFrame import ScrollableCustomFrame

root = tk.Tk()
root.geometry("300x200")

s = ScrollableCustomFrame(root)
frame = s.get_frame_for_content()

# Example content (labels)
for i in range(30):
    tk.Label(frame, text=f"Label {i}").pack()
s.update_view_after_adding_elements()



root.mainloop()

if __name__ == '__main__':
    pass