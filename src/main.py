import os
import cv2
import keyboard
from datetime import datetime, timedelta
import pyautogui
import time
import numpy as np
import fish_main as fish
import fuben_main as fuben
import kuaijie_main as kuaijie

STOP_HOUR = 8
STOP_MINUTE = 0
pyautogui.FAILSAFE = True


def should_stop():
    """检查当前时间是否达到停止时间"""
    now = datetime.datetime.now()
    if now.hour >= STOP_HOUR and now.minute >= STOP_MINUTE:
        return True
    return False

def select():
    print("请选择要执行的操作：")
    print("1. 开始钓鱼（默认）")
    print("2. 副本脚本")
    print("3. 一键切人")
    inputindex = input("请输入选项：")
    if(inputindex == "2"):
        fish.fish_main()
    elif(inputindex == "3"):
        kuaijie.kuaijie_main()
    else:
        fuben.fuben_main()

    input("按 Enter 键关闭控制台...")
if __name__ == "__main__":
    select()
