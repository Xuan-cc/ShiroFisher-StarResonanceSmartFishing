import pyautogui
import time
import keyboard
import sys
from fish.modules.utils import (get_suofang,press_key)
# 设置pyautogui的安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# 基准分辨率 (您提供的坐标基于此分辨率)
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

# 获取当前屏幕分辨率
# SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
# print(f"当前屏幕分辨率: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# 相对坐标字典 (基于1920x1080)
RELATIVE_COORDS = {
    "pos1": (1428/BASE_WIDTH, 565/BASE_HEIGHT),
    "pos2": (819/BASE_WIDTH, 721/BASE_HEIGHT),
    "pos3": (307/BASE_WIDTH, 909/BASE_HEIGHT),
    "pos4": (1589/BASE_WIDTH, 233/BASE_HEIGHT),
    "pos5": (1612/BASE_WIDTH, 997/BASE_HEIGHT),
    "pos6": (1749/BASE_WIDTH, 999/BASE_HEIGHT),
    "pos7": (1272/BASE_WIDTH, 798/BASE_HEIGHT),
    "pos8": (1113/BASE_WIDTH, 981/BASE_HEIGHT),
    "pos9": (1499/BASE_WIDTH, 931/BASE_HEIGHT),
    "pos10": (1759/BASE_WIDTH, 975/BASE_HEIGHT),
    "pos11": (1430/BASE_WIDTH, 278/BASE_HEIGHT),
    "pos12": (1791/BASE_WIDTH, 294/BASE_HEIGHT),
    "pos13": (1129/BASE_WIDTH, 919/BASE_HEIGHT),
    "pos14": (1855/BASE_WIDTH, 47/BASE_HEIGHT),
    "pos15": (581/BASE_WIDTH, 853/BASE_HEIGHT),
    "pos16": (875/BASE_WIDTH, 965/BASE_HEIGHT)
}
def calculate_absolute_coords(SCREEN_WIDTH,SCREEN_HEIGHT):
    """将相对坐标转换为绝对坐标"""
    absolute_coords = {}
    for key, (rel_x, rel_y) in RELATIVE_COORDS.items():
        abs_x = int(rel_x * SCREEN_WIDTH)
        abs_y = int(rel_y * SCREEN_HEIGHT)
        absolute_coords[key] = (abs_x, abs_y)
        print(f"{key}: 相对 ({rel_x:.3f}, {rel_y:.3f}) -> 绝对 ({abs_x}, {abs_y})")
    
    return absolute_coords

def get_coords(x_offset=0, y_offset=0):
    suofang = get_suofang()
    absolute_coords = calculate_absolute_coords(int(1920 * suofang), int(1080 * suofang))
    return {k: (int(v[0]) + x_offset, int(v[1]) + y_offset) for k, v in absolute_coords.items()}

def check_color(x, y, expected_color, tolerance=0):
    print(f"检查坐标 ({x}, {y}) 的颜色是否为 {expected_color} (容差: {tolerance})")
    """检查指定坐标的颜色是否与预期颜色匹配"""
    actual_color = pyautogui.pixel(x, y)
    expected_rgb = tuple(int(expected_color[i:i+2], 16) for i in (0, 2, 4))
    
    if tolerance == 0:
        return actual_color == expected_rgb
    else:
        # 简单的颜色容差检查
        return all(abs(actual_color[i] - expected_rgb[i]) <= tolerance for i in range(3))

def dina_main_loop(gamewindow):
    """主循环"""
    pretime = time.time() * 1000  # 转换为毫秒
    print(f"窗口的左上角坐标是：{gamewindow[0]}, {gamewindow[1]}")
    COORDS = get_coords(gamewindow[0], gamewindow[1]) # 获取坐标

    while True:
        print("正在循环中...")
        if keyboard.is_pressed('F12'):
            print("✅ 检测到 F12 键，停止脚本")
            break

        # O 标签对应的代码
        if not check_color(*COORDS["pos1"], "FFFFFF", 2):
            # 月卡
            print("不在蒂娜门口...")
            if check_color(*COORDS["pos2"], "FFFFFF", 0):
                print("大概率在月卡...")
                time.sleep(0.4)
                pyautogui.click()  # 退出
            else:
                print("没看懂...")
                if check_color(*COORDS["pos3"], "FFFFFF", 0):
                    time.sleep(0.4)
                    pyautogui.moveTo(*COORDS["pos4"])
                    time.sleep(0.4)
                    pyautogui.click()
            print("重启第一个print...")
            continue  # 相当于 Goto O
        
        
        # 按下 I 键
        print("按下I键")
        press_key('i')
        time.sleep(3)
        
        if check_color(*COORDS["pos5"], "E8E8E8", 1):
            print("执行Pos5...")
            time.sleep(1)
            pyautogui.moveTo(*COORDS["pos6"])
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(*COORDS["pos7"])
            time.sleep(1)
            pyautogui.click()  # 退出
            time.sleep(1)
            press_key('esc')
            continue  # 相当于 Goto o
        
        pyautogui.moveTo(*COORDS["pos6"])
        time.sleep(0.4)
        pyautogui.click()
        time.sleep(1.5)
        pyautogui.moveTo(*COORDS["pos8"])
        time.sleep(0.4)
        pyautogui.click()
        time.sleep(0.5)
        press_key('esc')
        
        time.sleep(0.5)
        press_key('f')
        time.sleep(1.0)
        pyautogui.moveTo(*COORDS["pos9"])
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.moveTo(*COORDS["pos10"])
        pyautogui.click()
        
        print("等待进入副本...")
        # a 标签对应的代码
        while True:  # 相当于 Rem a
            if check_color(*COORDS["pos11"], "FFFFFF", 0):  # 识别进本
                time.sleep(5.0)
                time.sleep(0.6)
                press_key('w', 0.6)
                # if check_color(*COORDS["pos12"], "ABABAB", 2):  # 识别是不是补齐起码6人队
                # else:
                    # print("退出副本")
                    # time.sleep(0.2)
                    # press_key('p')
                    # time.sleep(0.5)
                    # pyautogui.moveTo(*COORDS["pos7"])
                    # time.sleep(0.2)
                    # pyautogui.click()  # 退出
                    # time.sleep(7.0)
                    # break  # 跳出内层循环，回到主循环
                break  # 跳出内层循环
            time.sleep(0.1)  # 避免CPU占用过高



        print("进入副本")
        time.sleep(5.0)
        press_key('f')
        time.sleep(0.5)
        pyautogui.moveTo(*COORDS["pos13"])
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(8.0)
        
        # 前进并冲刺
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(6.0)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('w')
        
        # 右移并冲刺
        pyautogui.keyDown('d')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(0.6)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('d')
        
        time.sleep(0.5)
        press_key('f')
        time.sleep(2.0)
        
        # 进门前
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(4.5)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('w')
        
        time.sleep(0.2)
        pyautogui.keyDown('a')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(8.0)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('a')
        
        pyautogui.keyDown('s')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(2.5)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('s')
        
        press_key('a', 1.6)
        
        pyautogui.keyDown('s')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(3.3)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('s')
        
        press_key('d', 1.95)
        time.sleep(0.8)
        
        press_key('5')
        time.sleep(0.8)
        press_key('4')
        time.sleep(0.8)
        press_key('x')
        time.sleep(0.8)
        press_key('3')
        time.sleep(0.8)
        press_key('z')
        
        time.sleep(20.0)
        
        # 右移冲刺并跳跃
        pyautogui.keyDown('d')
        time.sleep(0.2)
        pyautogui.keyDown('shift')
        time.sleep(1.1)
        press_key('space')
        time.sleep(1.0)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('d')
        
        # 前进冲刺
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(1.1)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('w')
        
        # 右移冲刺并跳跃
        pyautogui.keyDown('d')
        time.sleep(0.2)
        pyautogui.keyDown('shift')
        time.sleep(1.5)
        press_key('space')
        time.sleep(1.93)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('d')
        time.sleep(0.1)
        press_key('f')
        
        # 出门
        time.sleep(2.0)
        pyautogui.keyDown('w')
        time.sleep(0.1)
        pyautogui.keyDown('shift')
        time.sleep(0.5)
        pyautogui.keyUp('shift')
        pyautogui.keyUp('w')
        time.sleep(0.2)
        press_key('f')
        
        # 进boss
        pretime = time.time() * 1000
        time.sleep(2.0)
        press_key('h')
        time.sleep(0.2)
        press_key('e')
        time.sleep(0.2)
        
        # QMScript_DOOR
        door_timeout = False
        while not door_timeout:
            nowtime = time.time() * 1000
            record = nowtime - pretime
            if record > 90000:
                time.sleep(1.5)
                press_key('p')
                time.sleep(0.5)
                pyautogui.moveTo(*COORDS["pos7"])
                time.sleep(0.2)
                pyautogui.click()  # 退出
                time.sleep(0.2)
                door_timeout = True
                break
            
            if check_color(*COORDS["pos14"], "FFFFFF", 0):
                time.sleep(0.5)
                press_key('esc')
                break
            time.sleep(0.1)  # 避免CPU占用过高
        
        if door_timeout:
            continue  # 回到主循环
        
        # QMScript_NEXT
        while True:
            if check_color(*COORDS["pos15"], "A7876E", 0):
                time.sleep(12.0)
                pyautogui.moveTo(*COORDS["pos16"])
                time.sleep(0.2)
                pyautogui.click()
                break
            time.sleep(0.1)  # 避免CPU占用过高


if __name__ == "__main__":
    try:
        dina_main_loop()
    except KeyboardInterrupt:
        print("程序被用户中断")
        sys.exit(0)
    except pyautogui.FailSafeException:
        print("触发了安全故障保护（鼠标移动到屏幕角落）")
        sys.exit(0)