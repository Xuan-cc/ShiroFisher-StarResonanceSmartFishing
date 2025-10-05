import os
import cv2
import keyboard
from datetime import datetime, timedelta
import pyautogui
import time
import numpy as np
from fish.modules.utils import (find_game_window, switch_to_window_by_title ,
                                 debug_screenshot_data , fish_area_cac)
from fish.modules.fishing_logic import (
    init_clicker,get_clicker, youganma, jinlema, shanggoulema, fishing_choose,
    diaoyuchong, diaodaole, PlayerCtl, SolveDaySwitch
)
from fish.modules.logger import logger

STOP_HOUR = 8
STOP_MINUTE = 0
pyautogui.FAILSAFE = True

def should_stop():
    """检查当前时间是否达到停止时间"""
    now = datetime.datetime.now()
    if now.hour >= STOP_HOUR and now.minute >= STOP_MINUTE:
        return True
    return False

def fish_init():
    print("欢迎使用星痕共鸣自动钓鱼脚本,本脚本识别16:9的游戏窗口~")
    print("Tip1:请确保游戏已经进入钓鱼界面!")
    print("Tip2:本脚本默认用光所有鱼竿和鱼饵后才会补全")
    print("Tip3:如果使用过程中发现无限左键了，请把鼠标移动至屏幕左上角自动结束左键连点，然后按F6停止脚本")
    print("请选择是自动补充神话鱼饵还是普通鱼饵(默认为神话鱼饵):")
    print("0.普通鱼饵 1.神话鱼饵")
    choice = input("输入后Enter确认:")
    fishing_choose(choice)
    print("接下来按F5键开始脚本把~,记得长按F6键是停止脚本！")
    # print(f"{g_current_dir}")
    while True:
        if keyboard.is_pressed('F5'):
            print("脚本开始运行")
            break
        time.sleep(0.05)
    init_clicker()
    switch_to_window_by_title("星痕共鸣")

def fish_reset(press1 = None,press2 = None):
    "无输入时冷启动，有输入时增加跨日重启功能"
    switch_to_window_by_title("星痕共鸣")
    # 尝试点击跨日刀问题
    if(press1 is not None and press2 is not None):
        SolveDaySwitch(press1,press2)
    #重新读取窗口,保证已切换至星痕共鸣窗口再截图
    print("尝试获取钓鱼状态窗口")
    pyautogui.sleep(1)
    gamewindow = None
    couter = 0
    while gamewindow is None:
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gamewindow = find_game_window(screenshot_cv,"fish")
        couter += 1
        if couter > 10:
            print("获取钓鱼状态窗口失败，请确保游戏已经进入钓鱼界面")
            return None
    # 计算各个检测区域
    yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_area_cac(gamewindow)
    debug_screenshot_data(screenshot_cv,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind)
    return gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind
    
def fish_porgress():
    print("脚本运行中...")
    logger.info("脚本运行中...")
    gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_reset()
    while gamewindow is None:
            return
    # 主循环
    status = 0
    fishcounter = 0
    timeout = timedelta(minutes=0, seconds=30)
    start_time = datetime.now()
    last_outdate_counter = 0
    clicker = get_clicker()
    while True:
        if keyboard.is_pressed('F6'):
            clicker.stop_clicking()
            pyautogui.keyUp('A')
            pyautogui.keyUp('D')
            pyautogui.mouseUp(button='left')
            print("✅ 检测到 F6 键，停止脚本")
            return print(f"✅ 脚本已停止，本次共钓上{fishcounter}条鱼")
        current_time = datetime.now()
        elapsed = current_time - start_time
        # 如果已经超过30秒，重置计时
        if elapsed > timeout:
            switch_to_window_by_title("星痕共鸣")
            print("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
            logger.debug("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
            if last_outdate_counter > 3:
                print("⚠️ 超过2分钟没动多半是跨日刀来了/出大问题了，强制重启模式")
                logger.critical("⚠️ 超过2分钟没动多半是跨日刀来了/出大问题了，强制重启模式")
                gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_reset(jixufind,shanggoufind)
                status = 0
                start_time = datetime.now()
                continue
            if jinlema(yugan):
                last_outdate_counter += 1
                start_time = datetime.now()
                print("🐟 仍旧在钓鱼一切正常")
                #检查是否还在钓鱼界面,如果还在就不管
                pass
            else:
                # 不在钓鱼界面，检查是否鱼已上钩
                if(diaodaole(gamewindow)): 
                    print("🐟 检测到鱼已上钩，但超时未处理，重新检测")
                else:
                    print("❌ 超时且不在钓鱼界面，也没有鱼上钩，重新启动流程")
                    logger.error("❌ 超时且不在钓鱼界面，也没有鱼上钩，重新启动流程")
                status = 0
                start_time = datetime.now()

            
        if status == 0:
            clicker.stop_clicking()
            start_time = datetime.now()
            if youganma(yugan, yuer):   
                PlayerCtl.leftmouse(1)
                print("🎯 甩杆结束。")
                status = 1
            else:
                logger.debug("❌ 无杆/饵，尝试购买")
        elif status == 1:
            clicker.stop_clicking()
            if jinlema(yugan):
                print("✅ 已成功甩杆进入钓鱼界面。")
                status = 2
            else:
                print("❌ 甩杆失败，重新尝试甩杆")
                status = 0
        elif status == 2:
            clicker.stop_clicking()
            if shanggoulema(shanggoufind, gamewindow):
                print("🎣 检测到鱼上钩了！准备钓鱼！")
                status = 3
        elif status == 3:
            if diaoyuchong(zuofind, youfind, jixufind, zhanglifind):
                print("🐟 成功钓上鱼！")
                fishcounter = fishcounter + 1
                print(f"🐠 当前已钓上 {fishcounter} 条鱼~")
                logger.info(f"🐠 当前已钓上 {fishcounter} 条鱼~")
                status = 4
        elif status == 4:
            clicker.stop_clicking()
            if diaodaole(gamewindow):
                print("✅ 鱼已收回，准备下一轮钓鱼\n\n")
                status = 0
                start_time = datetime.now()
                last_outdate_counter = 0
        # print(f"本轮钓鱼低【{looper}】轮检测已完成 - {datetime.datetime.now().strftime('%H:%M:%S')}")
        # print(f"\r\r")
        time.sleep(0.05)
def fish_main():
    try:
        fish_init()
        fish_porgress()
    except KeyboardInterrupt:
        print("\n用户中断脚本")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        pass

if __name__ == "__main__":
    fish_main()
