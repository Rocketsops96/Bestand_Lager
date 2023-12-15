import openpyxl
from openpyxl.styles import Font

def insert_data_into_excel(document_path, data_dict):
    # Открываем существующий Excel-файл
    wb = openpyxl.load_workbook(document_path)
    
    # Выбираем активный лист (можно использовать конкретное имя листа, если оно известно)
    sheet = wb.active
    
    # Проходим по каждой паре ключ-значение в словаре и вставляем данные в соответствующие ячейки
    for cell, value in data_dict.items():
        sheet[cell].value = value
        # Устанавливаем шрифт Calibri размером 18
        sheet[cell].font = Font(name='Calibri', size=18)
    
    # Сохраняем изменения в Excel-файле
    wb.save(document_path)

    # Закрываем файл
    wb.close()