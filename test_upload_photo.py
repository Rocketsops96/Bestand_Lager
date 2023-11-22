import tkinter as tk
from tkinter import filedialog
import base64
import psycopg2
import regbase

# Создаем окно tkinter (может потребоваться адаптация для использования в вашем приложении)
root = tk.Tk()
root.withdraw()  # скрываем основное окно

# Показываем диалог выбора файла для одного или нескольких файлов изображений
file_paths = filedialog.askopenfilenames(title="Выберите изображения", filetypes=[("Image files", "*.jpg;*.png")])

# Преобразовываем выбранные изображения в base64 и добавляем их в список images_base64
images_base64 = []
for file_path in file_paths:
    with open(file_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        images_base64.append(image_data)

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Преобразование списка в строку с разделителем запятой
combined_images = ','.join(images_base64)

# Пример SQL-запроса для вставки строки в таблицу
insert_query = "INSERT INTO images (image_data) VALUES (%s)"
cursor.execute(insert_query, (combined_images,))

# Пример коммита транзакции
conn.commit()

# Закрытие курсора и соединения
cursor.close()
conn.close()
