import sqlite3
import psycopg2

# Подключение к базе данных SQLite
sqlite_conn = sqlite3.connect('bd.db')
sqlite_cursor = sqlite_conn.cursor()

# Подключение к базе данных PostgreSQL
postgres_conn = psycopg2.connect(
    dbname='public.lager_bestand',
    user='	rblliwai',
    password='09thJLB-NkZ6M1poVSRkhe88CPM_yljX',
    host='surus.db.elephantsql.com',
    port='5432'
)
postgres_cursor = postgres_conn.cursor()

# Извлечение данных из SQLite и загрузка их в PostgreSQL
sqlite_cursor.execute('SELECT * FROM Lager_Bestand')
rows = sqlite_cursor.fetchall()

for row in rows:
    postgres_cursor.execute('INSERT INTO Lager_Bestand (bar_code, vz_nr, bedeutung, größe, bestand_lager, aktueller_bestand) VALUES (%s, %s, %s, %s, %s, %s)', row)


# Фиксация изменений и закрытие соединений
postgres_conn.commit()
sqlite_conn.close()
postgres_conn.close()
