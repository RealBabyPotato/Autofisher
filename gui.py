import tkinter as tk
import main
from PIL import Image, ImageTk
import threading

'''

TODO:
(O) Basic GUI
(O) Display vision bbox area, allow adjusting 
- Console w/ status updates (detected fishing, detected ...)
- If detected 3 fishing in a row, deactivate fishing
-Show time until next sell
- Keep a profile of preferred settings
- If previous state was detected fish on and current state is detected not fishing then
immediately click to speed up fishing process
- Adjust hook speed based off of hook speed level
- Allow bbox adjusting by clicking somewhere on the screen & registering coords from there

'''

# INIT

root = tk.Tk()
# vision_load = Image.open('testpoint.png')

x1 = tk.StringVar(root, '898')
x2 = tk.StringVar(root, '951')
y1 = tk.StringVar(root, '807')
y2 = tk.StringVar(root, '821')

x1_i, y1_i, x2_i, y2_i = None, None, None, None


def handle_selection():
    main.capture()
    update_image()

    if state.get() == 0:
        main.active_can_buy = False
        main.active_cannot_buy = False
    elif state.get() == 1:
        main.active_can_buy = True
        main.active_cannot_buy = False
    elif state.get() == 2:
        main.active_can_buy = False
        main.active_cannot_buy = True
    else:
        print("Invalid state!")


def update_bbox(*args):
    # executed when entrybox value for coordinate is changed
    update_bbox_ints()
    main.bbox = [x1_i, y1_i, x2_i, y2_i]
    print(state.get())


def validate( text, *args):
    if text.isdigit() and text != " ":
        return True
    else:
        return False


def update_image():
    global vision_load, vision
    vision_load = Image.open('testpoint.png')
    vision_load = vision_load.resize((264, 64))
    vision = ImageTk.PhotoImage(vision_load)
    vision_label.config(image=vision)


def main_loop():
    # any continuous code goes here
    # print(main.active_cannot_buy, main.active_can_buy)
    root.after(1000, main_loop)


def update_bbox_ints():
    global x1_i, y1_i, x2_i, y2_i
    x1_i = int(x1.get())
    x2_i = int(x2.get())
    y1_i = int(y1.get())
    y2_i = int(y2.get())


root.attributes('-topmost', True)
root.resizable(False, False)

update_bbox_ints()

# 0 = off, 1 = on can buy, 0 = on cannot buy
state = tk.IntVar()

root.geometry("600x400")
root.title("Autofisher")

# TITLE / SUBTITLE

title = tk.Label(root, text="R", font=('Lato', 18))
title.pack(pady=10)

subtitle = tk.Label(root, text="!", font=('Lato', 12))
subtitle.pack()

# VISION WIDGET

vision_load = Image.open('testpoint.png')
vision_load = vision_load.resize((264, 64))

vision = ImageTk.PhotoImage(vision_load)
vision_label = tk.Label(root, image=vision)
vision_label.place(relx=0.98, rely=0.98, anchor=tk.SE)  # Place at the bottom right


vision_label_text = tk.Label(root, text="Vision", font=('Lato', 16))
vision_label_text.place(relx=0.8, rely=0.8, anchor=tk.SE)

# RADIO BUTTONS

radio_off = tk.Radiobutton(root, text="Off", variable=state, value=0, command=handle_selection)
radio_on_can_buy = tk.Radiobutton(root, text="On (Can sell)", variable=state, value=1, command=handle_selection)
radio_on_cannot_buy = tk.Radiobutton(root, text="On (Cannot sell)", variable=state, value=2, command=handle_selection)

radio_on_can_buy.pack(anchor='w', pady=20)
radio_on_cannot_buy.pack(anchor='w', pady=20)
radio_off.pack(anchor='w', pady=20)

# BOUNDING BOX -> 898, 807, 951, 821

validation = root.register(validate)

x1_entry_label = tk.Label(root, text="x1", font=("Lato", 10))
x1_entry_label.place(x=175, y=335)
x1_entry = tk.Entry(root, validatecommand=(validation, "%P"), validate="key", width=5, textvariable=x1)
x1_entry.place(x=200, y=335)
x1.trace("w", update_bbox)

x2_entry_label = tk.Label(root, text="x2", font=("Lato", 10))
x2_entry_label.place(x=175, y=365)
x2_entry = tk.Entry(root, validatecommand=(validation, "%P"), validate="key", width=5, textvariable=x2)
x2_entry.place(x=200, y=365)
x2.trace("w", update_bbox)

y1_entry_label = tk.Label(root, text="y1", font=("Lato", 10))
y1_entry_label.place(x=250, y=335)
y1_entry = tk.Entry(root, validatecommand=(validation, "%P"), validate="key", width=5, textvariable=y1)
y1_entry.place(x=275, y=335)
y1.trace("w", update_bbox)

y2_entry_label = tk.Label(root, text="y2", font=("Lato", 10))
y2_entry_label.place(x=250, y=365)
y2_entry = tk.Entry(root, validatecommand=(validation, "%P"), validate="key", width=5, textvariable=y2)
y2_entry.place(x=275, y=365)
y2.trace("w", update_bbox)


if __name__ == '__main__':

    # LOOP
    main.timer(root)

    logic_thread = threading.Thread(target=main.main)
    logic_thread.start()

    print('Passed thread')

    root.after(1000, main_loop)
    root.mainloop()
