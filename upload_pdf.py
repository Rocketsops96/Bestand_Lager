import tkinter as tk
from tkinter import filedialog
import base64
import psycopg2
import regbase

def encode_pdf_to_base64(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
    return encoded_pdf

# Создаем окно tkinter
root = tk.Tk()
root.withdraw()  # скрываем основное окно

# Показываем диалог выбора файла для PDF
pdf_file_path = filedialog.askopenfilename(title="Выберите PDF файл", filetypes=[("PDF files", "*.pdf")])

# Если файл не выбран, выход из программы
if not pdf_file_path:
    print("PDF file not selected. Exiting.")
    exit()



# Кодируем PDF в base64
encoded_pdf = encode_pdf_to_base64(pdf_file_path)



# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Преобразование списка в строку с разделителем запятой


# Вставка изображений и PDF в базу данных
cursor.execute("INSERT INTO images (image_data) VALUES (%s)", (encoded_pdf,))

# Коммит изменений в базе данных
conn.commit()

# Закрытие курсора и соединения
cursor.close()
conn.close()
