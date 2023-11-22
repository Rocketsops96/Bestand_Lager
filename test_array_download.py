import psycopg2
import base64
from PIL import Image
from io import BytesIO
import regbase

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Выполнение SQL-запроса для извлечения массива base64-строк из столбца image_data_array
cursor.execute("SELECT image_data FROM bau WHERE id = 2")

# Извлечение строки
row = cursor.fetchone()

if row:
    # Преобразование объекта memoryview в строку
    image_data_array = bytes(row[0]).decode('utf-8').split(',')

    # Декодирование и сохранение каждого изображения
    for i, image_data in enumerate(image_data_array):
        try:
            # Декодирование из формата base64
            image_data_decoded = base64.b64decode(image_data)
            
            # Создание объекта изображения
            image = Image.open(BytesIO(image_data_decoded))
            if hasattr(image, '_getexif'):  # проверка на наличие данных ориентации
                exif = image._getexif()
                if exif is not None:
                    orientation = exif.get(0x0112)
                    if orientation is not None:
                        if orientation == 3:
                            image = image.rotate(180, expand=True)
                        elif orientation == 6:
                            image = image.rotate(270, expand=True)
                        elif orientation == 8:
                            image = image.rotate(90, expand=True)
            # Сохранение изображения на диск
            cursor.execute("SELECT kostenstelle_vvo FROM bau WHERE id = 2")
            data = cursor.fetchone()
            data1 = data[0]
            image.save(f"{data1}_{i+1}.jpeg", "JPEG", quality=20)
        except Exception as e:
            print(f"Error processing image {i+1}: {e}")
else:
    print("No data found for id = 9")

# Закрытие курсора и соединения
cursor.close()
conn.close()
