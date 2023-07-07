from pynput.mouse import Button, Controller
from PIL import ImageGrab, ImageStat, Image
import time
import threading
from pynput import keyboard
from ahk import AHK
import tkinter as tk
import gui

active_can_buy = False
active_cannot_buy = False
mouse_cast_position = (None, None)

# x1, y1, x2, y2
bbox = [898, 807, 951, 821]

mouse = Controller()
kb = keyboard.Controller()
ahk = AHK(executable_path=r"C:\Program Files\AutoHotkey\AutoHotkey.exe") # THIS NEEDS CHANGING!

# cast_time = 4.5 - (gui.hook_speed_level * 0.02)
cast_time = 3.5
sell_time = 1200


def on_press(key):
    global active_cannot_buy
    global active_can_buy
    global mouse_cast_position

    try:
       x = key.char

    except AttributeError:
        if key == keyboard.Key.f1:
            print("Toggling active (CAN buy)")
            active_can_buy = not active_can_buy if active_cannot_buy is False else False

        if key == keyboard.Key.f2:
            print("Toggling active (CANNOT buy)")
            active_cannot_buy = not active_cannot_buy if active_can_buy is False else False

        if key == keyboard.Key.f3:
            mouse_cast_position = mouse.position

        if key == keyboard.Key.f4:
            sell()


def capture() -> Image:
    # NEW pos (898, 807, 951, 821)

    img = ImageGrab.grab(bbox=(bbox[0], bbox[1], bbox[2], bbox[3]))
    img.save(f'testpoint.png')

    return img


def sell():
    print("THIS IS NOT TK_SELL()!")
    global mouse_cast_position, active_can_buy, active_cannot_buy

    if active_can_buy:
        frozen_state_can_buy = active_can_buy
        frozen_state_cannot_buy = active_cannot_buy

        active_can_buy = False
        active_cannot_buy = False

        kb.press('e')
        kb.release('e')

        time.sleep(2)
        ahk.mouse_move(1377, 582)

        time.sleep(2)
        mouse.click(Button.left, 1)

        time.sleep(1)
        ahk.mouse_move(1268, 430)
        mouse.click(Button.left, 1)

        time.sleep(1)
        ahk.mouse_move(1178, 421)
        mouse.click(Button.left, 1)

        time.sleep(1)
        mouse.click(Button.left, 1)

        time.sleep(0.25)
        ahk.mouse_move(mouse_cast_position[0], mouse_cast_position[1])

        time.sleep(0.25)

        active_can_buy = frozen_state_can_buy
        active_cannot_buy = frozen_state_cannot_buy

    timer()


def tk_sell(root: tk.Tk):
    global mouse_cast_position, active_can_buy, active_cannot_buy
    print("should be here!")
    gui.insert_console_text("Selling fish")

    if active_can_buy:
        frozen_state_can_buy = active_can_buy
        frozen_state_cannot_buy = active_cannot_buy

        active_can_buy = False
        active_cannot_buy = False

        kb.press('e')
        kb.release('e')

        root.after(2000)
        ahk.mouse_move(1377, 582)

        root.after(2000)
        mouse.click(Button.left, 1)

        root.after(1000)
        ahk.mouse_move(1268, 430)
        mouse.click(Button.left, 1)

        root.after(1000)
        ahk.mouse_move(1178, 421)
        mouse.click(Button.left, 1)

        root.after(1000)
        mouse.click(Button.left, 1)

        root.after(250)
        ahk.mouse_move(mouse_cast_position[0], mouse_cast_position[1])

        root.after(250)

        active_can_buy = frozen_state_can_buy
        active_cannot_buy = frozen_state_cannot_buy

    timer()
    gui.insert_console_text(f"Restarting timer; selling again in {sell_time}s")


def analyze(mean, root: tk.Tk = None):

    if [round(x) for x in mean] == [83.0, 250.0, 83.0]:
        print("Detected fish on, waiting")

    elif mean[0] > 80 and mean[1] > 240 and mean[2] > 80:
        print("Detected fish at threshold, clicking")
        mouse.click(Button.left, 1)

    elif [round(x) for x in mean] == [43, 43, 43]:
        print("Detected in IDE, passing")
        pass

    else:
        print("Detected not fishing, casting")
        if root:
            root.after(200)
            print("This should be getting run.")
        else:
            time.sleep(0.2)

        mouse.click(Button.left, 1)

        if root:
            root.after(cast_time)
        else:
            time.sleep(cast_time) # default 3.5

        mouse.click(Button.left, 1)

    return mean


def timer(root: tk.Tk = None):
    print("Starting timer")

    try:
        gui.insert_console_text("Starting/resetting timer")
    except NameError:
        pass

    thread = threading.Timer(sell_time, sell)
    thread.start()
    #if root:
    #    thread = threading.Timer(sell_time, tk_sell, args=root)
    #    thread.start()
    #else:

# (867, 818) --> test point
# [92.43589743589743, 250.28205128205127, 92.43589743589743] -> slight white
# [83.0, 250.0, 83.0] -> just green
# [181.21153846153845, 252.87179487179486, 181.21153846153845] -> half white

# (1371, 683) --> 'Sure' to Caster
# (1268, 430) --> 'Sell Everything'
# (1178, 421) --> 'Sell'
# Note: press mouse button 1 after selling to confirm!


def main(root: tk.Tk = None):
    while True:
        while active_can_buy or active_cannot_buy:
            colour_mean = ImageStat.Stat(capture()).mean

            if root is not None:
                print("we have root")
                gui.update_image()
                analyze(colour_mean, root)
            else:
                print("we do not have root")
                analyze(colour_mean)

            print(active_can_buy, active_cannot_buy)

            time.sleep(0.1)

        time.sleep(1)


if __name__ == '__main__':

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    timer()

    while True:
        main()
        time.sleep(1)
