import tkinter as tk
import main

'''

TODO:
Basic GUI
Display monitor area, allow adjusting

'''
def setup():
    root = tk.Tk()

    root.geometry("600x400")
    root.title("Autofisher")

    title = tk.Label(root, text="Autofisher", font=('Lato', 18))
    title.pack(pady=10)

    subtitle = tk.Label(root, text="Made by BP", font=('Lato', 12))
    subtitle.pack()

    textbox = tk.Text(root)
    textbox.pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    setup()
