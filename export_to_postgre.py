import pandas as pd
import psycopg2
import regbase

# Подключение к базе данных PostgreSQL
conn = regbase.create_conn()
cursor = conn.cursor()

# Имя таблицы
table_name = 'material_lager'

# Чтение данных из файла XLSX
xlsx_file_path = 'material.xlsx'  # Укажите путь к вашему файлу XLSX
df = pd.read_excel(xlsx_file_path)

# Проверка существования таблицы
cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
table_exists = cursor.fetchone()[0]

# Если таблицы нет, создаем ее
if not table_exists:
    # Определяем типы данных для каждого столбца в PostgreSQL
    column_types = {
        'bar_code': 'TEXT',
        'bedeutung': 'TEXT',
        'größe': 'TEXT',
        'bestand_lager': 'INTEGER',
        'aktueller_bestand': 'INTEGER'
    }

    # Формируем строку для создания таблицы
    columns_str = ', '.join([f'{column} {data_type}' for column, data_type in column_types.items()])
    create_table_query = f'CREATE TABLE {table_name} ({columns_str})'
    
    cursor.execute(create_table_query)

# Проверка существования колонок
for column in df.columns:
    # Игнорируем столбец "Unnamed"
    if column.startswith("Unnamed"):
        continue
    
    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{table_name}' AND column_name = '{column}')")
    column_exists = cursor.fetchone()[0]
    
    # Если колонки нет, добавляем ее
    if not column_exists:
        # Определяем тип данных для столбца
        data_type = 'TEXT'  # По умолчанию устанавливаем тип TEXT
        if pd.api.types.is_integer_dtype(df[column]):
            data_type = 'INTEGER'
        
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN {column} {data_type}"
        cursor.execute(add_column_query)

# Вставка данных в таблицу (только непустые значения)
for index, row in df.dropna().iterrows():
    values = tuple(row[column] for column in df.columns)
    insert_query = f"INSERT INTO {table_name} VALUES {values}"
    cursor.execute(insert_query)

# Фиксация изменений и закрытие соединений
conn.commit()
conn.close()
