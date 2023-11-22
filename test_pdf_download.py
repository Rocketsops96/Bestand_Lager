import psycopg2
import base64
import regbase

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Выполнение SQL-запроса для извлечения данных из столбца pdf_data
cursor.execute("SELECT image_data FROM images WHERE id = 39")

# Извлечение строки
row = cursor.fetchone()

if row:
    # Преобразование объекта memoryview в строку для PDF
    pdf_data = row[0]
    
    # Декодирование PDF из формата base64
    pdf_data_decoded = base64.b64decode(pdf_data)
    
    # Сохранение PDF на диск
    with open("downloaded_pdf.pdf", 'wb') as pdf_file:
        pdf_file.write(pdf_data_decoded)

else:
    print("No data found for id = 37")

# Закрытие курсора и соединения
cursor.close()
conn.close()
