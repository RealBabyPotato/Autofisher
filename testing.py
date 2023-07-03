import pyautogui
from pynput.mouse import Controller

ms = Controller()

print(pyautogui.size())


while True:
    print(ms.position)
