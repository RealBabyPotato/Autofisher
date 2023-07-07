import threading
import tkinter as tk

import PIL

import main
from PIL import Image, ImageTk
import customtkinter as ctk
import time

'''

TODO:
<<<<<<< HEAD
(O) Basic GUI
(O) Display vision bbox area, allow adjusting 
(O) Console w/ status updates (detected fishing, detected ...)
(O) If previous state was detected fish on and current state is detected not fishing then
(O) - Adjust cast time based off of hook speed level
- Adjust sell time based off of bag size
immediately click to speed up fishing process
- Set cast position timer; click button -> button changes colour -> click anywhere on screen & register mouse pos
- If detected 3 fishing in a row, deactivate fishing
? Show time until next sell
- Keep a profile of preferred settings
? Allow bbox adjusting by clicking somewhere on the screen & registering coords from there
- Kill thread after gui closes
- Prevent user from putting in invalid coords
- Say "try moving your camera to a darker spot (make sure vision is not displaying white)" if detected fish at threshold multiple times in a row &
stop clicking mouse

'''


def handle_selection():
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


def validate(text, *args):
    if text.isdigit() or text == "":
        return True
    else:
        return False


def level_validate(inp, *args):
    if inp.isdigit() and 0 < int(inp) <= 70:
        return True
    else:
        return False


def update_image():
    global vision_load, vision
    main.capture()
    try:
        vision_load = Image.open('testpoint.png')
        vision_load = vision_load.resize((264, 64))
        vision = ImageTk.PhotoImage(vision_load)
        vision_label.config(image=vision)
    except PIL.UnidentifiedImageError:
        insert_console_text("Something went wrong displaying 'Vision'. The program should still be working normally.")


def main_loop():
    # any continuous code goes here
    if state.get() == 1 or state.get() == 2:
        update_image()

    root.after(200, main_loop)


def update_bbox_ints():
    global x1_i, y1_i, x2_i, y2_i, state
    try:
        x1_i = int(x1.get())
        x2_i = int(x2.get())
        y1_i = int(y1.get())
        y2_i = int(y2.get())

    except ValueError:
        x1_i, x2_i, y1_i, y2_i= 0, 1, 0, 1
        state.set(0)


def update_setting_ints(*args):
    global hook_speed_level_i

    try:
        hook_speed_level_i = int(hook_speed_level.get())
        main.cast_time = 4.5 - (hook_speed_level_i * 0.02)
    except ValueError:
        hook_speed_level_i = 50
        main.cast_time = 3.5


def insert_console_text(text):
    console.configure(state=tk.NORMAL)
    console.insert(tk.END, f"[{time.strftime('%H:%M')}]: {text}\n")
    console.configure(state=tk.DISABLED)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # INIT

    root = ctk.CTk()

    x1 = tk.StringVar(root, '898')
    x2 = tk.StringVar(root, '951')
    y1 = tk.StringVar(root, '807')
    y2 = tk.StringVar(root, '821')

    hook_speed_level = tk.IntVar(root, 50)

    x1_i, y1_i, x2_i, y2_i, hook_speed_level_i = None, None, None, None, 50

    root.attributes('-topmost', True)
    root.resizable(False, False)

    update_bbox_ints()

    # 0 = off, 1 = on can buy, 0 = on cannot buy
    state = tk.IntVar()

    root.geometry("500x300")
    root.title("Autofisher")

    # TITLE / SUBTITLE

    title = ctk.CTkLabel(root, text="Autofisher v1", font=('Corbel light', 24))
    title.pack(pady=5)

    subtitle = ctk.CTkLabel(root, text="By @cityofgod. on Discord!", font=('Corbel light', 18))
    subtitle.pack()

    # VISION WIDGET

    vision_load = Image.open('testpoint.png')
    vision_load = vision_load.resize((316, 86))

    vision = ImageTk.PhotoImage(vision_load)
    vision_label = tk.Label(root, image=vision, width=220, height=55)
    vision_label.place(relx=1, rely=0.98, anchor=tk.SE)  # Place at the bottom right

    vision_label_text = ctk.CTkLabel(root, text="Vision", font=('Corbel light', 20))
    vision_label_text.place(relx=0.8, rely=0.775, anchor=tk.SE)

    # RADIO BUTTONS

    radio_off = ctk.CTkRadioButton(root, text="Off", variable=state, value=0, command=handle_selection, font=('Corbel light', 18))
    radio_on_can_buy = ctk.CTkRadioButton(root, text="Fish", variable=state, value=1, command=handle_selection, font=('Corbel light', 18))
    radio_on_cannot_buy = ctk.CTkRadioButton(root, text=f"Fish + Sell (Sell frequency: {main.sell_time}s)", variable=state, value=2, command=handle_selection, font=('Corbel light', 18))

    radio_on_can_buy.pack(anchor='w', pady=10, padx=5)
    radio_on_cannot_buy.pack(anchor='w', pady=10, padx=5)
    radio_off.pack(anchor='w', pady=10, padx=5)

    # BOUNDING BOX -> 898, 807, 951, 821

    validation = root.register(validate)
    level_validation = root.register(level_validate)

    x1_entry_label = ctk.CTkLabel(root, text="x1:", font=("Corbel light", 14))
    x1_entry_label.place(relx=0.3375, rely=0.885, anchor=tk.SE)
    x1_entry = ctk.CTkEntry(root, validatecommand=(validation, "%P"), validate="key", width=38, border_width=0, textvariable=x1, font=("Corbel light", 16))
    x1_entry.place(relx=0.42, rely=0.885, anchor=tk.SE)
    x1.trace("w", update_bbox)

    x2_entry_label = ctk.CTkLabel(root, text="x2:", font=("Corbel light", 14))
    x2_entry_label.place(relx=0.4575, rely=0.885, anchor=tk.SE)
    x2_entry = ctk.CTkEntry(root, validatecommand=(validation, "%P"), validate="key", width=38, border_width=0, textvariable=x2, font=("Corbel light", 16))
    x2_entry.place(relx=0.54, rely=0.885, anchor=tk.SE)
    x2.trace("w", update_bbox)

    y1_entry_label = ctk.CTkLabel(root, text="y1:", font=("Corbel light", 14))
    y1_entry_label.place(relx=0.3375, rely=0.995, anchor=tk.SE)
    y1_entry = ctk.CTkEntry(root, validatecommand=(validation, "%P"), validate="key", width=38, border_width=0, textvariable=y1, font=("Corbel light", 16))
    y1_entry.place(relx=0.42, rely=0.99, anchor=tk.SE)
    y1.trace("w", update_bbox)

    y2_entry_label = ctk.CTkLabel(root, text="y2:", font=("Corbel light", 14))
    y2_entry_label.place(relx=0.4575, rely=0.995, anchor=tk.SE)
    y2_entry = ctk.CTkEntry(root, validatecommand=(validation, "%P"), validate="key", width=38, border_width=0, textvariable=y2, font=("Corbel light", 16))
    y2_entry.place(relx=0.54, rely=0.99, anchor=tk.SE)
    y2.trace("w", update_bbox)

    # SETTINGS

    hook_speed_label = ctk.CTkLabel(root, text="Hook Speed Level:", font=("Corbel light", 14))
    hook_speed_label.place(x=5, y=270)
    hook_speed_entry = ctk.CTkEntry(root, validatecommand=(level_validation, "%P"), validate="key", width=30, border_width=0, textvariable=hook_speed_level, font=("Corbel light", 16))
    hook_speed_entry.place(x=110, y=269)
    hook_speed_level.trace("w", update_setting_ints)

    # CONSOLE

    console = ctk.CTkTextbox(root, font=('Courier new', 11), width=225, height=125, corner_radius=5, state=tk.DISABLED)
    console.place(x=275, y=80)

    # LOOP
    main.timer(root)

    logic_thread = threading.Thread(target=main.main)
    logic_thread.start()

    insert_console_text(f"This is the console.")

    root.after(1000, main_loop)
    root.mainloop()
    state = 0
