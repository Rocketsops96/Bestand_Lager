import psycopg2
import base64
from io import BytesIO
import regbase

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Выполнение SQL-запроса для извлечения данных из столбца pdf_data
cursor.execute("SELECT pdf_data FROM bau WHERE id = 1")

# Извлечение строки
row = cursor.fetchone()

if row:
    # Преобразование объекта memoryview в строку для PDF
    pdf_data_array = bytes(row[0]).decode('utf-8').split(',')

    # Декодирование и сохранение каждого PDF-файла
    for i, pdf_data in enumerate(pdf_data_array):
        try:
            # Декодирование из формата base64
            pdf_data_decoded = base64.b64decode(pdf_data)
            
            # Сохранение PDF-файла на диск
            with open(f"downloaded_pdf_{i+1}.pdf", 'wb') as pdf_file:
                pdf_file.write(pdf_data_decoded)
        except Exception as e:
            print(f"Error processing PDF {i+1}: {e}")
else:
    print("No data found for id = 37")

# Закрытие курсора и соединения
cursor.close()
conn.close()
