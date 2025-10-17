import os
import cv2
import keyboard
from datetime import datetime, timedelta
import pyautogui
import time
import numpy as np
from fish.modules.utils import (find_game_window, SwitchToGame, InitUnitLang,
                                 debug_screenshot_data,full_imagePath)
from fish.modules.fishing_logic import (
    init_clicker,get_clicker, youganma, jinlema, shanggoulema, fishing_choose,
    diaoyuchong, diaodaole,diaodaolema, PlayerCtl, SolveDaySwitch ,fish_area_cac,
    InitFishLogicLang
)
from fish.modules.logger import GetLogger ,log_init
from fish.modules.locate import GetSysLang,InitSysLang

STOP_HOUR = 8
STOP_MINUTE = 0
pyautogui.FAILSAFE = True
FishMainLangFlag = True # True为中文，False is English

def should_stop():
    """检查当前时间是否达到停止时间"""
    now = datetime.datetime.now()
    if now.hour >= STOP_HOUR and now.minute >= STOP_MINUTE:
        return True
    return False
def InitFishMainLang(mylang):
    global FishMainLangFlag
    if mylang == "zh":
        FishMainLangFlag = True
    else:
        FishMainLangFlag = False
def InitAllLang():
    InitSysLang()
    mylang = GetSysLang()
    InitFishMainLang(mylang)
    InitUnitLang(mylang)
    InitFishLogicLang(mylang)
    log_init()
def GuideInfomation():
    global FishMainLangFlag
    if FishMainLangFlag:
        print("欢迎使用星痕共鸣自动钓鱼脚本,本脚本识别16:9的游戏窗口~")
        print("Tip1:请确保游戏已经进入钓鱼界面!")
        print("Tip2:本脚本默认用光所有鱼竿和鱼饵后才会补全")
        print("Tip3:如果使用过程中发现无限左键了，请把鼠标移动至屏幕左上角自动结束左键连点，然后按F6停止脚本")
        print("请选择是自动补充神话鱼饵还是普通鱼饵(默认为神话鱼饵):")
        print("0.普通鱼饵 1.神话鱼饵")
        choice = input("输入后Enter确认:")
        fishing_choose(choice)
        print("接下来按F5键开始脚本把~,记得长按F6键是停止脚本！")
    else:
        print("\n\nWelcome to the Star Echo Fishing Script, this script recognizes 16:9 game windows~\n")
        print("Tip1:Please make sure the game has entered the fishing interface!")
        print("Tip2:The script will automatically replenish myth fish bait after using all fish rods and bait")
        print("Tip3:If you find that the left key is infinite," \
        "\nplease move the mouse to the upper left corner of the screen to automatically end the left key," \
        "\n and then press [F6] to stop the script")
        print("Tip4:Ctrl + C in console can stop the script.\n\n")
        print("Please choose to automatically replenish Special fish bait or Regular bait (default Special fish bait):")
        print("0.Regular bait\n1.Special bait")
        choice = input("Enter after input:")
        fishing_choose(choice)
        print("Next, press [F5] to start the script, \nremember to [hold] [F6] to stop the script!")

def fish_init():
    InitAllLang()
    GuideInfomation()
    # print(f"{g_current_dir}")
    while True:
        if keyboard.is_pressed('F5'):
            global FishMainLangFlag
            if FishMainLangFlag:
                print("脚本开始运行")
            else:
                print("The script is running")
            break
        time.sleep(0.05)
    init_clicker()
    SwitchToGame()

def fish_reset(press1 = None,press2 = None):
    "无输入时冷启动，有输入时增加跨日重启功能"
    SwitchToGame()
    global FishMainLangFlag
    # 尝试点击跨日刀问题
    if(press1 is not None and press2 is not None):
        resetCounter = 0
        while(resetCounter < 3):
            if SolveDaySwitch(press1,press2):
                break
            resetCounter += 1
        if resetCounter < 3:
            pass
        else:
            logger = GetLogger()
            stopScreenshot = pyautogui.screenshot()
            stopScreenshot_cv = cv2.cvtColor(np.array(stopScreenshot), cv2.COLOR_RGB2BGR)
            image_save_path = full_imagePath("debug_screenshot_stop.png")
            cv2.imwrite(image_save_path, stopScreenshot_cv)
            if FishMainLangFlag:
                print("已无法重置回正常MiniGame界面,强制停止脚本\n")
                logger.critical("已无法重置回正常MiniGame界面,强制停止脚本\n")
                print(f"debug截图已保存在{image_save_path}\n")
                logger.critical(f"debug截图已保存在{image_save_path}\n")
            else:
                print("Unable to reset to normal MiniGame interface, force stop script\n")
                logger.critical("Unable to reset to normal MiniGame interface, force stop script\n")
                print(f"Debug screenshot has been saved to {image_save_path}\n")
                logger.critical(f"Debug screenshot has been saved to {image_save_path}\n")
            return False,press1,press1,press1,press1,press1,press1,press1,press1
    #重新读取窗口,保证已切换至星痕共鸣窗口再截图

    if FishMainLangFlag:
        print("尝试获取钓鱼状态窗口")
    else:
        print("Try to get the fishing status window")
    pyautogui.sleep(2)
    gamewindow = None
    couter = 0
    while gamewindow is None:
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gamewindow = find_game_window(screenshot_cv,"fish")
        couter += 1
        if couter > 10:
            if FishMainLangFlag:
                print("获取钓鱼状态窗口失败，请确保游戏已经进入钓鱼界面")
            else:
                print("Failed to get the fishing status window, please make sure the game has entered the fishing interface")
            return None
    # 计算各个检测区域
    yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_area_cac(gamewindow)
    debug_screenshot_data(screenshot_cv,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind)
    return True,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind
    
def fish_porgress():
    global FishMainLangFlag
    logger = GetLogger()
    if FishMainLangFlag:
        print("正在钓鱼中...")
        logger.info("正在钓鱼中...")
    else:
        print("Fishing in progress...")
        logger.info("Fishing in progress...")
    restetFlag,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_reset()
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
            if FishMainLangFlag:
                print("✅ 检测到 F6 键，停止脚本")
                return print(f"✅ 脚本已停止，本次共钓上{fishcounter}条鱼")
            else:
                print("✅ Detected F6 key, stop script")
                return print(f"✅ The script has been stopped,\n{fishcounter} fish have been caught this time")
            
        current_time = datetime.now()
        elapsed = current_time - start_time
        # 如果已经超过30秒，重置计时
        if elapsed > timeout:
            SwitchToGame()
            last_outdate_counter += 1
            if FishMainLangFlag:
                print("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
                logger.debug("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
            else:
                print("⏰ ⚠️ More than 30 seconds have passed without ending the fishing process, force check status...")
                logger.debug("⏰ ⚠️ More than 30 seconds have passed without ending the fishing process, force check status...")
            if last_outdate_counter >= 3:
                if FishMainLangFlag:
                    print("⚠️ 超过90秒没动多半是跨日刀来了/出大问题了，强制重启模式")
                    logger.critical("⚠️ 超过90秒没动多半是跨日刀来了/出大问题了，强制重启模式")
                else:
                    print("⚠️ More than 90 seconds have passed without moving, most likely the Monthly Pass has come or there is a big problem, force restart mode")
                    logger.critical("⚠️ More than 90 seconds have passed without moving, most likely the Monthly Pass has come or there is a big problem, force restart mode")
                restetFlag,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind = fish_reset(jixufind,shanggoufind)
                if restetFlag:
                    status = 0
                    start_time = datetime.now()
                    continue
                else:
                    if FishMainLangFlag:
                        print("⚠️ 无法恢复至钓鱼界面，停止脚本")
                        return print(f"✅ 脚本已停止，本次共钓上{fishcounter}条鱼")
                    else:
                        print("⚠️ Cant restore to fishing interface, stop script")
                        return print(f"✅ The script has been stopped,\n{fishcounter} fish have been caught this time")

            if jinlema(yugan):
                start_time = datetime.now()
                if FishMainLangFlag:
                    print("🐟 仍在钓鱼中，继续等待")
                    logger.debug("🐟 仍在钓鱼中，继续等待")
                else:
                    print("🐟 Still fishing, continue waiting")
                    logger.debug("🐟 Still fishing, continue waiting")
                #检查是否还在钓鱼界面,如果还在就不管
                pass
            else:
                # 不在钓鱼界面，检查是否鱼已上钩
                if(diaodaolema(jixufind)): 
                    if FishMainLangFlag:
                        print("🐟 检测到鱼已上钩，但超时未处理，重新检测")
                        logger.debug("🐟 检测到鱼已上钩，但超时未处理，重新检测")
                    else:
                        print("🐟 Detected that the fish has been hooked, but it timed out and was not processed, re-checking")
                        logger.debug("🐟 Detected that the fish has been hooked, but it timed out and was not processed, re-checking")
                    diaodaole()
                else:
                    if FishMainLangFlag:
                        print("❌ 超时且不在钓鱼界面，也没有鱼上钩，重新启动流程")
                        logger.error("❌ 超时且不在钓鱼界面，也没有鱼上钩，重新启动流程")
                    else:
                        print("❌ Timeout and not in the fishing interface, no fish is hooked, restart the process")
                        logger.error("❌ Timeout and not in the fishing interface, no fish is hooked, restart the process")

                status = 0
                start_time = datetime.now()

            
        if status == 0:
            clicker.stop_clicking()
            if youganma(yugan, yuer):   
                PlayerCtl.leftmouse(1)
                if FishMainLangFlag:
                    print("🎯 甩杆中...")
                else:
                    print("🎯 Throwing a rod...")
                status = 1
            else:
                if FishMainLangFlag:
                    logger.debug("❌ 无杆/饵，尝试购买")
                else:
                    logger.debug("❌ No rod or bait, try to buy")
        elif status == 1:
            clicker.stop_clicking()
            if jinlema(yugan):
                "已进入钓鱼才算循环开始,避免其实在无限甩杆"
                start_time = datetime.now()
                if FishMainLangFlag:
                    print("✅ 已成功甩杆进入钓鱼界面。")
                else:
                    print("✅ Successfully threw a rod into the fishing interface.")
                status = 2
            else:
                if FishMainLangFlag:
                    print("❌ 甩杆失败，重新尝试甩杆")
                else:
                    print("❌ Failed to throw a rod, try again")
                status = 0
        elif status == 2:
            clicker.stop_clicking()
            if shanggoulema(shanggoufind, gamewindow):
                if FishMainLangFlag:
                    print("🎣 检测到鱼上钩了！准备钓鱼！")
                else:
                    print("🎣 Detected that the fish has been hooked! Ready to fish!")
                status = 3
        elif status == 3:
            if diaoyuchong(zuofind, youfind, jixufind, zhanglifind):
                fishcounter = fishcounter + 1
                if FishMainLangFlag:
                    print("🎣 鱼已收回，准备下一轮钓鱼\n\n")
                    print(f"🐠 当前已钓上 {fishcounter} 条鱼~")
                    logger.info(f"🐠 当前已钓上 {fishcounter} 条鱼~")
                else:
                    print("🎣 The fish has been reeled in, ready for the next round of fishing\n\n")
                    print(f"🐠 Currently caught {fishcounter} fish~")
                    logger.info(f"🐠 Currently caught {fishcounter} fish~")
                status = 4
        elif status == 4:
            clicker.stop_clicking()
            if diaodaole():
                if FishMainLangFlag:
                    print("✅ 鱼已收回，准备下一轮钓鱼\n\n")
                else:
                    print("✅ The fish has been reeled in, ready for the next round of fishing\n\n")
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
        if FishMainLangFlag:
            print("\n用户中断脚本")
        else:
            print("\nUser interrupted the script")
    except Exception as e:
        if FishMainLangFlag:
            print(f"发生错误: {e}")
        else:
            print(f"An error occurred: {e}")
    finally:
        pass

if __name__ == "__main__":
    fish_main()
