import paling
import time

paling.init('UI')  # 假设您的HTML/CSS/JavaScript文件都放在`web`目录下

@paling.expose
def switchPage(page: str):
    paling.switchPage(page)

@paling.expose
def page_ready():
    # 程式ui打開後會立即執行
    pass
    
# switchPage('home')

paling.start('main.html', size=(1910, 1080), port=5349)  # 启动应用，打开`main.html`



# 打包命令
# pyinstaller --add-data 'UI:UI' launcher.py
