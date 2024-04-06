# 主要程式邏輯之所在
if __name__ != '__main__':
    from .DBControl import init_db, insert_record
    from .DBControl import query_records as db_query_records
else:
    from DBControl import init_db, insert_record
    from DBControl import query_records as db_query_records

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
            '屆': 'INT',
            '職位': 'TEXT',
            'phone': 'TEXT',
            'primary key': '(屆, 職位)',
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

# 查詢每屆社團資料中有哪些職位
def query_positions(gen: int) -> list[str]:
    result = db_query_records('每屆社團資料', {'屆': gen}, [], return_as_dict=True)
    if not result:
        return ['社長', '副社長', '文書長', '美宣長', '教學長', '公關長', '器材長', '總務長', '活動長', '資訊長', '攝影長']
    return [key for key, _ in result[0].items() if key != '屆' and key != '指導老師']

# 查詢每個職位是誰，和電話號碼
def query_cadres_name_and_phone_numbers(gen: int) -> dict[str, str]:
    result = db_query_records('每屆社團資料', {'屆': gen}, [], return_as_dict=True)
    if result:
        n={}
        for position, name in result[0].items():
            if position != '屆' and name != None:
                phone_result = db_query_records('Phone', {'屆': gen, '職位': position}, [])
                if phone_result:
                    phone = phone_result[0][0]
                    n[position] = {'name': name, 'phone': phone}
                else:
                    n[position] = {'name': name}
    return n
        

    # return {record['職位']: record['phone'] for record in result}

# insert_record('Phone', {'屆': 2023, '職位': '指導老師', 'phone': '20330'})
# print(query_positions(2023))
# print(query_cadres_name_and_phone_numbers(2023))