# ShiroFisher-StarResonanceSmartFishing
# 钓鱼自动化脚本

这是一个用于自动化钓鱼的Python脚本。
功能：
自动检测游戏窗口
自动投放鱼竿
自动检测鱼上钩
自动收杆
自动购买鱼竿和鱼饵

## 安装依赖

```bash
pip install -r requirements.txt

# 使用方法

1.确保游戏窗口标题为"星痕共鸣",分辨率为1920*1080
2.运行脚本：
python main.py
3.按F6键可以停止脚本
4.如果产生无线左键错误可以鼠标放在屏幕左上角，然后按F6键停止脚本，再按F6键重新开始脚本  
## 安装依赖
python = 3.12.7
opencv-python==4.12.0.88
numpy==2.2.6
PyAutoGUI==0.9.54
PyGetWindow==0.0.9
keyboard==0.13.5

project/
├── src/
│   └── fish/
│       ├── __init__.py
│       ├── main.py
│       └── modules/
│           ├── __init__.py
│           ├── camera_control.py
│           ├── player_control.py
│           ├── fishing_logic.py
│           └── utils.py
├── tests/
├── requirements.txt
└── README.md