# 主要程式邏輯之所在
from DBControl import init_db

# 在 launcher.py 中 import 這個函數
def app():
    # init_db({
    #     table1: [{
    #         '屬性1': '資料型態1 PRIMARY KEY',
    #         '屬性2': '資料型態2',
    #     },{
    #         '外來鍵1': '參考表格(參考屬性)',
    #         '外來鍵2': '參考表格(參考屬性)',
    #     }],
    #     table2: [{
            # '屬性1': '資料型態1 INTEGER PRIMARY KEY AUTOINCREMENT', # AUTOINCREMENT 會自動照順序生成數字
    #         '屬性2': '資料型態2',
    #     },{
    #         # 若無外來鍵就空白
    #     }],
    # }) # 初始化資料庫，若有變更將自動更新，原有資料不受影響
    pass