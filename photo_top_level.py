import customtkinter
from customtkinter import CTkCheckBox
import regbase
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image
from io import BytesIO
import base64
import threading
from datetime import datetime
from win10toast import ToastNotifier
import subprocess
from sys import platform

class Photo_menu(customtkinter.CTkToplevel):
    def __init__(self,parent,product_kostenstelle, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        self.conn = regbase.create_conn()
        self.geometry("400x300")
        self.state("zoomed")
        self.title("Bilder")
        self.product_kostenstelle= product_kostenstelle

        self.table_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True)

        self.button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill="both", expand=True)


        table_style = ttk.Style()
        table_style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="black")  # Для заголовков столбцов 
        table_style.configure("Treeview", font=("Arial", 14), foreground="white", rowheight=30)  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
        self.table = ttk.Treeview(self.table_frame, columns=("","id","Kapo", "Kostenstelle", "VZ Nr.", "Aktion", "Datum"), style="Treeview", height=10)
        self.table.pack(fill="both", expand=True)
       
        self.table.column("#0", width=0, stretch=False)
        self.table.column("#1", width=50)
        self.table.column("#2", minwidth=100)
        self.table.column("#3", minwidth=100)
        self.table.column("#4", minwidth=100)
        self.table.column("#5", minwidth=100)
        self.table.column("#6", minwidth=100)
        
        # Добавляем заголовки столбцов
        self.table.heading("#1", text="id")
        self.table.heading("#2", text="Kapo")
        self.table.heading("#3", text="Kostenstelle")
        self.table.heading("#4", text="VZ Nr.")
        self.table.heading("#5", text="Aktion")
        self.table.heading("#6", text="Datum")

        self.download_all_photo = customtkinter.CTkButton(self.button_frame, corner_radius=0, height=40, text="Alles herunterladen", font=("Arial", 14, "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.threading_download_all)
        self.download_all_photo.pack(side = "left", anchor = "n")


        self.show_all_data()


        self.table.bind("<<TreeviewSelect>>", self.download_photo)

    def threading_download_all(self):
        threading.Thread(target=self.download_all).start()

    def download_all(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Save Images")
        cursor = self.conn.cursor()
        cursor.execute("SELECT photo_data, bau, date_ab FROM sicherung WHERE bau = %s", (self.product_kostenstelle,))
        rows = cursor.fetchall()

        if folder_path:
            # Создаем папку для сохранения изображений
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for row in rows:
                data1 = row[1]

                if row[0] is not None:
                    image_data_array = bytes(row[0]).decode('utf-8').split(',')

                    for i, image_data in enumerate(image_data_array):
                        try:
                            image_data_decoded = base64.b64decode(image_data)
                            image = Image.open(BytesIO(image_data_decoded))

                            if hasattr(image, '_getexif'):
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

                            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                            image_path = os.path.join(folder_path, f"{data1}_{i+1}_{timestamp}.jpeg")
                            image.save(image_path, "JPEG", quality=20)
                        except Exception as e:
                            print(f"Ошибка обработки изображения {i+1}: {e}")
                else:
                    print(f"Данные не найдены для id = {self.product_kostenstelle}")
                threading.Thread(target=self.show_notification, args=("Уведомление", "Изображения успешно загружены!")).start()
    
    def show_all_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_capo, bau, vzp, action, date_ab FROM sicherung WHERE bau = %s",(self.product_kostenstelle,))
        data= cursor.fetchall()
        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)
        # Вставляем данные в таблицу
        for item in data:
            self.table.insert("", "end", values=item)

    def threading_download_photo(self,event,selected_item):
        threading.Thread(target=self.download_photo, args=(selected_item)).start()

    def download_photo(self, event):
        selected_item = self.table.selection()
        if selected_item:
            id = self.table.item(selected_item, "values")[0] 
            print(id)
            folder_path = filedialog.askdirectory(title="Select Folder to Save Images")
            cursor = self.conn.cursor()
            cursor.execute("SELECT photo_data, bau, date_ab FROM sicherung WHERE id = %s", (id,))
            row = cursor.fetchone()

            if row is not None:
                data1 = row[1]
                data2 = row[2]

        if folder_path:
            # Преобразуйте строку даты в объект datetime
            date_object = datetime.strptime(data2, "%Y-%m-%d %H:%M:%S")
            # Получите только год, месяц и день
            year_month_day = date_object.strftime("%d-%m-%Y")

            # Создаем папку для сохранения изображений
            folder_name = f"{data1} - {year_month_day}"
            folder_path = os.path.join(folder_path, folder_name)

            # Проверяем, существует ли папка, и создаем, если нет
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Извлечение строки
            if row is not None:
                # Проверяем, что данные не являются None
                if row[0] is not None:
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

                            # Путь для сохранения изображения
                            image_path = os.path.join(folder_path, f"{data1}_{i+1}_{year_month_day}.jpeg")

                            # Проверка наличия файла перед сохранением
                            if not os.path.exists(image_path):
                                # Сохранение изображения
                                image.save(image_path, "JPEG", quality=20)
                            else:
                                print(f"File {image_path} already exists, skipping.")
                        except Exception as e:
                            print(f"Error processing image {i+1}: {e}")
                else:
                    print(f"No data found for id = {self.product_kostenstelle}")
            threading.Thread(target=self.show_notification, args=("Уведомление", "Изображения успешно загружены!")).start()

    def show_notification(self, title, message):
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)
        

