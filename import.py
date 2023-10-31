import sqlite3
import pandas as pd

# Установите соединение с базой данных SQLite
conn = sqlite3.connect("bd.db")

# Замените 'your_excel_file.xlsx' на путь к вашему файлу Excel
excel_file_path = 'material.xlsx'

# Загрузите данные из Excel в DataFrame с помощью pandas
df = pd.read_excel(excel_file_path)

# Замените 'Lager_Bestand' на имя вашей таблицы SQLite, если оно отличается
table_name = 'Material_Lager'

# Запишите данные из DataFrame в базу данных SQLite
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Закройте соединение с базой данных
conn.close()

print("Данные успешно импортированы в таблицу Lager_Bestand в базе данных bd.db.")
