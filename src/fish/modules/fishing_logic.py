import cv2
import pyautogui
import time
import threading
import numpy as np
import os
from .utils import find_pic, dirinfo2pyautoguiinfo, fuzzy_color_match ,full_imagePath,SwitchToGame,searchandmovetoclick,press_key,FindPicFromFullScreen
from .player_control import PlayerCtl,precise_sleep
from .logger import GetLogger
global g_yuer_type
g_yuer_type = 1 # 1为默认贵的，0为便宜的
clicker = None
global g_jixudiaoyu
g_jixudiaoyu = None
global FishLogicLangFlag
FishLogicLangFlag = True
def InitFishLogicLang(mylang):
    global FishLogicLangFlag
    if mylang == "zh":
        FishLogicLangFlag = True
    else:
        FishLogicLangFlag = False

def fishing_choose(idx):
    "用于给外部修改默认鱼饵类型"
    global g_yuer_type
    global FishLogicLangFlag
    if idx == "0":
        if FishLogicLangFlag:
            print(f"选择便宜鱼饵")
        else:
            print(f"Choose Regular bait")
        g_yuer_type = 0
    else:
        if FishLogicLangFlag:
            print("选择默认鱼饵")
        else:
            print("Choose Special bait")
        g_yuer_type = 1

class PreciseMouseClicker:
    def __init__(self, interval_ms=60, button='left', duration_ms=0):
        self.interval_ms = interval_ms
        self.button = button
        self.duration_ms = duration_ms
        self.is_clicking = False
        self.click_thread = None
        self.click_count = 0
        self.start_time = 0
    
    def start_clicking(self):
        if self.is_clicking:
            # print("点击已在运行中")
            return
        
        self.is_clicking = True
        self.click_count = 0
        self.start_time = time.perf_counter()
        self.click_thread = threading.Thread(target=self._precise_click_loop)
        self.click_thread.daemon = True
        self.click_thread.start()
        
        print(f"Starting to click {self.button} mouse button per {self.interval_ms}ms ")
        # print("按 Ctrl+C 停止点击")
    
    def stop_clicking(self):
        if not self.is_clicking:
            # print("点击未在运行中")
            return
        
        self.is_clicking = False
        if self.click_thread:
            self.click_thread.join(timeout=1.0)
        
        total_time = time.perf_counter() - self.start_time
        print(f"Stop Clicking，have clicked {self.click_count} times")
        # print(f"总运行时间: {total_time:.2f}秒")
        # print(f"平均点击频率: {self.click_count/total_time:.2f}次/秒")
    
    def _precise_click_loop(self):
        interval_sec = self.interval_ms / 1000.0
        duration_sec = self.duration_ms / 1000.0
        next_time = time.perf_counter()
        
        try:
            while self.is_clicking:
                if self.duration_ms > 0:
                    pyautogui.mouseDown(button=self.button)
                    time.sleep(duration_sec)
                    pyautogui.mouseUp(button=self.button)
                else:
                    pyautogui.click(button=self.button)
                
                self.click_count += 1
                next_time += interval_sec
                current_time = time.perf_counter()
                sleep_time = next_time - current_time
                
                if sleep_time > 0:
                    self._precise_sleep(sleep_time)
                else:
                    next_time = current_time + interval_sec
                    # print(f"警告: 点击延迟 {-sleep_time*1000:.2f}ms")
                    
        except pyautogui.FailSafeException:
            print("故障安全触发：鼠标移动到屏幕左上角")
            self.is_clicking = False
        except Exception as e:
            print(f"点击过程中发生错误: {e}")
            self.is_clicking = False
    
    def _precise_sleep(self, duration):
        end_time = time.perf_counter() + duration
        if duration > 0.02:
            time.sleep(duration - 0.01)
        while time.perf_counter() < end_time:
            pass

def find_game_window(screenshot_cv):
    image_path = full_imagePath("esc.png")
    logoinfo = find_pic(screenshot_cv, image_path, confidence = 0.8,type="A")
    print(f"Has found logoinfo :{logoinfo}")

    image_path = full_imagePath("rightdown.png")
    youxiainfo = find_pic(screenshot_cv, image_path,type="A")
    print(f"Has found youxiainfo:{youxiainfo}")

    if logoinfo is None or youxiainfo is None:
        return None
    
    left = logoinfo.get("left")
    top_left = (logoinfo.get("left"), logoinfo.get("top"))
    width = youxiainfo.get("left") + youxiainfo.get("width") - logoinfo.get("left")
    height = youxiainfo.get("top") + youxiainfo.get("height") - logoinfo.get("top")

    windowinfo = {
        'left': top_left[0],
        'top': top_left[1],
        'width': width,
        'height': height,
    }

    print(f"Has found Game window:{windowinfo}")
    return dirinfo2pyautoguiinfo(windowinfo)

def purchase(sth):
    trust = 0.8
    delay = 0.2
    pyautogui.keyDown("B")
    precise_sleep(0.5)
    pyautogui.keyUp("B")
    searchandmovetoclick("shop.png",trust,delay)
    if sth == 'gan':
        searchandmovetoclick("shop_gan.png",trust,delay)
    elif sth == 'er':
        if g_yuer_type:
            searchandmovetoclick("shop_er.png",trust,delay)
        else:
            searchandmovetoclick("shop_er_cheap.png",trust,delay)
    searchandmovetoclick("shop_num.png",trust,delay)
    searchandmovetoclick("shop_2.png",trust,delay)
    searchandmovetoclick("shop_0.png",trust,delay)
    searchandmovetoclick("shop_0.png",trust,delay)
    searchandmovetoclick("shop_OK.png",trust,delay)
    searchandmovetoclick("shop_buy.png",trust,delay)
    if sth == 'er':
        searchandmovetoclick("shop_yes.png",trust,delay)
    searchandmovetoclick("shop_x.png",trust,delay)
    global FishLogicLangFlag
    if FishLogicLangFlag:
        print("购买成功")
    else:
        print("Purchase Success")

def youganma(yugan, yuer):
    global FishLogicLangFlag
    clicker.stop_clicking()
    SwitchToGame()
    image_path = full_imagePath("nogan.png")
    yuganshot = pyautogui.screenshot(region=yugan)
    yuganshot_cv = cv2.cvtColor(np.array(yuganshot), cv2.COLOR_RGB2BGR)
    image_save_path = full_imagePath("yugan_screenshot.png")
    cv2.imwrite(image_save_path, yuganshot_cv)
    temp1 = find_pic(yuganshot_cv, image_path, confidence=0.8,type = "A")
    if temp1 is not None:
        if FishLogicLangFlag:
            print("❌ 鱼竿NOK")
        else:
            print("Fishing Pole NOK")
        pyautogui.keyDown("M")
        precise_sleep(0.5)
        pyautogui.keyUp("M")
        window = pyautogui.screenshot()
        window_cv = cv2.cvtColor(np.array(window), cv2.COLOR_RGB2BGR)
        image_path = full_imagePath("yong.png")
        temp = find_pic(window_cv, image_path, 0.80,type = "A")
        if temp is None:
            if FishLogicLangFlag:
                print("❌ 鱼竿已用完，尝试买杆")
            else:
                print("No Fishing Pole,try to buy")
            purchase('gan')
        else:
            data = dirinfo2pyautoguiinfo(temp)
            x = int(data[0] + 0.75 * data[2])
            y = int(data[1] + 0.5 * data[3])
            pyautogui.moveTo(x, y)
            PlayerCtl.leftmouse(0.5)
            precise_sleep(0.5)
        return 0
    if FishLogicLangFlag:
        print("✅ 鱼竿OK")
    else:
        print("Fishing Pole OK")
    yuershot = pyautogui.screenshot(region=yuer)
    yuershot_cv = cv2.cvtColor(np.array(yuershot), cv2.COLOR_RGB2BGR)
    image_save_path = full_imagePath("yuer_screenshot.png")
    cv2.imwrite(image_save_path, yuershot_cv)
    temp2 = find_pic(yuershot_cv, image_path, 0.80,type = "A")
    if temp2 is not None:
        if FishLogicLangFlag:
            print("❌ 鱼饵NOK")
        else:
            print("Bait NOK")
        pyautogui.keyDown("N")
        precise_sleep(0.5)
        pyautogui.keyUp("N")
        window = pyautogui.screenshot()
        window_cv = cv2.cvtColor(np.array(window), cv2.COLOR_RGB2BGR)
        image_path = full_imagePath("yong.png")
        temp = find_pic(window_cv, image_path, 0.80,type = "A")
        if temp is None:
            if FishLogicLangFlag:
                print("❌ 鱼饵已用完，尝试买饵")
            else:
                print("No Bait,try to buy")
            purchase('er')
        else:
            data = dirinfo2pyautoguiinfo(temp)
            x = int(data[0] + 0.75 * data[2])
            y = int(data[1] + 0.5 * data[3])
            pyautogui.moveTo(x, y)
            PlayerCtl.leftmouse(0.5)
            precise_sleep(0.5)
        return 0
    if FishLogicLangFlag:
        print("✅ 鱼饵OK")
    else:
        print("Bait OK")
    return 1

def jinlema(yugan):
    "检查鱼竿位置图标 在钓鱼则返回1，不在钓鱼则返回0"
    yuganshot = pyautogui.screenshot(region=yugan)
    yuganshot_cv = cv2.cvtColor(np.array(yuganshot), cv2.COLOR_RGB2BGR)
    image_path = full_imagePath("yugan_screenshot.png")
    temp = find_pic(yuganshot_cv, image_path,0.8)
    if temp is None:
        return 1
    else:
        return 0

def shanggoulema(shanggoufind, window):
    target_color = (251, 177, 22)
    is_match, match_ratio = fuzzy_color_match(shanggoufind, target_color, 30, 0.2)
    if is_match:
        PlayerCtl.leftmouse(0.5)
        window = pyautogui.screenshot(region=window)
        window_cv = cv2.cvtColor(np.array(window), cv2.COLOR_RGB2BGR)
        image_path = full_imagePath("diaoyuchong.png")
        temp = find_pic(window_cv, image_path, 0.5,type = "A")
        if temp is not None:
            return 1
    # print(f"上钩检测中,当前匹配比率{match_ratio}")
    return 0

def zuoma(zuo):
    target_color = (255, 87, 1)
    is_match, match_ratio = fuzzy_color_match(zuo, target_color, 35, 0.02)
    # print(f"左侧颜色,当前匹配比率{match_ratio}")
    if is_match:
        return 1
    return 0

def youma(you):
    target_color = (255, 87, 1)
    is_match, match_ratio = fuzzy_color_match(you, target_color, 35, 0.02)
    # print(f"右侧颜色,当前匹配比率{match_ratio}")
    if is_match:
        return 1
    return 0
def diaodaolema(jixu):
    target_color2 = (232, 232, 232)
    is_match, match_ratio = fuzzy_color_match(jixu, target_color2, 5, 0.8)
    # print(f"当前是否钓上检测比率{match_ratio}")
    return is_match
def diaoyuchong(zuo, you, jixu, zhanglifind):
    pyautogui.mouseDown()
    target_color_zhang = (250, 250, 250)
    zhangli, match_ratio_zhang = fuzzy_color_match(zhanglifind, target_color_zhang, 30, 0.5)
    if zhangli:
        print("SHAKING~")
        clicker.start_clicking()
    else:
        clicker.stop_clicking()

    if zuoma(zuo):
        pyautogui.keyDown("A")
        pyautogui.keyUp("D")
        pyautogui.mouseDown()
    if youma(you):
        pyautogui.keyDown("D")
        pyautogui.keyUp("A")
        pyautogui.mouseDown()
    if(diaodaolema(jixu)):
    # print(f"是否钓上检测比率{match_ratio},张力检测比率{match_ratio_zhang}")
        clicker.stop_clicking()
        pyautogui.mouseUp()
        pyautogui.keyUp("A")
        pyautogui.keyUp("D")
        return 1
    return 0
def diaodaole():
    clicker.stop_clicking()
    global g_jixudiaoyu
    pyautogui.moveTo(g_jixudiaoyu[0], g_jixudiaoyu[1])
    PlayerCtl.leftmouse(0.5)
    return 1

def get_clicker():
    global clicker
    return clicker

def init_clicker():
    global clicker
    if clicker is None:
        clicker = PreciseMouseClicker(interval_ms=60, button='left', duration_ms=10)

def fish_area_cac(gamewindow):
    yuer = (
        int(gamewindow[0] + 0.715 * gamewindow[2]),
        int(gamewindow[1] + 0.915 * gamewindow[3]),
        int(0.05 * 9 / 16 * gamewindow[2]),
        int(0.05 * gamewindow[3]),
    )
    
    yugan = (
        int(gamewindow[0] + 0.855 * gamewindow[2]),
        int(gamewindow[1] + 0.915 * gamewindow[3]),
        int(0.05 * 9 / 16 * gamewindow[2]),
        int(0.05 * gamewindow[3]),
    )
    
    shanggoufind = (
        int(gamewindow[0] + 0.47 * gamewindow[2]),
        int(gamewindow[1] + 0.4 * gamewindow[3]),
        int(0.04 * 9 / 16 * gamewindow[2]),
        int(0.14 * gamewindow[3]),
    )
    
    zuofind = (
        int(gamewindow[0] + 0.43 * gamewindow[2]),
        int(gamewindow[1] + 0.46 * gamewindow[3]),
        int(0.03 * 9 / 16 * gamewindow[2]),
        int(0.05 * gamewindow[3]),
    )
    
    youfind = (
        int(gamewindow[0] + 0.53 * gamewindow[2]),
        int(gamewindow[1] + 0.46 * gamewindow[3]),
        int(0.03 * 9 / 16 * gamewindow[2]),
        int(0.05 * gamewindow[3]),
    )
    
    jixufind = (
        int(gamewindow[0] + 0.892 * gamewindow[2]),
        int(gamewindow[1] + 0.88 * gamewindow[3]),
        int(0.02 * 9 / 16 * gamewindow[2]),
        int(0.02 * gamewindow[3]),
    )
    
    zhanglifind = (
        int(gamewindow[0] + 0.53 * gamewindow[2]),
        int(gamewindow[1] + 0.822 * gamewindow[3]),
        int(0.02 * 9 / 16 * gamewindow[2]),
        int(0.02 * gamewindow[3]),
    )

    global g_jixudiaoyu
    g_jixudiaoyu = (
        int(gamewindow[0] + 0.829307 * gamewindow[2]),
        int(gamewindow[1] + 0.903042 * gamewindow[3]),
    )

    return yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind

def NotFindESC():
    SwitchToGame()
    window = pyautogui.screenshot()
    window_cv = cv2.cvtColor(np.array(window), cv2.COLOR_RGB2BGR)
    image_path = full_imagePath("ESC.png")
    temp = find_pic(window_cv, image_path, 0.8)
    if temp is None:
        return 1
    else:
        return 0
def SolveDaySwitch(pos1,pos2):
    # 清除所有按键状态
    global clicker
    clicker.stop_clicking()
    pyautogui.keyUp('A')
    pyautogui.keyUp('D')
    pyautogui.mouseUp(button='left')
    # 点掉跨日界面
    pyautogui.keyDown('alt')
    pyautogui.moveTo(g_jixudiaoyu[0], g_jixudiaoyu[1])
    pyautogui.click()
    pyautogui.keyUp('alt')
    pyautogui.sleep(0.5)
    pyautogui.keyDown('alt')
    pyautogui.moveTo(pos2[0], pos2[1])
    pyautogui.click()
    pyautogui.keyUp('alt')
    #避免过快检测ESC
    precise_sleep(2)
    # 到这里位置应该已经把月卡界面点掉了，避免在商店界面
    counter = 0
    while(NotFindESC()):
        SolvePurchaseStoped()
        pyautogui.sleep(1.2)
        if counter > 6:
            return False
        counter += 1
    return True

def SolvePurchaseStoped():
    trust = 0.8
    delay = 0.2
    if FindPicFromFullScreen(full_imagePath("shop_yes.png")):
        searchandmovetoclick("shop_yes.png",trust,delay)
        searchandmovetoclick("shop_x.png",trust,delay)
    elif FindPicFromFullScreen(full_imagePath("shop_buy.png")):
        press_key('esc')
    elif FindPicFromFullScreen(full_imagePath("shop_OK.png")):
        press_key('esc')
    elif FindPicFromFullScreen(full_imagePath("shop_x.png")):
        press_key('esc')
    
        
if __name__ == "__main__":
    init_clicker()