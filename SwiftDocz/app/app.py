# 主要程式邏輯之所在
from .DBControl import init_db

# 在 launcher.py 中 import 這個函數
def app_init():
    # 初始化資料庫，若有變更將自動更新，原有資料不受影響
    init_db({
        '每屆社團資料': [{
            '屆': 'INT PRIMARY KEY',
            '指導老師': 'TEXT',
            '社長': 'TEXT',
            '副社長': 'TEXT',
            '文書長': 'TEXT',
            '美宣長': 'TEXT',
            '教學長': 'TEXT',
            '公關長': 'TEXT',
            '器材長': 'TEXT',
            '總務長': 'TEXT',
            '活動長': 'TEXT',
            '資訊長': 'TEXT',
            '攝影長': 'TEXT',
        }, {
            # 無外來鍵
        }],

        'Phone': [{
            '屆': 'INT PRIMARY KEY',
            '指導老師': 'TEXT',
            '社長': 'TEXT',
            '副社長': 'TEXT',
            '文書長': 'TEXT',
            '美宣長': 'TEXT',
            '教學長': 'TEXT',
            '公關長': 'TEXT',
            '器材長': 'TEXT',
            '總務長': 'TEXT',
            '活動長': 'TEXT',
            '資訊長': 'TEXT',
            '攝影長': 'TEXT',
        }, {
            '屆': '每屆社團資料(屆)',
        }]

    #     'table1': [{
    #         '屬性1': '資料型態1 PRIMARY KEY',
    #         '屬性2': '資料型態2',
    #     },{
    #         '外來鍵1': '參考表格(參考屬性)',
    #         '外來鍵2': '參考表格(參考屬性)',
    #     }],
    #     'table2': [{
            # '屬性1': '資料型態1 INTEGER PRIMARY KEY AUTOINCREMENT', # AUTOINCREMENT 會自動照順序生成數字
    #         '屬性2': '資料型態2',
    #     },{
    #         # 若無外來鍵就空白
    #     }],
    }) 
    pass