import customtkinter
import customtkinter as CTk
import sqlite3
from PIL import Image, ImageTk
from tkinter import *
from tkinter.simpledialog import askstring
import BestandLagerWindow
import PIL.Image
from CTkListbox import *

customtkinter.set_appearance_mode("dark")

class TableListWindow(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Список таблиц в базе данных")
        self.iconbitmap(default=r"vvo.ico")
        self.geometry("800x500+700+400")

        # Подключитесь к базе данных
        self.conn = sqlite3.connect("bau.db")
        self.cursor = self.conn.cursor()

        # Получите список таблиц из базы данных
        self.tables = self.get_table_list()


        self.f1 = customtkinter.CTkFrame(self, width=400)
        self.f1.grid( row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f2 = customtkinter.CTkFrame(self, width=400)
        self.f2.grid( row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # Создайте список для отображения таблиц
        self.table_listbox = CTkListbox(self.f1, width=240, height=10)
        self.table_listbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Заполните список таблицами
        for table in self.tables:
            self.table_listbox.insert(CTk.END, table)

        # Создайте кнопку для выбора таблицы
        self.select_button = CTk.CTkButton(self.f2, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Выбрать таблицу", command=self.select_table)
        self.select_button.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Создайте кнопку для создания новой таблицы
        self.create_button = CTk.CTkButton(self.f2, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Создать новую таблицу", command=self.create_table)
        self.create_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def get_table_list(self):
        # Получите список таблиц из базы данных
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = self.cursor.fetchall()
        return [table[0] for table in table_list]

    def select_table(self):
        # Получите выбранную таблицу из списка
        selected_table = self.table_listbox.get(self.table_listbox.curselection())




        # Закройте соединение с базой данных и окно
        self.cursor.close()
        self.conn.close()
        self.destroy()

        # В этом месте вы можете выполнить действия с выбранной таблицей

    def create_table(self):
        # Запросите имя новой таблицы с помощью диалогового окна
        table_name = askstring("Создание новой таблицы", "Введите название новой таблицы:")

        if table_name:
            # Создайте новую таблицу в базе данных
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY, Name TEXT, Value REAL);")
            self.conn.commit()

            # Обновите список таблиц
            self.tables = self.get_table_list()
            self.table_listbox.delete(0, CTk.END)  # Очистите список
            for table in self.tables:
                self.table_listbox.insert(CTk.END, table)

if __name__ == '__main__':
    app = TableListWindow()
    app.mainloop()
