import customtkinter
import regbase
from tkcalendar import DateEntry
import threading
import time
from tkinter import filedialog
import base64
from win10toast import ToastNotifier
import os
from tkinter import StringVar
from PIL import Image
from tkinter import ttk
import psycopg2

class Material(customtkinter.CTkToplevel):

    def __init__(self, parent, conn, product_kostenstelle, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.kostenstelle = product_kostenstelle
        self.conn = regbase.create_conn()  # Убедитесь, что у вас есть функция для создания соединения с базой данных
        self.iconbitmap(default=r"vvo.ico")
        self.geometry('1280x720+300+180')
        self.title('VVO')
        self.resizable(False, False)
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.table_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10, side="left", anchor="n")

        table_style = ttk.Style()
        table_style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="black")
        table_style.configure("Treeview", font=("Arial", 14), foreground="white", rowheight=30)
        table_style.configure("Treeview", background="#333333")

        self.table = ttk.Treeview(self.table_frame, columns=("Plan Nr..", "Größe", "Anzahl"), style="Treeview", height=10)
        self.table.pack(fill="both", expand=True, padx=(10, 10), pady=(10, 10))

        # Настроим столбцы таблицы для растягивания
        self.table.column("#0", width=0, stretch=False)
        self.table.column("#1", anchor="w", width=0, stretch=True)
        self.table.column("#2", anchor="center", width=120, stretch=True,)
        self.table.column("#3", anchor="center", width=100, stretch=True)

        
        self.table.heading("#1", text="VZP.Nr.")
        self.table.heading("#2", text="Größe.")
        self.table.heading("#3", text="Anzahl")
       
        self.load_data()

        self.filter_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", expand=False, padx=10, pady=10, side="top", anchor="n")
        self.image_search = customtkinter.CTkImage(light_image=Image.open("images/search.png"), dark_image=Image.open("images/search.png"), size=(20, 20))
        self.image_show_all = customtkinter.CTkImage(light_image=Image.open("images/show_all.png"),dark_image=Image.open("images/show_all.png"),size=(20, 20))
        # Поле для ввода номера плана
        self.plan_number_label = customtkinter.CTkLabel(self.filter_frame, text="Plan Nr:")
        self.plan_number_label.pack(side="left", padx=5, pady=5)

        self.plan_number_entry = customtkinter.CTkEntry(self.filter_frame,placeholder_text="Suchen:", width= 250, height=28, corner_radius = 3)
        self.plan_number_entry.pack(side="left", padx=5, pady=5)

        # Кнопка применить фильтр
        self.apply_button = customtkinter.CTkButton(self.filter_frame, image = self.image_search, text="",corner_radius=2, height=28, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),anchor="center", command=self.apply_filter)
        self.apply_button.pack(side="left", padx=5, pady=5)
 

        # Кнопка показать весь список
        self.show_all_button = customtkinter.CTkButton(self.filter_frame, image=self.image_show_all, text="",corner_radius=2, height=28, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),anchor="center", command=self.load_data)
        self.show_all_button.pack(side="left", padx=5, pady=5)






        self.plan_number_entry.bind('<Return>', lambda event=None: self.apply_filter())
        self.bind("<Escape>", self.show_all)
    
    def load_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT plan_number, vz_nr, größe, quantity FROM test2 WHERE kostenstelle = %s", (self.kostenstelle,))
        results = cursor.fetchall()
        
        # Debug: выводим результаты запроса
        print("Results from database:", results)

        # Подсчет суммарного количества по Plan Number и Größe
        data_dict = {}
        for row in results:
            plan_number, vzp_nr, größe, quantity = row
            quantity = int(quantity)  # Убедимся, что quantity интерпретируется как число
            key = (plan_number, größe)
            if key in data_dict:
                data_dict[key]['Anzahl'] += quantity
            else:
                data_dict[key] = {'VZP.Nr.': vzp_nr, 'Plan Nr.': plan_number, 'Anzahl': quantity}

        # Очистка таблицы перед вставкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Debug: выводим данные перед вставкой в таблицу
        print("Data to be inserted into the table:", data_dict)

        # Вставка данных в таблицу
        for key, data in data_dict.items():
            self.table.insert("", "end", values=( data['Plan Nr.'], key[1], data['Anzahl']))

    def apply_filter(self):
        plan_number = self.plan_number_entry.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT plan_number, vz_nr, größe, quantity FROM test2 WHERE kostenstelle = %s AND plan_number = %s", (self.kostenstelle, plan_number))
        results = cursor.fetchall()
        
        # Debug: выводим результаты запроса
        print("Filtered results from database:", results)

        # Подсчет суммарного количества по Plan Number и Größe
        data_dict = {}
        for row in results:
            plan_number, vzp_nr, größe, quantity = row
            quantity = int(quantity)  # Убедимся, что quantity интерпретируется как число
            key = (plan_number, größe)
            if key in data_dict:
                data_dict[key]['Anzahl'] += quantity
            else:
                data_dict[key] = {'VZP.Nr.': vzp_nr, 'Plan Nr.': plan_number, 'Anzahl': quantity}

        # Очистка таблицы перед вставкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Debug: выводим данные перед вставкой в таблицу
        print("Filtered data to be inserted into the table:", data_dict)

        # Вставка данных в таблицу
        for key, data in data_dict.items():
            self.table.insert("", "end", values=(data['Plan Nr.'], key[1], data['Anzahl']))

    def show_all(self, event=None):
        self.load_data()

    def on_closing(self, event=0):
        self.conn.close()
        self.destroy()

# Пример использования
# root = customtkinter.CTk()
# conn = regbase.create_conn()
# Material(root, conn, product_kostenstelle='some_value')
# root.mainloop()
