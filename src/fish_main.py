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
from fish.modules.locate import GetSysLang,InitSysLang,GetCnLang

STOP_HOUR = 8
STOP_MINUTE = 0
pyautogui.FAILSAFE = True
FishMainLangFlag = True # True为中文，False is English
logger = None
clicker = None
class FishMainStatus:
    """游戏窗口类"""
    def __init__(self):
        self.startTime = datetime.now()
        self.timeOutTimes = 0
        self.resetFlag = True
        self.gamewindow = None
        self.FishStopFlag = False
        self.FishPauseFlag = False
        self.yuer = None
        self.yugan = None
        self.shanggoufind = None
        self.zuofind = None
        self.youfind = None
        self.jixufind = None
        self.zhanglifind = None
        self.status = 0
        self.fishCounter = 0
        self.lastkey = None
        self.delayTimes = 0.06
    def addDelayTimes(self):
        if(self.delayTimes < 1):
            self.delayTimes += 0.05
            if(FishMainLangFlag):
                print(f"循环时间加长,当前循环时间{self.delayTimes:.2f}s!")
            else:
                print("Delay time is extended")
                print(f"Current delay time{self.delayTimes:.2f}s!")
        else:
            if(FishMainLangFlag):
                print(f"循环时间不能太长,当前循环时间{self.delayTimes:.2f}s!")
            else:
                print("Delay time is too long")
                print(f"Current delay time{self.delayTimes:.2f}s!")
    def subDelayTimes(self):
        if(self.delayTimes > 0.05):
            self.delayTimes -= 0.05
            if(FishMainLangFlag):
                print(f"循环时间缩短,当前循环时间{self.delayTimes:.2f}s!")
            else:
                print("Delay time is shortened")
                print(f"Current delay time{self.delayTimes:.2f}s!")
        else:
            if(FishMainLangFlag):
                print(f"循环时间不能太短,当前循环时间{self.delayTimes:.2f}s!")
            else:
                print("Delay time is too short")
                print(f"Current delay time{self.delayTimes:.2f}s!")
    def setLastKey(self,key):
        self.lastkey = key
    def getLastKey(self):
        return self.lastkey
    def addFishCounter(self):
        self.fishCounter += 1
    def addTimeOutTimes(self):
        self.timeOutTimes += 1
    def resetTimeOutTimes(self):
        self.timeOutTimes = 0

    def setStartTime(self):
        self.startTime = datetime.now()
    def getTimeLag (self):
        return datetime.now() - self.startTime
    def setstatus(self,data):
        self.status = data
    def stop(self):
        self.FishStopFlag = True
    def pause(self):
        self.FishPauseFlag = True
    def run(self):
        self.FishPauseFlag = False
    def reload(self):
        #重新读取窗口,保证已切换至星痕共鸣窗口再截图
        SwitchToGame()
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
                return False
        # 计算各个检测区域
        self.setstatus(0)
        self.resetTimeOutTimes()
        self.gamewindow = gamewindow
        self.yuer,self.yugan,self.shanggoufind,self.zuofind,self.youfind,self.jixufind,self.zhanglifind = fish_area_cac(gamewindow)
        debug_screenshot_data(screenshot_cv,gamewindow,self.yuer,self.yugan,self.shanggoufind,self.zuofind,self.youfind,self.jixufind,self.zhanglifind)
        return True

g_FishMain = FishMainStatus()

def fish_InitLogger():
    global logger  
    logger = GetLogger()
def fish_InitClicker():
    global clicker
    clicker = get_clicker()

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
    InitFishLogicLang(mylang,GetCnLang())
    log_init()
def GuideInfomation():
    if FishMainLangFlag:
        print("欢迎使用星痕共鸣自动钓鱼脚本,本脚本识别16:9的游戏窗口~")
        print("Tip1:请确保游戏已经进入钓鱼界面!")
        print("Tip2:本脚本默认用光所有鱼竿和鱼饵后才会补全")
        print("Tip3:如果使用过程中发现无限左键了，请把鼠标移动至屏幕左上角自动结束左键连点，然后按F6停止脚本")
        print("Tip4:请保证你已经使用管理员模式打开脚本！\n请保证你已经使用管理员模式打开脚本！\n请保证你已经使用管理员模式打开脚本！")
        print("Tip5:你可以通过PageUp和PageDown来增加和减少检测时间，默认为0.06s")
        print("请选择是自动补充特制鱼饵还是普通鱼饵(默认为特制鱼饵):")
        print("0.普通鱼饵 普通魚餌 \n1.特制鱼饵 特質魚餌")
        choice = input("输入后Enter确认:")
        fishing_choose(choice)
        print("接下来按F5键开始脚本把~,记得长按F6键是暂停脚本，ESC是退出脚本！")
    else:
        print("\n\nWelcome to the Star Echo Fishing Script, this script recognizes 16:9 game windows~\n\n")
        print("Tip0:Please make sure you run this programme as administrator!")
        print("Tip0:Please make sure you run this programme as administrator!")
        print("Tip0:Please make sure you run this programme as administrator!")
        print("Tip1:Please make sure the game has entered the fishing interface!")
        print("Tip2:The script will automatically replenish myth fish bait after using all fish rods and bait")
        print("Tip3:If you find that the left key is infinite," \
        "\nplease move the mouse to the upper left corner of the screen to automatically end the left key," \
        "\n and then press [F6] to pause the script")
        print("Tip4:Ctrl + C in console can stop the script.")
        print("Tip5:You can use [PageUp] and [PageDown] to increase and decrease the detection time, the default is 0.06s\n\n")
        print("Please choose to automatically replenish Special fish bait or Regular bait (default Special fish bait):")
        print("0.Regular bait\n1.Special bait")
        choice = input("Enter after input:")
        fishing_choose(choice)
        print("Next, press [F5] to start the script, \nremember to [hold] [F6] to pause the script, \n [ESC] to escape the script!")

def fish_CleanEvent():
    clicker = get_clicker()
    clicker.stop_clicking()
    pyautogui.keyUp('A')
    pyautogui.keyUp('D')
    pyautogui.mouseUp(button='left')

def fish_KeyboardHandler(event):
    """按键事件处理函数"""
    key = event.name  # 获取按键名称（如 'a', 'esc', 'up'） 
    if key == 'page up':
        g_FishMain.addDelayTimes()
    elif key == 'page down':
        g_FishMain.subDelayTimes()

    if key == g_FishMain.getLastKey():
        return
    g_FishMain.setLastKey(key)
    # print(f"检测到按键: {key}")
    if event.event_type != 'down':
        return  # 只处理按键按下事件

    if key == 'f6' and g_FishMain.FishPauseFlag == False:
        fish_CleanEvent()
        g_FishMain.pause()
        if FishMainLangFlag:
            print("✅ 检测到 F6 键，暂停脚本")
            print("按F5键继续脚本,按ESC退出脚本")
        else:
            print("✅ Detected F6 key, pause script")
            print("Press [F5] to continue the script, press [ESC] to exit the script")
    elif key == 'f5' and g_FishMain.FishPauseFlag == True:
        if FishMainLangFlag:
            print("检测到 F5 键，开始脚本")
        else:
            print("✅ Detected F5 key, start script")
        g_FishMain.reload()
        g_FishMain.run()
    elif key == 'esc':
        fish_CleanEvent()
        if FishMainLangFlag:
            print("检测到 ESC 键，停止脚本")
        else:
            print("✅ Detected ESC key, stop script")
        g_FishMain.stop()

def fish_InitKeyboard():
    keyboard.on_press(fish_KeyboardHandler)

def fish_init():
    InitAllLang()
    GuideInfomation()
    # print(f"{g_current_dir}")
    while True:
        if keyboard.is_pressed('F5'):
            if FishMainLangFlag:
                print("脚本开始运行")
            else:
                print("The script is running")
            break
        time.sleep(0.05)
    init_clicker()
    SwitchToGame()
    fish_InitLogger()
    fish_InitClicker()
    fish_InitKeyboard()

def fish_reset():
    SwitchToGame()
    # 尝试点击跨日刀问题
    if(g_FishMain.zhanglifind is not None):
        resetCounter = 0
        while(resetCounter < 3):
            if SolveDaySwitch(g_FishMain.jixufind,g_FishMain.zhanglifind):
                break
            resetCounter += 1
        if resetCounter < 3:
            pass
        else:
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
            return False
    return g_FishMain.reload()

def fish_HardOutDate():
    if FishMainLangFlag:
        print("⚠️ 超过90秒没动多半是跨日刀来了/出大问题了，强制重启模式")
        logger.critical("⚠️ 超过90秒没动多半是跨日刀来了/出大问题了，强制重启模式")
    else:
        print("⚠️ More than 90 seconds have passed without moving, most likely the Monthly Pass has come or there is a big problem, force restart mode")
        logger.critical("⚠️ More than 90 seconds have passed without moving, most likely the Monthly Pass has come or there is a big problem, force restart mode")
    if fish_reset():
        g_FishMain.setstatus(0)
    else:
        g_FishMain.stop()
        if FishMainLangFlag:
            print("⚠️ 无法恢复至钓鱼界面，停止脚本")
        else:
            print("⚠️ Cant restore to fishing interface, stop script")
    
def fish_SoftOutDate():
    if FishMainLangFlag:
        print("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
        logger.debug("⏰ ⚠️ 超过30秒未结束钓鱼流程，强制检查状态...")
    else:
        print("⏰ ⚠️ More than 30 seconds have passed without ending the fishing process, force check status...")
        logger.debug("⏰ ⚠️ More than 30 seconds have passed without ending the fishing process, force check status...")
        
    if jinlema(g_FishMain.yugan):
        if FishMainLangFlag:
            print("🐟 仍在钓鱼中，继续等待")
            logger.debug("🐟 仍在钓鱼中，继续等待")
        else:
            print("🐟 Still fishing, continue waiting")
            logger.debug("🐟 Still fishing, continue waiting")
        #检查是否还在钓鱼界面,如果还在就不管
        return False
    else:
        # 不在钓鱼界面，检查是否鱼已上钩
        if(diaodaolema(g_FishMain.jixufind)): 
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
        g_FishMain.setstatus(0)
        return True
    
def fish_StopData():
    if FishMainLangFlag:
        print(f"✅ 脚本已停止，本次共钓上{g_FishMain.fishCounter}条鱼")
    else:
        print(f"✅ The script has been stopped, {g_FishMain.fishCounter} fish have been caught this time")

def fish_ProgressDefault():
    clicker.stop_clicking()
    if youganma(g_FishMain.yugan, g_FishMain.yuer):   
        PlayerCtl.leftmouse(1)
        if FishMainLangFlag:
            print("🎯 甩杆中...")
        else:
            print("🎯 Throwing a rod...")
        g_FishMain.setstatus(1)
    else:
        if FishMainLangFlag:
            logger.debug("❌ 无杆/饵，尝试购买")
        else:
            logger.debug("❌ No rod or bait, try to buy")

        
def fish_ProgressCheckMiniGameStart():
    clicker.stop_clicking()
    if jinlema(g_FishMain.yugan):
        "已进入钓鱼才算循环开始,避免其实在无限甩杆"
        g_FishMain.setStartTime()
        if FishMainLangFlag:
            print("✅ 已成功甩杆进入钓鱼界面。")
        else:
            print("✅ Successfully threw a rod into the fishing interface.")
        g_FishMain.setstatus(2)
    else:
        if FishMainLangFlag:
            print("❌ 甩杆失败，重新尝试甩杆")
        else:
            print("❌ Failed to throw a rod, try again")
        g_FishMain.setstatus(0)

def fish_ProgressCheckHook():
    clicker.stop_clicking()
    if shanggoulema(g_FishMain.shanggoufind, g_FishMain.gamewindow):
        if FishMainLangFlag:
            print("🎣 检测到鱼上钩了！准备钓鱼！")
        else:
            print("🎣 Detected that the fish has been hooked! Ready to fish!")
        g_FishMain.setstatus(3)

def fish_ProgressFishing():
    if diaoyuchong(g_FishMain.zuofind,
                    g_FishMain.youfind,
                    g_FishMain.jixufind,
                    g_FishMain.zhanglifind):
        g_FishMain.addFishCounter()
        if FishMainLangFlag:
            print("🎣 鱼已收回，准备下一轮钓鱼\n\n")
            print(f"🐠 当前已钓上 {g_FishMain.fishCounter} 条鱼~")
            logger.info(f"🐠 当前已钓上 {g_FishMain.fishCounter} 条鱼~")
        else:
            print("🎣 The fish has been reeled in, ready for the next round of fishing\n\n")
            print(f"🐠 Currently caught {g_FishMain.fishCounter} fish~")
            logger.info(f"🐠 Currently caught {g_FishMain.fishCounter} fish~")
        g_FishMain.setstatus(4)

def fish_ProgressFinishied():
    clicker.stop_clicking()
    if diaodaole():
        lag = g_FishMain.getTimeLag()
        if FishMainLangFlag:
            print(f"✅ 鱼已收回，本轮钓鱼花费{lag}s，准备下一轮钓鱼\n\n")
        else:
            print(f"✅ The fish has been reeled in, this round of fishing took {lag}s, ready for the next round of fishing\n\n")
        g_FishMain.setstatus(0)
        g_FishMain.setStartTime()
        g_FishMain.resetTimeOutTimes()

g_FishFunctionDic = {
    0:fish_ProgressDefault,
    1:fish_ProgressCheckMiniGameStart,
    2:fish_ProgressCheckHook,
    3:fish_ProgressFishing,
    4:fish_ProgressFinishied
}

def fish_porgress():
    """
    钓鱼主函数，根据语言设置显示不同的钓鱼提示信息，并执行钓鱼主循环
    包含超时处理、停止标志检查和状态切换等功能
    """
    if FishMainLangFlag:
        print("正在钓鱼中...")  # 根据语言标志显示中文提示
        logger.info("正在钓鱼中...")  # 记录中文日志
    else:
        print("Fishing in progress...")  # 根据语言标志显示英文提示
        logger.info("Fishing in progress...")  # 记录英文日志
    
    if g_FishMain.reload() is not True:  # 尝试重新加载，如果失败则返回
            return
    # 主循环 - 处理钓鱼过程中的各种状态和事件
    timeout = timedelta(minutes=0, seconds=30)  # 设置超时时间为30秒
    g_FishMain.setStartTime()  # 记录开始时间
    g_FishMain.resetTimeOutTimes()  # 重置超时次数
    while True:
        # fish_KeyboardStopScript()  # 键盘停止脚本功能（已注释）
        # 如果已经超过30秒，重置计时
        if g_FishMain.FishStopFlag:
            fish_StopData()
            return
        if g_FishMain.FishPauseFlag:
            g_FishMain.setStartTime()
            continue
        if g_FishMain.getTimeLag() > timeout:
            g_FishMain.setStartTime()
            SwitchToGame()
            if fish_SoftOutDate():
                g_FishMain.resetTimeOutTimes()
            if g_FishMain.timeOutTimes >= 3:
                fish_HardOutDate()
                g_FishMain.resetTimeOutTimes()
            g_FishMain.addTimeOutTimes()

        g_FishFunctionDic[g_FishMain.status]()

        time.sleep(g_FishMain.delayTimes)

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
