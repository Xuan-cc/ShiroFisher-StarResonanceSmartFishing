import os
import logging
from logging.handlers import RotatingFileHandler
from .utils import full_imagePath

global logger
logger = None

def log_init():
    global logger  # 声明logger为全局变量，以便在函数外部也能访问
    if logger is not None:
        return
    g_log_path = full_imagePath("log.txt")
    # logging.basicConfig(
    # level=logging.INFO,  # 设置日志级别，如 DEBUG, INFO, WARNING, ERROR, CRITICAL
    # format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    # handlers=[
    #     logging.FileHandler(g_log_path, encoding='utf-8'),  # 输出到文件
    #     # logging.StreamHandler()  # 同时输出到控制台（可选）
    # ]
    #)
    logger = logging.getLogger('my_app_logger')
    logger.setLevel(logging.DEBUG) #输出所有信息
    #logger.setLevel(logging.INFO)
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 最大单个日志文件大小：1 MB (单位是字节，5 * 1024 * 1024 = 5MB)
    max_bytes = 1 * 1024 * 1024  # 1 MB
    backup_count = 3  # 最多保留 3 个备份日志文件（加上当前一共最多4个）

    # 创建 RotatingFileHandler
    file_handler = RotatingFileHandler(
        filename=g_log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # # 同时输出到控制台（可选）
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)

    # 添加 handler 到 logger
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)
    logger.info("日志初始化成功")
def GetLogger():
    global logger
    return logger

if __name__ == '__main__':
    if logger == None:
        log_init()