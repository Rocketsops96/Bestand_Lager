import customtkinter
import customtkinter as CTk
import sqlite3
from tkinter import *
from tkinter import ttk
import Autorisation
import PIL.Image
from CTkListbox import *
from tkinter.simpledialog import askstring
import tkinter.messagebox
from CTkTable import *
import export_to_exel
import os
import localizations



customtkinter.set_appearance_mode("dark")

class BestandLager(CTk.CTk):
    def __init__(self): # После теста добавить аргумент login и не забыть убрать комментарий ниже!!!!
        super().__init__()
        self.language = self.load_language_from_file()  # Загружаем язык из файла
        # Установите геометрию окна
        self.geometry("1280x720")
        self.iconbitmap(default=r"vvo.ico")
        self.title("Bestand Lager")
        self.resizable(True, True)  # Запрещаем или разрешаем изменение размера окна
        self.state("zoomed")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #Создаем навигационный фрейм
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)


        #Создаем текст вверху слева
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="VVO Bestand Lager", 
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home", font=("Arial", 14, "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2", font=("Arial", 14, "bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3", font=("Arial", 14, "bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        
        self.language_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Русский","English","Deutsch"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.update_ui_language)
        self.language_menu.grid(row=7, column=0, padx=20, pady=(10, 0), sticky= "s")
        self.saved_language = self.load_language_from_file()
        self.language_menu.set(self.saved_language)

        # Вызовите update_ui_language с текущим языком
        
       
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["60%","70%","80%", "90%", "100%", "110%", "120%"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky= "s")
        self.scaling_optionemenu.set("100%")


        #Создаем фреймы для каждого окна
        self.f1 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f1.grid_columnconfigure(0, weight=1)
        self.f1.grid_rowconfigure(0, weight=1)
        self.f1.grid_rowconfigure(1, weight=0)
     

        self.f2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f2.grid_columnconfigure(0, weight=0)
        self.f2.grid_columnconfigure(1, weight=0)
        self.f2.grid_columnconfigure(2, weight=1)

        self.f3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f3.grid_columnconfigure(0, weight=1)

        #Создаем дефолтный фрейм
        self.select_frame_by_name("home")



############## ############## ############## ############## #Настройка фрейма №1 ############## ############## ############## ############## ############## 
        
        table_style = ttk.Style()
        table_style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="black")  # Для заголовков столбцов 
        table_style.configure("Treeview", font=("Arial", 14), foreground="white")  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
        self.table = ttk.Treeview(self.f1, columns=("","Bar Code", "VZ Nr.", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.table.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
       
        
        
        self.table.column("#0", width=0, stretch=False)
        self.table.column("#1", minwidth=120)
        self.table.column("#2", minwidth=100)
        self.table.column("#3", minwidth=700)
        self.table.column("#4", minwidth=100)
        self.table.column("#5", minwidth=70)
        self.table.column("#6", minwidth=150)
        self.table.column("#7", width=0, stretch=False)
        
        # Добавляем заголовки столбцов
        
        self.table.heading("#1", text="Bar Code")
        self.table.heading("#2", text="VZ Nr.")
        self.table.heading("#3", text="Bedeutung")
        self.table.heading("#4", text="Größe")
        self.table.heading("#5", text="Lager")
        self.table.heading("#6", text="Aktueller")


        self.home_frame1 = customtkinter.CTkFrame(self.f1,fg_color="transparent")
        self.home_frame1.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame1.grid_columnconfigure(0, weight=1)
        self.home_frame2 = customtkinter.CTkFrame(self.f1,fg_color="transparent")
        self.home_frame2.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame2.grid_columnconfigure(1, weight=1)
    
        

        self.bar_code = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Bar Code:", width= 250)
        self.bar_code.grid(column= 0, row=0, padx=(10, 10), pady=(10, 10), sticky="nw",)
        

        self.vz_nr = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Vz Nr.:", width= 250)
        self.vz_nr.grid(column= 0, row=1, padx=(10, 10), pady=(0, 10), sticky="nw",)

        self.plus = customtkinter.CTkButton(master=self.home_frame1, corner_radius=5, height=40, width=250, border_spacing=10, text="Search",
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.kol2)
        self.plus.grid(column = 0,row=2, padx=(10,10), pady=(0, 10), sticky="nw")

        self.show_all = customtkinter.CTkButton(master=self.home_frame1, corner_radius=5, height=40, width=250, border_spacing=10, text="Show all",
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.show_all_data)
        self.show_all.grid(column = 0,row=3, padx=(10,0), pady=(0, 10), sticky="nw")

        self.export_to_exel_button = customtkinter.CTkButton(master=self.home_frame1, corner_radius=5, height=40, width=250, border_spacing=10, text="Export to Excel all",
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.export_to_excel_button_click)
        self.export_to_exel_button.grid(column = 0,row=4, padx=(10,0), pady=(0, 10), sticky="nw")

############## ############## ############## ############## #Настройка фрейма №2 ############## ############## ############## ############## ##############        
        self.conn = sqlite3.connect("bau.db")
        self.cursor = self.conn.cursor()
        
        self.bau_list_frame = customtkinter.CTkFrame(self.f2)
        self.bau_list_frame.grid(row=0, column=0, padx=(10,10), sticky="nw")
        self.bau_list_frame.grid_columnconfigure(0, weight=1)

        self.bau_button_frame = customtkinter.CTkFrame(self.f2)
        self.bau_button_frame.grid(row=0, column=1, padx=(10,10), sticky="nw")
        self.bau_button_frame.grid_columnconfigure(1, weight=1)

        self.bau_item_frame = customtkinter.CTkFrame(self.f2)
        self.bau_item_frame.grid(row=0, column=2, padx=(10,10), sticky="ne")
        self.bau_item_frame.grid_columnconfigure(2, weight=1)
        
        
        
        self.tables = self.get_table_list()

        # Создайте список для отображения таблиц
        self.table_listbox = CTkListbox(self.bau_list_frame,  height=10)
        self.table_listbox.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # Заполните список таблицами
        for table in self.tables:
            self.table_listbox.insert(CTk.END, table)

        # Создайте кнопку для выбора таблицы
        self.select_button = CTk.CTkButton(self.bau_list_frame, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Выбрать", command=self.select_table_button)
        self.select_button.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Создайте кнопку для создания новой таблицы
        self.create_button = CTk.CTkButton(self.bau_list_frame, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Создать", command=self.create_table)
        self.create_button.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Создайте кнопку для удаления таблицы
        self.delete_button = CTk.CTkButton(self.bau_list_frame, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Удалить", command=self.delete_table)
        self.delete_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        
        self.selcted_bau_table_label = customtkinter.CTkLabel(self.bau_button_frame, text="", 
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.selcted_bau_table_label.grid(row=0, column=0, padx=20, pady=20)

        self.bar_code_f2 = customtkinter.CTkEntry(self.bau_button_frame, placeholder_text="Bar Code:", width= 250)
        self.bar_code_f2.grid(column= 0, row=1, padx=(10, 10), pady=(10, 10), sticky="nsew",)
        

        self.sum = customtkinter.CTkEntry(self.bau_button_frame, placeholder_text="Введите количество", width= 250)
        self.sum.grid(column= 0, row=2, padx=(10, 10), pady=(0, 10), sticky="nsew",)

        self.add_button = CTk.CTkButton(self.bau_button_frame, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Отправить", command=self.add_button_bau)
        self.add_button.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")





        
        self.item_table = ttk.Treeview(self.bau_item_frame, columns=("","VZ Nr.", "Bedeutung","Bestand"), style="Treeview", height=24)
        self.item_table.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
       
        self.item_table.column("#0", width=0, stretch=False)
        self.item_table.column("#1", width=150)
        self.item_table.column("#2", width=250)
        self.item_table.column("#3", width=150)
        self.item_table.column("#4", width=0, stretch=False)
       
        # Добавляем заголовки столбцов
        
        self.item_table.heading("#1", text="VZ Nr.")
        self.item_table.heading("#2", text="Bedeutung")
        self.item_table.heading("#3", text="Bestand")

        self.after(100, lambda: self.bar_code_f2.focus_set())
        self.add_button.bind('<Return>', lambda event=None: self.add_button_bau())

############## ############## ############## ############## #Настройка фрейма №3 ############## ############## ############## ############## ############## 
        




    
        
        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
        self.bar_code_f2.bind('<Return>', lambda event=None: self.add_button_bau())
        self.sum.bind('<Return>', lambda event=None: self.add_button_bau())

        self.update_ui_language(self.language)
        self.update()


        # self.login = login
        self.barcode = None
        self.error_label= None
        

        self.show_all_data()
    

    def export_to_excel_button_click(self):
        try:
            export_to_exel.export_to_excel()  # Вызываем функцию из другого файла
            print("Файл Excel успешно создан.")
        except Exception as e:
            print("Произошла ошибка при создании файла Excel:", str(e))

    # Проверяем наличие файла Excel
        if os.path.exists("Bestand_Lager.xlsx"):
            print("Файл Excel уже существует.")
        
    def add_button_bau(self):
        print(self.selected_table)
        self.barcode_f2 = self.bar_code_f2.get()
        self.sum_value = self.sum.get()  # Сохраняем значение суммы как атрибут объекта
        
        # Создаем контекстные менеджеры для соединений, и здесь не нужно закрывать соединение с базой
        with sqlite3.connect("bd.db") as conn_bd, sqlite3.connect("bau.db") as conn_bau:
            cursor_bd = conn_bd.cursor()
            cursor_bau = conn_bau.cursor()

            # Выполняем операцию SELECT в базе данных "bd.db"
            data = cursor_bd.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode_f2,)).fetchone()
            bar = data[0]
            vz = data[1]
            bed = data[2]
            akt = data[3]
            
            try:
                # Проверяем наличие товара в таблице
                cursor_bau.execute(f"SELECT * FROM {self.selected_table} WHERE Bar_Code = ?", (bar,))
                existing_product = cursor_bau.fetchone()
                
                if existing_product:
                    # Если товар уже существует, обновляем Bestand
                    cursor_bau.execute(f"UPDATE {self.selected_table} SET Bestand = ? WHERE Bar_Code = ?", (self.sum_value, bar))
                else:
                    # Если товар не существует, добавляем новую запись
                    cursor_bau.execute(f"INSERT INTO {self.selected_table} (Bar_Code, VZ_Nr, Bedeutung, Bestand) VALUES (?, ?, ?, ?)", (bar, vz, bed, self.sum_value))
                
                conn_bau.commit()
                 # Очищаем таблицу программы перед добавлением новых данных
                for row in self.item_table.get_children():
                    self.item_table.delete(row)

                # Загружаем все данные из выбранной таблицы и выводим их в таблицу программы
                cursor_bau.execute(f"SELECT VZ_Nr, Bedeutung, Bestand FROM {self.selected_table}")
                data = cursor_bau.fetchall()
                for item in data:
                    self.item_table.insert("", "end", values=item)
                self.bar_code_f2.delete(0, 'end')
                self.sum.delete(0, 'end') 
                self.after(50, lambda: self.bar_code_f2.focus_set())
                
                
            except sqlite3.Error as e:
                print("Ошибка SQLite:", e)

    def delete_table(self):
        selected_table = self.table_listbox.get(self.table_listbox.curselection())
        if selected_table:
            # Открываем диалоговое окно с вопросом
            confirmation = tkinter.messagebox.askyesno("Подтверждение", f"Вы уверены что хотите удалить таблицу '{selected_table}'?")
            
            if confirmation:
                # Удалите таблицу из базы данных
                self.cursor.execute(f"DROP TABLE IF EXISTS {selected_table};")
                self.conn.commit()

                # Обновите список таблиц
                self.tables = self.get_table_list()
                self.table_listbox.delete(0, CTk.END)  # Очистите список
                for table in self.tables:
                    self.table_listbox.insert(CTk.END, table)

    def create_table(self):
        # Запросите имя новой таблицы с помощью диалогового окна

        dialog = customtkinter.CTkInputDialog(text="Введите название стройки или номер", title="Baustelle")
        dialog.geometry("300x200")
        text = dialog.get_input()  # waits for input

        if text:
            # Создайте новую таблицу в базе данных
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {text} (Bar_Code TEXT, VZ_Nr TEXT, Bedeutung TEXT, Bestand TEXT);")
            self.conn.commit()

            if self.table_listbox.size() > 0:
                self.table_listbox.delete(0, customtkinter.CTk.END)
            # Обновляем список таблиц, вызывая функцию get_table_list()
            self.tables = self.get_table_list()
            for table in self.tables:
                self.table_listbox.insert(CTk.END, table)

    def get_table_list(self):
        # Получите список таблиц из базы данных
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = self.cursor.fetchall()
        return [table[0] for table in table_list]

    def select_table_button(self):
        selected_table = self.table_listbox.get(self.table_listbox.curselection())
        if selected_table:
            self.selected_table = selected_table  # Сохраняем имя выбранной таблицы
            if self.selcted_bau_table_label:
                self.selcted_bau_table_label.destroy()
                self.selcted_bau_table_label = customtkinter.CTkLabel(self.bau_button_frame, text=f"Вы выбрали: {selected_table}", 
                                                                font=customtkinter.CTkFont(size=15, weight="bold"))
                self.selcted_bau_table_label.grid(row=0, column=0, padx=20, pady=20)
        # Очищаем таблицу программы перед добавлением новых данных
        for row in self.item_table.get_children():
            self.item_table.delete(row)
        
        # Загружаем данные из выбранной таблицы и выводим их в таблицу программы
        with sqlite3.connect("bau.db") as conn_bau:
            cursor_bau = conn_bau.cursor()
            cursor_bau.execute(f"SELECT VZ_Nr, Bedeutung, Bestand FROM {selected_table}")
            data = cursor_bau.fetchall()
            for item in data:
                self.item_table.insert("", "end", values=item)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        font = ("Arial", int(14 * new_scaling_float))
        style = ttk.Style()
        style.configure("Treeview", font=font)

        print("сработало")


    def update_ui_language(self, language):      
        # Получите словарь с текстами для выбранного языка
        texts = localizations.language_texts.get(language, {})
        
        # Обновите тексты для виджетов, кнопок, лейблов и других элементов
        self.home_button.configure(text=texts.get("Home", "Home"))
        self.plus.configure(text=texts.get("Search", "Search"))
        self.show_all.configure(text=texts.get("Show all", "Show all"))
        self.export_to_exel_button.configure(text=texts.get("Export to Excel", "Export to Excel"))
        self.select_button.configure(text=texts.get("Choose", "Choose"))
        self.create_button.configure(text=texts.get("Create a construction site", "Create a construction site"))
        self.home_button.configure(text=texts.get("Home", "Default Text"))
        self.home_button.configure(text=texts.get("Home", "Default Text"))
        self.home_button.configure(text=texts.get("Home", "Default Text"))

        selected_language = language
        self.save_language_to_file(selected_language)





    def show_img_for_barcode(self, barcode):
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT VZ_Nr FROM Lager_Bestand WHERE Bar_Code = ?", (barcode,)).fetchone()
        
        if data is not None:
            vznr = data[0]
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .png

            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует

                self.image_label = CTk.CTkLabel(self.home_frame2, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=0, pady=0, sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}
        
        cursor.close()
        conn.close()

    def show_img_for_vz(self, vz):
        
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT VZ_Nr FROM Lager_Bestand WHERE VZ_Nr = ?", (vz,)).fetchone()

        if data is not None:
            vznr = data[0]
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .png

            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует

                self.image_label = CTk.CTkLabel(self.home_frame2, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}")
        
        cursor.close()
        conn.close()   

    def kol2(self):
        self.barcode = self.bar_code.get()
        self.vz = self.vz_nr.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        # Получаем данные из базы данных (замените на ваш SQL-запрос)
        data = cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = ? OR VZ_Nr = ?", (self.barcode, self.vz)).fetchall()
        
        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)

        if data:
            for item in data:
                # Добавляем новые строки с данными в таблицу
                self.show_img_for_barcode(self.bar_code.get())
                self.show_img_for_vz(self.vz_nr.get())
                self.table.insert("", "end", values=item)
        elif self.barcode == "" and self.vz == "":
            print("Сработало")
            self.result_show("Забыл ввести данные")
        else:
            self.result_show("Данных не найдено")
        self.bar_code.delete(0, 'end')
        self.vz_nr.delete(0, 'end')
        cursor.close()
        conn.close()

    def check_vz_nr(self, event):
        # Функция вызывается при изменении баркода
        if self.bar_code.get():
            # Если баркод не пустой, очищаем поле Vz Nr
            self.vz_nr.delete(0, 'end')
        
    def check_barcode(self, event):
        # Функция вызывается при изменении Vz Nr
        if self.vz_nr.get():
            # Если Vz Nr не пустой, очищаем поле баркода
            self.bar_code.delete(0, 'end')
        
    def show_all_data(self):
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        
        # Получаем все записи из таблицы "Lager_Bestand"
        data = cursor.execute("SELECT * FROM Lager_Bestand").fetchall()
        
        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)
        if hasattr(self, "image_label"):
                self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        if self.error_label:
            self.error_label.destroy()
        # Вставляем данные в таблицу
        for item in data:
            self.table.insert("", "end", values=item)
        
        cursor.close()
        conn.close()    

    def select_frame_by_name(self, name):
        # Ставим цвет для активной кнопки
        self.home_button.configure(fg_color=("red") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("red") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("red") if name == "frame_3" else "transparent")

        # Показываем включенный фрейм
        if name == "home":
            self.f1.grid(row=0, column=1, sticky="nsew")
        else:
            self.f1.grid_forget()
        if name == "frame_2":
            self.f2.grid(row=0, column=1, sticky="nsew")
        else:
            self.f2.grid_forget()
        if name == "frame_3":
            self.f3.grid(row=0, column=1, sticky="nsew")
        else:
            self.f3.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def on_item_select(self, event):
        selected_items = self.table.selection()
        if selected_items:
            selected_item = selected_items[0]
            vznr = self.table.item(selected_item, "values")[1]  # Получаем значение Bar Code из выбранной строки
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .jpg
            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
                if self.error_label:
                    self.error_label.destroy()

                self.image_label = CTk.CTkLabel(self.f1, image=ctk_image, text="")
                self.image_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 0), sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}

    def result_show(self, message):
        if self.error_label:
            self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было
        if hasattr(self, "image_label"):
                self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        self.error_label = CTk.CTkLabel(self.home_frame2, font=('<Arial>', 20)  , bg_color="transparent", text=message, text_color="gray")
        self.error_label.grid( row=0, column=0, padx=0, pady=0, sticky="ne")
        
    def exit (self):
        self.destroy()  # Сворачиваем окно
        new_window = Autorisation.App()
        new_window.mainloop()  # Запускаем главный цикл нового окна
   
    

    def save_language_to_file(self, language):
        with open("language.txt", "w") as file:
            file.write(language)

    # Функция для загрузки выбранного языка из файла
    def load_language_from_file(self):
        try:
            with open("language.txt", "r") as file:
                return file.read()
        except FileNotFoundError:
            # Если файл не найден, вернуть значение по умолчанию (например, "English")
            return "English"


if __name__ == '__main__':
    app = BestandLager()
    app.mainloop()