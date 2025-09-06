import os
import cv2
import keyboard
from datetime import datetime, timedelta
import pyautogui
import time
import numpy as np
from fish.modules.utils import (find_game_window, switch_to_window_by_title ,
                                 debug_screenshot_data , area_cac ,debug_screenshot_coordinates)
from fish.modules.fuben_logic import(dina_main_loop,get_coords)
def fuben_select():
    "通过输入选择要打的副本，目前只有蒂娜"
    inputindex = input("请输入选项：")
    if(inputindex == "1"):
        return 1
    else:
        return 0

fuben_dict = {
    1: dina_main_loop,
    2: dina_main_loop,
    3: dina_main_loop
}
def default_function(gamewindow):
    dina_main_loop(gamewindow)

def fuben_main():
    print("欢迎使用星痕共鸣自动副本脚本,本脚本识别16:9的游戏窗口~")
    # print("Tip1:请确保游戏已经进入钓鱼界面!")
    # print("Tip2:本脚本默认用光所有鱼竿和鱼饵后才会补全")
    # print("Tip3:如果使用过程中发现无限Y左键了，请把鼠标移动至屏幕左上角自动结束左键连点，然后按F6停止脚本")
    # print("请选择是自动补充神话鱼饵还是普通鱼饵(默认为神话鱼饵):")
    # print("0.普通鱼饵 1.神话鱼饵")
    g_select = fuben_select()
    try:
        print("脚本运行中...")
        print("尝试获取游戏窗口")
        pyautogui.sleep(2)
        switch_to_window_by_title("星痕共鸣")
        pyautogui.sleep(1)
        gamewindow = None
        couter = 0
        while gamewindow is None:
            screenshot = pyautogui.screenshot()
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            gamewindow = find_game_window(screenshot_cv,"fuben")
            couter += 1
            if couter > 10:
                print("获取游戏窗口失败，请确保游戏已经进入正常界面")
                pyautogui.sleep(5)
                break
        
        # 计算各个检测区域
        yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = area_cac(gamewindow)
        debug_screenshot_data(screenshot_cv,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind)
        dir = get_coords(gamewindow[0], gamewindow[1]) # 获取坐标
        debug_screenshot_coordinates(screenshot_cv,dir)
        print("接下来按F12键开始脚本把~,记得长按F12键是停止脚本！")
        # 主循环
        fubencounter = 0
        while True:
            if keyboard.is_pressed('F12'):
                print("✅ 检测到 F12 键，停止脚本")
                break
            if g_select in fuben_dict:
                fuben_dict[g_select](gamewindow)
            else:
                default_function(gamewindow)
            
    except KeyboardInterrupt:
        print("\n用户中断脚本")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        print(f"✅ 脚本已停止，本次共进行{fubencounter}次副本")
        input("enter键退出")#临时使用
if __name__ == "__main__":
    fuben_main()