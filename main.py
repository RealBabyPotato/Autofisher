from pynput.mouse import Button, Controller
from PIL import ImageGrab, ImageStat, Image
import time
import threading
from playsound import playsound
from pynput import keyboard
from ahk import AHK
import gui

active_can_buy = False
active_cannot_buy = False
mouse_cast_position = (None, None)

mouse = Controller()
kb = keyboard.Controller()
ahk = AHK(executable_path=r"C:\Program Files\AutoHotkey\AutoHotkey.exe")


def ding():
    try:
        playsound(r'C:\Users\jlamb\PycharmProjects\Autofisher\ding.mp3')
    except:
        print("Failed to play sound (try pressing the toggle button slower!)")


def on_press(key):
    global active_cannot_buy
    global active_can_buy
    global mouse_cast_position

    try:
       x = key.char

    except AttributeError:
        if key == keyboard.Key.f1:
            thread = threading.Thread(target=ding)
            thread.start()
            print("Toggling active (CAN buy)")
            active_can_buy = not active_can_buy if active_cannot_buy is False else False

        if key == keyboard.Key.f2:
            thread = threading.Thread(target=ding)
            thread.start()
            print("Toggling active (CANNOT buy)")
            active_cannot_buy = not active_cannot_buy if active_can_buy is False else False

        if key == keyboard.Key.f3:
            mouse_cast_position = mouse.position

        if key == keyboard.Key.f4:
            sell()


def capture():
    # OLD pos (898, 804, 951, 821)
    # NEW pos (898, 807, 951, 821)

    img = ImageGrab.grab(bbox=(898, 807, 951, 821))
    img.save(f'testpoint.png')
    return img


def sell():
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


def analyze(mean):

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
        mouse.click(Button.left, 1)
        time.sleep(3.5)
        mouse.click(Button.left, 1)

    return mean


def timer():
    print("Starting timer")
    thread = threading.Timer(1200, sell)
    thread.start()


# (867, 818) --> test point
# [92.43589743589743, 250.28205128205127, 92.43589743589743] -> slight white
# [83.0, 250.0, 83.0] -> just green
# [181.21153846153845, 252.87179487179486, 181.21153846153845] -> half white

# (1371, 683) --> 'Sure' to Caster
# (1268, 430) --> 'Sell Everything'
# (1178, 421) --> 'Sell'
# Note: press mouse button 1 after selling to confirm!

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    last_recorded_mean = [None, None, None]

    print("Press [f1] to toggle active (CAN buy/sell), [f2] to toggle active (CANNOT buy/sell), [f3] to set mouse casting position")

    timer()

    while True:

        while active_can_buy and mouse_cast_position != (None, None):
            colour_mean = ImageStat.Stat(capture()).mean
            analyze(colour_mean)

            time.sleep(0.1)

        while active_cannot_buy and mouse_cast_position != (None, None):
            colour_mean = ImageStat.Stat(capture()).mean
            analyze(colour_mean)

            time.sleep(0.1)

        if mouse_cast_position == (None, None):
            print("A mouse cast position has not been assigned. Press [f3] to assign one. ")

        time.sleep(1)
