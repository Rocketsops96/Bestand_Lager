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
pdf_file_paths = filedialog.askopenfilenames(title="Выберите PDF файлы", filetypes=[("PDF files", "*.pdf")])

# Если файлы не выбраны, выход из программы
if not pdf_file_paths:
    print("No PDF files selected. Exiting.")
    exit()

# Кодируем PDF-файлы в base64 и добавляем их в список pdf_files_base64
pdf_files_base64 = []
for pdf_file_path in pdf_file_paths:
    pdf_files_base64.append(encode_pdf_to_base64(pdf_file_path))

# Подключение к вашей базе данных PostgreSQL
conn = regbase.create_conn()

# Создание объекта курсора
cursor = conn.cursor()

# Преобразование списка в строку с разделителем запятой
combined_pdf_files = ','.join(pdf_files_base64)

# Вставка PDF-файлов в базу данных
cursor.execute("INSERT INTO images (image_data) VALUES (%s)", (combined_pdf_files,))

# Коммит изменений в базе данных
conn.commit()

# Закрытие курсора и соединения
cursor.close()
conn.close()
