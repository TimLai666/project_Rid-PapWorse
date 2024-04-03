import sqlite3
from DBBackup import backup as db_backup
import time

# 資料庫路徑
database_paths = {
    'main': '../data/database.db' 
}

def do_database_operations(sql_statement: str, database: str = 'main', placeholders_mode: bool = False, values_tuple: tuple = None, query_mode: bool = False, fk_mode: bool = True, return_as_dict: bool = False) -> (list[any] | None):
    # 使用 sqlite3 連接數據庫
    with sqlite3.connect(database_paths[database]) as conn:
        if fk_mode:
            conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        if return_as_dict:
            conn.row_factory = sqlite3.Row  # 设置返回字典
        cursor = conn.cursor()
        # 執行 SQL 語句
        if placeholders_mode and query_mode:
            new_cursor = cursor.execute(sql_statement, values_tuple)
        elif query_mode:
            new_cursor = cursor.execute(sql_statement)
        elif placeholders_mode:
            cursor.execute(sql_statement, values_tuple)
        else:
            cursor.execute(sql_statement)
        conn.commit()  # 確保變更被提交
    
    records = None
    if query_mode:
        records = new_cursor.fetchall()

    if records:
        if return_as_dict:
            records = [dict(row) for row in records]
    return records

# relation:Table名稱，attributes:dict[屬性, 資料型態]，foreign_keys:dict[外來鍵名稱, 參考表格(參考屬性)]
def create_table(relation: str, attributes: dict[str, str], foreign_keys: dict[str, str]) -> None:
    # 構建屬性定義部分
    columns_definitions = ', '.join([f"{name} {data_type}" for name, data_type in attributes.items()])
    
    # 構建外來鍵定義部分
    foreign_keys_definitions = []
    for fk_column, references in foreign_keys.items():
        # 假設 references 的格式為 "ParentTableName(ParentColumnName)"
        foreign_keys_definitions.append(f", FOREIGN KEY ({fk_column}) REFERENCES {references} ON UPDATE CASCADE ON DELETE CASCADE")
    foreign_keys_definition = ''.join(foreign_keys_definitions)
    
    # 組合最終的 SQL 語句
    sql_statement = f"CREATE TABLE IF NOT EXISTS {relation} ({columns_definitions}{foreign_keys_definition});"
    do_database_operations(sql_statement)

# relation:Table名稱，record:dict[屬性, 值]
def insert_record(relation: str, records: dict[str, str]) -> None:
    columns = ', '.join(records.keys())
    placeholders = ', '.join('?' for _ in records.values())
    values = tuple(records.values())
    
    # 組合成完整的 SQL 語句
    sql_statement = f"INSERT INTO {relation} ({columns}) VALUES ({placeholders});"
    do_database_operations(sql_statement, placeholders_mode=True, values_tuple=values)

# relation:Table名稱，conditions條件(需全部符合):dict[屬性名稱, 值]
def delete_record(relation: str, conditions: dict[str, any]) -> None:
    # 構建 WHERE 條件語句和對應的值
    where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
    values = tuple(conditions.values())
    
    # 構建完整的 SQL 刪除語句
    sql_statement = f"DELETE FROM {relation} WHERE {where_clause};"
    do_database_operations(sql_statement, placeholders_mode=True, values_tuple=values)

# relation:Table名稱，conditions條件(需全部符合):dict[屬性名稱, 值]，to_query:list[要查的屬性]
# 結果：list[tuple[any]]，[(記錄1屬性1, 記錄1屬性2), (記錄2屬性1, 記錄2屬性2)]
def query_records(relation: str, conditions: dict[str, any], to_query: list[any], return_as_dict: bool = False) -> (list[tuple[any]] | list[dict[str, any]]):
    # 构建要查询的字段字符串
    query_fields = ', '.join(to_query) if to_query else '*'

    # 构建 WHERE 条件语句和对应的值
    where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
    values = tuple(conditions.values())

    # 构建完整的 SQL 查询语句
    sql_statement = f"SELECT {query_fields} FROM {relation} WHERE {where_clause};"

    # 执行查询操作
    records = do_database_operations(sql_statement, placeholders_mode=True, values_tuple=values, query_mode=True, return_as_dict=return_as_dict)
    return records

def update_records(relation: str, conditions: dict[str, any], new_values: dict[str, any]) -> None:
    # 构建更新字段的部分
    set_clause = ', '.join([f"{k} = ?" for k in new_values.keys()])
    # 构建 WHERE 条件语句和对应的值
    where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
    
    # 合并新值和条件值为一个参数列表
    values = tuple(new_values.values()) + tuple(conditions.values())
    
    # 构建完整的 SQL 更新语句
    sql_statement = f"UPDATE {relation} SET {set_clause} WHERE {where_clause};"
    do_database_operations(sql_statement, placeholders_mode=True, values_tuple=values)

def create_trigger(trigger_name: str, action: str, table_name: str, triggering_event: str, sql_operation: str) -> None:
    """
    创建一个数据库触发器的通用函数。
    
    :param trigger_name: 触发器的名称。
    :param action: 触发器触发的动作，比如 'AFTER INSERT' 或 'BEFORE UPDATE'。
    :param table_name: 触发器所依附的表名。
    :param triggering_event: 触发器的条件，比如是对哪个列的操作。
    :param sql_operation: 触发器被触发时执行的 SQL 操作。
    """
    # 构建触发器的 SQL 语句
    sql_statement = f"""
    CREATE TRIGGER IF NOT EXISTS {trigger_name}
    {action} ON {table_name}
    FOR EACH ROW
    WHEN ({triggering_event})
    BEGIN
        {sql_operation};
    END;
    """
    do_database_operations(sql_statement)

# def init_db() -> None:
#     # table['表名'] = [{
#     #   '屬性1': '資料型態1', '屬性2': '資料型態2'
#     # }, {
#     #   '外來鍵名稱': '參考表格(參考屬性)'
#     # }]
#     tables: dict[str, list[dict, list, dict]] = {}

#     # Users
#     tables['Users'] = [{
#         'uuid': 'TEXT PRIMARY KEY',
#         'username': 'TEXT',
#         'email': 'TEXT',
#         'password': 'TEXT',
#         'firstname': 'TEXT',
#         'lastname': 'TEXT',
#         'phone': 'TEXT'
#     }, {
#         # 無外來鍵
#     }]

#     # SessionRecords
#     tables['SessionRecords'] = [{
#         'session_id': 'TEXT PRIMARY KEY',
#         'time': 'DATETIME',
#         'ip': 'TEXT',
#         'expiration': 'DATETIME',
#         'is_active': 'BOOLEAN',
#         'user_uuid': 'TEXT'
#     }, {
#         'user_uuid': 'Users(uuid)'
#     }]

#     # Games
#     tables['Games'] = [{
#         'name':'TEXT PRIMARY KEY',
#         'highest_score': 'REAL DEFAULT 0',
#         'achievement_holder': 'TEXT'
#     }, {
#         'achievement_holder': 'Users(uuid)'
#     }]

#     tables['GamePlayingRecords'] = [{
#         'record_id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
#         'game_name': 'TEXT',
#         'user_uuid': 'TEXT',
#         'time': 'DATETIME',
#         'score': 'REAL'
#     }, {
#         'game_name': 'Games(name)',
#         'user_uuid': 'Users(uuid)'
#     }]

#     for relation in tables:
#         create_table(relation, tables[relation][0], tables[relation][1])
    
#     # 更新已有的表格結構
#     update_db(tables)

#     # 创建一个触发器来自动更新 Games 表的 highest_score 字段
#     create_trigger(
#         trigger_name="UpdateHighestScoreAndHolder",
#         action="AFTER INSERT",
#         table_name="GamePlayingRecords",
#         triggering_event="NEW.score > (SELECT highest_score FROM Games WHERE name = NEW.game_name)",
#         sql_operation="""
#         UPDATE Games
#         SET highest_score = NEW.score,
#             achievement_holder = NEW.user_uuid
#         WHERE name = NEW.game_name
#         """
#     )

# updating_tables: dict[表名, 結構]
def update_db(updating_tables: dict[str, list]):
    for name, details in updating_tables.items():
        drop_triggers()
        # 临时新表的名称
        new_table = f"new_{name}"
        # 创建新表
        create_table(new_table, details[0], details[1])
        # 复制数据
        do_database_operations(f"INSERT INTO {new_table} SELECT * FROM {name};")
        # 删除原有表
        do_database_operations(f"DROP TABLE {name};", fk_mode=False)
        # 重命名新表
        do_database_operations(f"ALTER TABLE {new_table} RENAME TO {name};")

def drop_triggers():
    triggers = do_database_operations("SELECT name FROM sqlite_master WHERE type='trigger'", query_mode=True, return_as_dict=True)
    if triggers:
        for trigger in triggers:
            do_database_operations(f"DROP TRIGGER IF EXISTS {trigger['name']};")

def backup_database():
    db_backup(database_paths)
    time.sleep(86400)  # 每天更新一次