import os
import cv2
import keyboard
from datetime import datetime, timedelta
import pyautogui
import time
import numpy as np
from fish.modules.utils import (find_game_window, SwitchToGame ,debug_screenshot_coordinates)
from fish.modules.kuaijie_logic import(KuaiSuZhuanZhi,init_coords_kuaijie)

g_gamewindow = None
g_lastkey = None
def kuaijie_key_handler(event):
    """按键事件处理函数"""
    key = event.name  # 获取按键名称（如 'a', 'esc', 'up'） 
    global g_lastkey
    if key == g_lastkey:
        return
    g_lastkey = key
    print(f"检测到按键: {key}")
    if event.event_type != 'down':
        return  # 只处理按键按下事件
    is_ctrl_pressed = keyboard.is_pressed('ctrl')

    global g_gamewindow
    if is_ctrl_pressed and key == '0':
        print("检测到 Ctrl + 0，切换至灵魂乐手！")
        KuaiSuZhuanZhi(g_gamewindow, "linghunyueshou.png")
    elif is_ctrl_pressed and key == '-':
        print("检测到 Ctrl + -，切换至冰魔导师！")
        KuaiSuZhuanZhi(g_gamewindow, "bingmodaoshi.png")
    elif is_ctrl_pressed and key == '+':
        print("检测到 Ctrl + -，切换至森语者！")
        KuaiSuZhuanZhi(g_gamewindow, "senyuzhe.png")
    elif is_ctrl_pressed and key == '=':
        print("检测到 Ctrl + -，切换至神盾骑士！")
        KuaiSuZhuanZhi(g_gamewindow, "shendunqishi.png")
def kuaijie_main():
    print("欢迎使用星痕共鸣自动换人脚本,本脚本识别16:9的游戏窗口~")
    print("目前可用的功能为:")
    print("Ctrl + 0 切换至灵魂乐手")
    print("Ctrl + - 切换至冰魔导师")
    print("Ctrl + + 切换至森语者")
    print("Ctrl + = 切换至神盾骑士")
    print("即将启动！")
    # print("Tip1:请确保游戏已经进入钓鱼界面!")
    # print("Tip2:本脚本默认用光所有鱼竿和鱼饵后才会补全")
    # print("Tip3:如果使用过程中发现无限Y左键了，请把鼠标移动至屏幕左上角自动结束左键连点，然后按F6停止脚本")
    # print("请选择是自动补充神话鱼饵还是普通鱼饵(默认为神话鱼饵):")
    # print("0.普通鱼饵 1.神话鱼饵")
    try:
        
        print("尝试获取游戏窗口")
        time.sleep(1)
        SwitchToGame()
        time.sleep(1)
        global g_gamewindow
        couter = 0
        while g_gamewindow is None:
            screenshot = pyautogui.screenshot()
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            g_gamewindow = find_game_window(screenshot_cv,"fuben")
            couter += 1
            if couter > 10:
                print("获取游戏窗口失败，请确保游戏已经进入正常界面")
                pyautogui.sleep(5)
                break
        # 计算各个检测区域
        # yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = area_cac(g_gamewindow)
        # debug_screenshot_data(screenshot_cv,g_gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind)
        dir = init_coords_kuaijie(g_gamewindow) # 获取坐标
        debug_screenshot_coordinates(screenshot_cv,dir)
        # print("接下来按F12键开始脚本把~,记得长按F12键是停止脚本！")
        # 主循环
        keyboard.on_press(kuaijie_key_handler)
        print("已经开始监听...按F12停止监听")
        while True:
            if keyboard.is_pressed('F12'):
                print("✅ 检测到 F12 键，停止脚本")
                keyboard.unhook_all()
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n用户中断脚本")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        keyboard.unhook_all()
        input("按回车键退出脚本")
        pass
if __name__ == "__main__":
    kuaijie_main()