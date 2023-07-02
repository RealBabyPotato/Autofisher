import pynput.keyboard
from pynput.mouse import Button, Controller
import time
import random
from ahk import AHK

kb = pynput.keyboard.Controller()
mouse = Controller()

ahk = AHK(executable_path=r"C:\Program Files\AutoHotkey\AutoHotkey.exe")

#kb.press('e')
#kb.release('e')


def move_mouse_smoothly(x, y, duration):
    start_x, start_y = mouse.position
    end_x, end_y = x, y
    start_time = time.time()

    while time.time() - start_time <= duration:
        elapsed_time = time.time() - start_time
        progress = min(elapsed_time / duration, 1.0)
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        mouse.position = (current_x, current_y)

    # Set the final position to ensure accuracy
    mouse.position = (end_x, end_y)

# Usage example
#target_x = 500
#target_y = 300
#duration = 2  # in seconds

#move_mouse_smoothly(target_x, target_y, duration)


time.sleep(2)
ahk.mouse_move(x=82, y=476)
time.sleep(1)
ahk.click()
# move_mouse_smoothly(1377, 582, 1)
#move_mouse_smoothly(82, 476, 1)
#time.sleep(0.25)
#mouse.move(10, 10)
#time.sleep(0.25)
#mouse.click(Button.left)

'''from pyautogui import *
import pyautogui
import time
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #uses time api, to simulate normal input.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)'''