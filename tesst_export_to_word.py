from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_ALIGN_VERTICAL
import regbase 
data_table2 = None
data_table1 = None
def insert_data_into_tables(input_file, output_file, data_table1, data_table2):
    # Открываем существующий документ Word
    doc = Document(input_file)

    # Выбираем нужные таблицы (предположим, что они находятся в документе)
    try:
        table1 = doc.tables[0]  # Первая таблица
        table2 = doc.tables[1]  # Вторая таблица
    except IndexError:
        print("Ошибка: Не удалось найти одну из таблиц.")
        return

    # Вставляем данные в первую таблицу
    for row_num, row_data in enumerate(data_table1):
        for col_num, cell_data in enumerate(row_data):
            cell = table1.cell(row_num, col_num)
            if not cell.text.strip():
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.clear()
                cell.text = str(cell_data)
                cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].runs[0].font.size = Pt(10)

    # Вставляем данные во вторую таблицу
    for row_num, row_data in enumerate(data_table2):
        for col_num, cell_data in enumerate(row_data):
            cell = table2.cell(row_num, col_num)
            if not cell.text.strip():
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.clear()
                cell.text = str(cell_data)
                cell.paragraphs[0].paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                cell.paragraphs[0].runs[0].font.size = Pt(10)

    # Сохраняем изменения
    doc.save(output_file)

if __name__ == "__main__":
    input_document = "Stundenbericht Verkehrssicherung.docx"
    output_document = "test.docx"
    
    conn = regbase.create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bau WHERE id = 1")
    data = cursor.fetchone()
    data_table1 = [
        ["", data[2], "", "", f"{data[6]}-{data[7]}"],
        ["", "", "", "", ""],
        ["", data[3], "","",data[8]],
        [f"{data[4]},{data[5]}", "","","", data[9]],
    ]

    # Пример данных для второй таблицы
    data_table2 = [
        ["", "", "", "", "", ""],
        ["", "", "", "", "", "","", "", "", "", "", ""],
        [1, "", "", "", "", "","", "", "", "", "", ""],
        [2, "", "", "", "", "","", "", "", "", "", ""],
        [3, "", "", "", "", "","", "", "", "", "", ""],
        [4, "", "", "", "", "","", "", "", "", "", ""],
        [5, "", "", "", "", "","", "", "", "", "", ""],
        [6, "", "", "", "", "","", "", "", "", "", ""],
        [7, "", "", "", "", "","", "", "", "", "", ""],
        [8, "", "", "", "", "","", "", "", "", "", ""],
        [9, "", "", "", "", "","", "", "", "", "", ""],
        [10, "", "", "", "", "","", "", "", "", "", ""],
        [11, "", "", "", "", "","", "", "", "", "", ""],
        [12, "", "", "", "", "","", "", "", "", "", ""],
        [13, "", "", "", "", "","", "", "", "", "", ""],
        [14, "", "", "", "", "","", "", "", "", "", ""],
        [15, "", "", "", "", "","", "", "", "", "", ""],
        [16, "", "", "", "", "","", "", "", "", "", ""],
        ["", "", "", "", "", "","", "", "", "", "", ""],
    ]

    insert_data_into_tables(input_document, output_document, data_table1, data_table2)
