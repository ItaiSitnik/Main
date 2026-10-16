import time

import pyautogui

pyautogui.click(x=810, y=995)

for i in range(10):
    # pyautogui.typewrite("@")
    pyautogui.typewrite(f"{i + 1}")
    # time.sleep(0.1)
    # for _ in range(i):
    #     pyautogui.press("down")
    #     time.sleep(0.1)
    pyautogui.press("enter")
    # pyautogui.press("enter")
    time.sleep(0.1)
