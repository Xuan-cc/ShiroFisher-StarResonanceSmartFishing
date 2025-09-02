import pyautogui
"目前未知原因无效"
class CameraCtl:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2

    def up(self, seconds):
        pyautogui.moveTo(self.center_x, self.center_y)
        pyautogui.moveRel(0, -1, duration=seconds)

    def left(self, seconds):
        pyautogui.moveTo(self.center_x, self.center_y)
        pyautogui.moveRel(-1, 0, duration=seconds)

    def right(self, seconds):
        pyautogui.moveTo(self.center_x, self.center_y)
        pyautogui.moveRel(1, 0, duration=seconds)

    def down(self, seconds):
        pyautogui.moveTo(self.center_x, self.center_y)
        pyautogui.moveRel(0, 1, duration=seconds)