import tkinter as tk
import main
from PIL import Image, ImageTk

'''

TODO:
Basic GUI
Display monitor area, allow adjusting

'''


class GUI:

    def __init__(self):
        self.root = tk.Tk()

        self.root.attributes('-topmost', True)

        # 0 = off, 1 = on can buy, 0 = on cannot buy
        self.state = tk.IntVar()

        self.root.geometry("600x400")
        self.root.title("Autofisher")

        self.title = tk.Label(self.root, text="Autofisher", font=('Lato', 18))
        self.title.pack(pady=10)

        self.subtitle = tk.Label(self.root, text="Made by BP", font=('Lato', 12))
        self.subtitle.pack()

        self.vision_load = Image.open('testpoint.png')
        self.vision_load = self.vision_load.resize((264, 64))

        self.vision = ImageTk.PhotoImage(self.vision_load)
        self.vision_label = tk.Label(self.root, image=self.vision)
        self.vision_label.place(relx=0.98, rely=0.98, anchor=tk.SE)  # Place at the bottom right

        self.vision_label_text = tk.Label(self.root, text="Vision", font=('Lato', 16))
        self.vision_label_text.place(relx=0.8, rely=0.8, anchor=tk.SE)

        self.radio_off = tk.Radiobutton(self.root, text="Off", variable=self.state, value=0, command=self.handle_selection)
        self.radio_on_can_buy = tk.Radiobutton(self.root, text="On (Can sell)", variable=self.state, value=1, command=self.handle_selection)
        self.radio_on_cannot_buy = tk.Radiobutton(self.root, text="On (Cannot sell)", variable=self.state, value=2, command=self.handle_selection)

        self.radio_on_can_buy.pack()
        self.radio_on_cannot_buy.pack()
        self.radio_off.pack()

        self.root.mainloop()

    def handle_selection(self):
        main.capture()
        self.update_image()

    def update_image(self):
        self.vision_load = Image.open('testpoint.png')
        self.vision_load = self.vision_load.resize((264, 64))
        self.vision = ImageTk.PhotoImage(self.vision_load)
        self.vision_label.config(image=self.vision)


if __name__ == '__main__':
    gui = GUI()
