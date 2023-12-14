import pyautogui
import time
from pynput.mouse import Controller, Button

mouse = Controller()


def press_left():
    mouse.position = pyautogui.position()
    mouse.press(Button.left)
    time.sleep(0.1)


def release_left():
    mouse.position = pyautogui.position()
    mouse.release(Button.left)


def press_right():
    mouse.position = pyautogui.position()
    mouse.press(Button.right)
    time.sleep(0.1)


def release_right():
    mouse.position = pyautogui.position()
    mouse.release(Button.right)


def click_right():
    mouse.position = pyautogui.position()
    mouse.press(Button.right)
    mouse.release(Button.right)


def click_left():
    mouse.position = pyautogui.position()
    mouse.press(Button.left)
    mouse.release(Button.left)
