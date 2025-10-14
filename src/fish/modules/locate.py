import os
import locale

g_myLang = None
def GetSysLang():
    global g_myLang
    # return "en" 断点用于调试en环境
    return g_myLang

def InitSysLang():
    
    global g_myLang
    if g_myLang is not None:
        return
    # 方法一：通过 locale 模块获取系统默认语言设置
    try:
        lang, _ = locale.getdefaultlocale()
        if lang:
            #print(f"[方法一 - locale模块] 系统默认语言: {lang}")
            if lang.startswith('zh'):
                g_myLang = "zh"
                return
            elif lang.startswith('en'):
                g_myLang = "en"
                return
    except Exception as e:
        print(f"locale.getdefaultlocale() Error: {e}")

    # 方法二：通过环境变量（更通用，跨平台性更好）
    language_env_vars = ['LANG', 'LC_ALL', 'LANGUAGE']
    for var in language_env_vars:
        value = os.environ.get(var)
        if value:
            #print(f"[环境变量] {var}={value}")
            # 常见格式如：en_US.UTF-8 或 zh_CN.UTF-8
            parts = value.split('.')
            if parts:
                lang_part = parts[0]  # 取 en_US 或 zh_CN
                langs = lang_part.split('_')
                if langs and langs[0].lower() in ['zh', 'en']:
                    if langs[0].lower() == 'zh':
                        g_myLang = "zh"
                        return
                    elif langs[0].lower() == 'en':
                        g_myLang = "en"
                        return

    # 如果无法明确判断，默认返回英文或其他提示
    g_myLang = "en"
    return

# 调用函数并打印结果
if __name__ == "__main__":
    InitSysLang()
    system_lang = GetSysLang()
    print(f"检测到的系统语言环境是：{system_lang}")