import eel
import time

eel.init('UI')  # 假设您的HTML/CSS/JavaScript文件都放在`web`目录下

def switchPage(page: str):
    eel.switchPage(page)

@eel.expose
def page_ready():
    # 程式ui打開後會立即執行
    pass
    
# switchPage('home')

eel.start('main.html', size=(1920, 1080), port=5349)  # 启动应用，打开`main.html`


# mac 要使用 python 3.10

# 打包命令
# pyinstaller --add-data 'UI:UI' launcher.py
