import pyautogui
import math
from fish.modules.utils import precise_sleep


class PlayerCtl:
    def leftmouse(seconds):
        pyautogui.mouseDown()
        precise_sleep(seconds)
        pyautogui.mouseUp()

    def right(seconds):
        pyautogui.keyDown('D')
        precise_sleep(seconds)
        pyautogui.keyUp('D')

    def left(seconds):
        pyautogui.keyDown('A')
        precise_sleep(seconds)
        pyautogui.keyUp('A')
    
    def up(seconds):
        pyautogui.keyDown('W')
        precise_sleep(seconds)
        pyautogui.keyUp('W')
    
    def down(seconds):
        pyautogui.keyDown('S')
        precise_sleep(seconds)
        pyautogui.keyUp('S')

    def upright(seconds):
        pyautogui.keyDown('D')
        pyautogui.keyDown('W')
        precise_sleep(seconds)
        pyautogui.keyUp('W')
        pyautogui.keyUp('D')

    def upleft(seconds):
        pyautogui.keyDown('A')
        pyautogui.keyDown('W')
        precise_sleep(seconds)
        pyautogui.keyUp('W')
        pyautogui.keyUp('A')

    def downright(seconds):
        pyautogui.keyDown('D')
        pyautogui.keyDown('S')
        precise_sleep(seconds)
        pyautogui.keyUp('S')
        pyautogui.keyUp('D')

    def downleft(seconds):
        pyautogui.keyDown('A')
        pyautogui.keyDown('S')
        precise_sleep(seconds)
        pyautogui.keyUp('S')
        pyautogui.keyUp('A')