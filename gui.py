import tkinter as tk
import main
from PIL import Image, ImageTk

'''

TODO:
Basic GUI
Display vision bbox area, allow adjusting
Console w/ status updates (detected fishing, detected ...)
If detected 3 fishing in a row, deactivate fishing


'''


class GUI:

    def __init__(self):
        # INIT

        self.root = tk.Tk()

        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)

        # 0 = off, 1 = on can buy, 0 = on cannot buy
        self.state = tk.IntVar()

        self.root.geometry("600x400")
        self.root.title("Autofisher")

        # TITLE / SUBTITLE

        self.title = tk.Label(self.root, text="Autofisher", font=('Lato', 18))
        self.title.pack(pady=10)

        self.subtitle = tk.Label(self.root, text="Made by @cityofgod. on Discord!", font=('Lato', 12))
        self.subtitle.pack()

        # VISION WIDGET

        self.vision_load = Image.open('testpoint.png')
        self.vision_load = self.vision_load.resize((264, 64))

        self.vision = ImageTk.PhotoImage(self.vision_load)
        self.vision_label = tk.Label(self.root, image=self.vision)
        self.vision_label.place(relx=0.98, rely=0.98, anchor=tk.SE)  # Place at the bottom right

        self.vision_label_text = tk.Label(self.root, text="Vision", font=('Lato', 16))
        self.vision_label_text.place(relx=0.8, rely=0.8, anchor=tk.SE)

        # RADIO BUTTONS

        self.radio_off = tk.Radiobutton(self.root, text="Off", variable=self.state, value=0, command=self.handle_selection)
        self.radio_on_can_buy = tk.Radiobutton(self.root, text="On (Can sell)", variable=self.state, value=1, command=self.handle_selection)
        self.radio_on_cannot_buy = tk.Radiobutton(self.root, text="On (Cannot sell)", variable=self.state, value=2, command=self.handle_selection)

        self.radio_on_can_buy.pack(anchor='w', pady=20)
        self.radio_on_cannot_buy.pack(anchor='w', pady=20)
        self.radio_off.pack(anchor='w', pady=20)

        # BOUNDING BOX -> 898, 807, 951, 821

        validation = self.root.register(self.validate_and_update)

        self.x1_entry_label = tk.Label(self.root, text="x1", font=("Lato", 10))
        self.x1_entry_label.place(x=175, y=335)
        self.x1_entry = tk.Entry(self.root, validatecommand=(validation, "%P"), validate="key", width=5)
        self.x1_entry.place(x=200, y=335)
        self.x1_entry.insert(tk.END, "10")

        self.x2_entry_label = tk.Label(self.root, text="x2", font=("Lato", 10))
        self.x2_entry_label.place(x=175, y=365)
        self.x2_entry = tk.Entry(self.root, validatecommand=(validation, "%P"), validate="key", width=5)
        self.x2_entry.place(x=200, y=365)

        self.y1_entry_label = tk.Label(self.root, text="y1", font=("Lato", 10))
        self.y1_entry_label.place(x=250, y=335)
        self.y1_entry = tk.Entry(self.root, validatecommand=(validation, "%P"), validate="key", width=5)
        self.y1_entry.place(x=275, y=335)

        self.y2_entry_label = tk.Label(self.root, text="y2", font=("Lato", 10))
        self.y2_entry_label.place(x=250, y=365)
        self.y2_entry = tk.Entry(self.root, validatecommand=(validation, "%P"), validate="key", width=5)
        self.y2_entry.place(x=275, y=365)

        # LOOP

        self.root.mainloop()

    def handle_selection(self):
        main.capture()
        self.update_image()

    def validate_and_update(self, text):
        if text.isdigit() and text != " ":
            '''self.x1 = int(self.x1_entry.get())
            self.x2 = int(self.x2_entry.get())
            self.y1 = int(self.x1_entry.get())
            self.y2 = int(self.x1_entry.get())'''
            return True
        else:
            return False

    def update_image(self):
        self.vision_load = Image.open('testpoint.png')
        self.vision_load = self.vision_load.resize((264, 64))
        self.vision = ImageTk.PhotoImage(self.vision_load)
        self.vision_label.config(image=self.vision)


if __name__ == '__main__':
    gui = GUI()
