import paling
import time
from pathlib import Path
import app.app

DATA_ROOT_DIR = Path("./data")

paling.init('UI')  # 假设您的HTML/CSS/JavaScript文件都放在`web`目录下

app.app.app_init()

@paling.expose
def switchPage(page: str) -> None:
    paling.switchPage(page)

@paling.expose
def set_account(value: str):
    # 查詢資料庫
    # 用屆數當資料夾名稱
    # gen
    # dir_path = DATA_ROOT_DIR / Path(gen)
    pass

@paling.expose
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

    
@paling.expose
def page_ready() -> None:
    # 程式ui打開後會立即執行
    pass
    
# switchPage('home')

paling.start('main.html', size=(1910, 1080), port=5349)  # 启动应用，打开`main.html`



# 打包命令
# pyinstaller --add-data 'UI:UI' launcher.py
