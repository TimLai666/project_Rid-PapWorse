import eel
import time
from pathlib import Path
import app.app
import sys
if hasattr(sys, "_MEIPASS"): # if the script is started from an executable file
    with open("logs.txt", "a") as f_logs:
        sys.stdout = f_logs
        sys.stderr = f_logs

DATA_ROOT_DIR = Path("./data")

eel.init('UI')  # 假设您的HTML/CSS/JavaScript文件都放在`web`目录下

app.app.app_init()

@eel.expose
def switchPage(page: str) -> None:
    eel.switchPage(page)

@eel.expose
def set_account(value: str):
    # 查詢資料庫
    # 用屆數當資料夾名稱
    # gen
    # dir_path = DATA_ROOT_DIR / Path(gen)
    pass

@eel.expose
def what_to_input(type: str) -> list[dict[str, str]]:
    match type:
        case 'createClubInfo':
            # 從資料庫決定要輸入什麼
            return [{
                '社團名稱': 'text',
                '第幾屆': 'number',
                '指導老師': 'text',
                'detailDescription': 'textarea',
                'importImage': 'file',
            }, {
                # 預填的值
                '社團名稱': 'TODO: 從資料庫取得',
            }]

    
@eel.expose
def page_ready() -> None:
    # 程式ui打開後會立即執行
    pass
    
# switchPage('home')

eel.start('main.html', size=(1910, 1080), port=5349)  # 启动应用，打开`main.html`



# 打包命令
# pyinstaller -F --add-data 'UI;UI' --add-data 'app;app' launcher.py
