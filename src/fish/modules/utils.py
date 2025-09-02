import os
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw
import time
import math
import sys

g_current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
g_current_dir = os.path.join(g_current_dir, "_internal") #打包需要
g_current_dir = os.path.join(g_current_dir, "fish")
g_current_dir = os.path.join(g_current_dir, "modules")
g_current_dir = os.path.join(g_current_dir, "pic")
# print(f"{g_current_dir}")
global g_suofang 
g_suofang = 1.0
global g_suofang_ratio
g_suofang_ratio = 1.0

def multi_scale_template_match(template_path, screenshot=None, region=None, 
                              scale_range=(0.5, 2.0), scale_steps=10, 
                              method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
    """
    多尺度模板匹配
    
    参数:
        template_path: 模板图像路径
        screenshot: 屏幕截图（可选）
        region: 屏幕区域 (x, y, width, height)（可选）
        scale_range: 尺度搜索范围 (min_scale, max_scale)
        scale_steps: 尺度搜索步数
        method: 模板匹配方法
        threshold: 匹配阈值
    
    返回:
        匹配位置 (x, y, width, height) 或 None
    """
    # 读取模板图像
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"无法读取模板图像: {template_path}")
    
    # 获取屏幕截图
    if screenshot is None:
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        # 转换为OpenCV格式
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    else:
        # 确保是灰度图
        if len(screenshot.shape) == 3:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # 获取模板和屏幕截图的尺寸
    h_template, w_template = template.shape
    h_screen, w_screen = screenshot.shape
    
    # 初始化最佳匹配变量
    best_match_val = -1
    best_match_loc = None
    best_scale = 1.0
    
    # 在多尺度上搜索
    for scale in np.linspace(scale_range[0], scale_range[1], scale_steps):
        # 计算缩放后的模板尺寸
        w_resized = int(w_template * scale)
        h_resized = int(h_template * scale)
        
        # 检查缩放后的模板是否比屏幕大
        if w_resized > w_screen or h_resized > h_screen:
            continue
        
        # 缩放模板
        resized_template = cv2.resize(template, (w_resized, h_resized))
        
        # 执行模板匹配
        result = cv2.matchTemplate(screenshot, resized_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 对于不同的匹配方法，处理结果
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            match_val = 1 - min_val  # 对于平方差方法，值越小越好
            match_loc = min_loc
        else:
            match_val = max_val  # 对于相关方法，值越大越好
            match_loc = max_loc
        
        # 更新最佳匹配
        if match_val > best_match_val:
            best_match_val = match_val
            best_match_loc = match_loc
            best_scale = scale
            best_size = (w_resized, h_resized)
        
        print(f"尺度 {scale:.2f}: 匹配值 {match_val:.3f}")
    
    # 检查是否找到匹配
    if best_match_val >= threshold:
        x, y = best_match_loc
        w, h = best_size
        print(f"最佳匹配: 尺度 {best_scale:.2f}, 匹配值 {best_match_val:.3f}")
        global g_suofang 
        g_suofang = best_scale
        global g_suofang_ratio
        g_suofang_ratio = best_match_val
        print(f"1920 * 1080 缩放比例: {g_suofang}")
        return 1
    else:
        print(f"未找到匹配，最佳匹配值 {best_match_val:.3f} 低于阈值 {threshold}")
        return None
    

def find_pic(screenshot_cv, template_path, confidence=0.4 , type = None):
    template = cv2.imread(template_path)
    if template is None:
        print(f"错误：无法读取模板图片 {template_path}")
        return None
    template_height, template_width = template.shape[:2]
    if (type == "A"):
        # print(f"缩放比例: {g_suofang}")
        h_resized = int(template_height * g_suofang)
        w_resized = int(template_width * g_suofang)
        dim = (w_resized, h_resized)
        resized_template = cv2.resize(template, dim ,interpolation=cv2.INTER_AREA)
        confidence = confidence * g_suofang_ratio
    else:
        resized_template = template

    result = cv2.matchTemplate(screenshot_cv, resized_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print(f"最高相似度: {max_val}")
    
    if max_val >= confidence:
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        
        window_info = {
            'left': top_left[0],
            'top': top_left[1],
            'width': template_width,
            'height': template_height,
            'confidence': max_val
        }
        return window_info
    else:
        # print(f"未找到图片。最高匹配度 {max_val} 低于阈值 {confidence}")
        return None

def pyautogui2opencv(temp):
    top_left = (temp[0], temp[1])
    bottom_right = (temp[0] + temp[2], temp[1] + temp[3])
    return top_left, bottom_right

def dirinfo2pyautoguiinfo(temp):
    res = (
        temp.get("left"),
        temp.get("top"),
        temp.get("width"),
        temp.get("height"),
    )
    return res

def fuzzy_color_match(region, target_color, tolerance=10, match_threshold=0.7):
    screenshot = pyautogui.screenshot(region=region)
    img_array = np.array(screenshot)
    color_diff = np.abs(img_array - target_color)
    matches = np.all(color_diff <= tolerance, axis=2)
    match_ratio = np.sum(matches) / matches.size
    is_match = match_ratio >= match_threshold
    return is_match, match_ratio

def switch_to_window_by_title(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            target_window = windows[0]
            if target_window.isMinimized:
                target_window.restore()
            target_window.activate()
            pyautogui.sleep(0.5)
            print(f"已切换到窗口: {window_title}")
            return True
        else:
            print(f"未找到标题包含 '{window_title}' 的窗口")
            return False
    except Exception as e:
        print(f"切换窗口时出错: {e}")
        return False

def find_game_window(screenshot_cv):
    """
    使用模板匹配在屏幕上寻找游戏窗口,并寻找鱼竿相关信息串口
    
    参数:
        screenshot_cv:CV格式的游戏窗口
    返回:
        window_info_ret or None: 包含窗口坐标和尺寸的字典，未找到返回None
    """
    
    image_path = os.path.join(g_current_dir, "esc.png")
    multi_scale_template_match(image_path,screenshot_cv,
                               scale_range=(0.5, 2.0),
                               scale_steps=10,
                               threshold=0.5)
    
    image_path = os.path.join(g_current_dir, "esc.png")
    logoinfo = find_pic(screenshot_cv,image_path,0.3,type = "A")
    # print(f"已找到logoinfo为:{logoinfo}")

    # image_path = os.path.join(g_current_dir, "rightdown.png")
    # youxiainfo= find_pic(screenshot_cv,image_path,0.3,type = "A")
    # print(f"已找到youxiainfo为:{youxiainfo}")

    if(logoinfo == None):
        return None
    # if(youxiainfo == None):
    #     return None
    
    left = logoinfo.get("left")
    top_left = (logoinfo.get("left"),logoinfo.get("top"))
    width = int(1904 * g_suofang)
    height = int(1052 * width / 1904)
    bottom_right = (top_left[0] + width, top_left[1] + height)

    windowinfo = {
        'left': top_left[0],
        'top': top_left[1],
        'width': width,
        'height': height,
    }

    print(f"已找到窗口为:{windowinfo}")
    # top_left = (window_info.left,window_info.top)
    # bottom_right = (top_left[0] + window_info.width, top_left[1] + window_info.height)
    # # 添加置信度文本
    # label = f"Confidence: NA"
    # cv2.putText(screenshot_cv, label, (top_left[0], top_left[1]-10), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # 显示结果（调试用）
    # cv2.imshow('匹配结果', screenshot_cv)
    # cv2.waitKey(0) # 等待按键后关闭窗口
    # cv2.destroyAllWindows()
    
    # 返回pyautogui能够用的格式
    windowinfo_ret = dirinfo2pyautoguiinfo(windowinfo)
    return windowinfo_ret

def pyautogui2opencv(temp):
    top_left = (temp[0],temp[1])
    bottom_right = (temp[0] + temp[2],temp[1] + temp[3])
    return top_left , bottom_right
    
def dirinfo2pyautoguiinfo(temp):
    res = (
        temp.get("left"),
        temp.get("top"),
        temp.get("width"),
        temp.get("height"),
    )
    return res

import math
import time

def precise_sleep(duration):
    (a, b) = math.modf(duration)
    time.sleep(b)
    target = time.perf_counter() + a
    while time.perf_counter() < target:
        pass

def debug_screenshot_data(screenshot_cv,gamewindow,yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind):

    top_left,bot_right = pyautogui2opencv(gamewindow)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (0, 255, 0), 2)
    top_left,bot_right = pyautogui2opencv(yuer)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (0, 0, 255), 2)
    top_left,bot_right = pyautogui2opencv(yugan)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (0, 0, 255), 2)
    top_left,bot_right = pyautogui2opencv(shanggoufind)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (255, 0, 0), 2)
    top_left,bot_right = pyautogui2opencv(zuofind)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (255, 255, 0), 2)
    top_left,bot_right = pyautogui2opencv(youfind)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (255, 255, 0), 2)
    top_left,bot_right = pyautogui2opencv(jixufind)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (255, 170, 170), 2)
    top_left,bot_right = pyautogui2opencv(zhanglifind)
    cv2.rectangle(screenshot_cv, top_left, bot_right, (255, 0, 0), 2)

    image_save_path = os.path.join(g_current_dir, "debug_screenshot.png")
    cv2.imwrite(image_save_path, screenshot_cv)

def area_cac(gamewindow):
    yuer = (
        int(gamewindow[0] + 0.715 * gamewindow[2]),
        int(gamewindow[1] + 0.915 * gamewindow[3]),
        int(0.05 * 9 / 16 * gamewindow[2]),
        int(0.05 * gamewindow[3]),
    )
    
    yugan = (
        int(gamewindow[0] + 0.86 * gamewindow[2]),
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
        int(gamewindow[0] + 0.88 * gamewindow[2]),
        int(gamewindow[1] + 0.88 * gamewindow[3]),
        int(0.03 * 9 / 16 * gamewindow[2]),
        int(0.03 * gamewindow[3]),
    )
    
    zhanglifind = (
        int(gamewindow[0] + 0.53 * gamewindow[2]),
        int(gamewindow[1] + 0.822 * gamewindow[3]),
        int(0.02 * 9 / 16 * gamewindow[2]),
        int(0.02 * gamewindow[3]),
    )
    return yuer,yugan,shanggoufind,zuofind,youfind,jixufind,zhanglifind