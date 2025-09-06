import pyautogui
import time
import keyboard
import sys
import time
from fish.modules.utils import (full_imagePath,get_suofang,switch_to_window_by_title,press_key,searchandmovetoclick)
# 设置pyautogui的安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

g_coords_kuaijie = {}
# 基准分辨率 (您提供的坐标基于此分辨率)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
def init_coords_kuaijie(gamewindow):
    x1 = int(gamewindow[0] + gamewindow[2] * 0.5 + gamewindow[2] * 200 / 1920)
    y1 = int(gamewindow[1] + gamewindow[3] * 0.5 - gamewindow[3] * 100 / 1080)

    x2 = int(gamewindow[0] + gamewindow[2] * 0.5 + gamewindow[2] * 793 / 1920)
    y2 = int(gamewindow[1] + gamewindow[3] * 0.5 + gamewindow[3] * 407 / 1080)

    x3 = int(gamewindow[0] + gamewindow[2] * 0.5 + gamewindow[2] * 220 / 1920)
    y3 = int(gamewindow[1] + gamewindow[3] * 0.5 + gamewindow[3] * 252 / 1080)

    x4 = int(gamewindow[0] + gamewindow[2] * 0.5 + gamewindow[2] * 220 / 1920)
    y4 = int(gamewindow[1] + gamewindow[3] * 0.5 + gamewindow[3] * 466 / 1080)
    global g_coords_kuaijie 
    g_coords_kuaijie = {"renwu": (x1, y1),"qiehuan": (x2, y2),"queding": (x3, y3),"zhuangbei": (x4, y4)}
    return g_coords_kuaijie

def KuaiSuZhuanZhi(gamewindow, screenshotname):
    print(f"KuaiSuZhuanZhi,{gamewindow}")
    """按键事件处理函数"""
    # suofang = get_suofang()
    pyautogui.keyUp('ctrl')
    press_key('c')
    pyautogui.sleep(0.5)
    pyautogui.moveTo(g_coords_kuaijie["renwu"])
    pyautogui.click()
    pyautogui.sleep(0.5)
    "选择职业"
    imagePath = full_imagePath(screenshotname)
    searchandmovetoclick(imagePath,0.9,0.1)
    pyautogui.sleep(0.1)
    "点击切换"
    pyautogui.moveTo(g_coords_kuaijie["qiehuan"])
    pyautogui.click()
    pyautogui.sleep(0.1)
    "点击确定*2"
    pyautogui.moveTo(g_coords_kuaijie["queding"])
    pyautogui.click()
    pyautogui.sleep(0.4)
    pyautogui.click()
    pyautogui.sleep(0.5)
    "装备武器"
    pyautogui.moveTo(g_coords_kuaijie["zhuangbei"])
    pyautogui.click()
    "不退出 为了避免战斗中无法切换这样你可以自己多点点"
    # pyautogui.sleep(0.2)
    # press_key('ESC')
    # pyautogui.sleep(0.2)
    # press_key('ESC')
    # pyautogui.sleep(0.2)
    # press_key('ESC')



if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        print("程序被用户中断")
        sys.exit(0)
    except pyautogui.FailSafeException:
        print("触发了安全故障保护（鼠标移动到屏幕角落）")
        sys.exit(0)