import psycopg2
from PIL import Image
import base64
from io import BytesIO
import regbase

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Выполнение SQL-запроса для извлечения данных из столбца image_data
cursor.execute("SELECT image_data FROM images")

# Извлечение всех строк
rows = cursor.fetchall()

# Декодирование изображений и сохранение на диск
for i, row in enumerate(rows):
    image_data = row[0]
    
    # Проверка наличия данных в image_data
    if image_data:
        try:
            # Декодирование из формата base64
            image_data_decoded = base64.b64decode(image_data)
            
            # Создание объекта изображения
            image = Image.open(BytesIO(image_data_decoded))

            # Поворот изображения в соответствии с ориентацией
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

            # Сохранение изображения на диск с сжатием
            image.save(f"image_{i+1}.jpeg", "JPEG", quality=20)
        except Exception as e:
            print(f"Error processing image {i+1}: {e}")
    else:
        print(f"Image data is empty for row {i+1}")

# Закрытие курсора и соединения
cursor.close()
conn.close()
