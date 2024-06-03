import customtkinter
import regbase
from tkcalendar import DateEntry
from tkinter import filedialog
from win10toast import ToastNotifier
from tkinter import StringVar
from PIL import Image
from tkinter import ttk
import os


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
        self.table.column("#2", anchor="center", width=120, stretch=True)
        self.table.column("#3", anchor="center", width=100, stretch=True)

        self.table.heading("#1", text="VZP.Nr.")
        self.table.heading("#2", text="Größe.")
        self.table.heading("#3", text="Anzahl")

        # Добавим команду для сортировки по заголовку "Plan Nr."
        self.table.heading("#1", text="VZP.Nr.", command=self.sort_by_plan_number)

        self.sort_ascending = False  # Флаг для отслеживания порядка сортировки

        self.load_data()

        self.filter_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", expand=False, padx=10, pady=10, side="top", anchor="n")

        self.second_button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.second_button_frame.pack(fill="x", expand=False, padx=10, pady=10, side="top", anchor="n")

        self.image_search = customtkinter.CTkImage(light_image=Image.open("images/search.png"), dark_image=Image.open("images/search.png"), size=(20, 20))
        self.image_show_all = customtkinter.CTkImage(light_image=Image.open("images/show_all.png"), dark_image=Image.open("images/show_all.png"), size=(20, 20))
        self.image_excel = customtkinter.CTkImage(light_image=Image.open("images/excel.png"), dark_image=Image.open("images/excel.png"), size=(20, 20))

        # Поле для ввода номера плана
        self.plan_number_label = customtkinter.CTkLabel(self.filter_frame, text="Plan Nr:")
        self.plan_number_label.pack(side="left", padx=5, pady=5)

        self.plan_number_entry = customtkinter.CTkEntry(self.filter_frame, placeholder_text="Suchen:", width=250, height=28, corner_radius=3)
        self.plan_number_entry.pack(side="left", padx=5, pady=5)

        # Кнопка применить фильтр
        self.apply_button = customtkinter.CTkButton(self.filter_frame, image=self.image_search, text="", corner_radius=2, height=28, width=50,
                                                    fg_color=("#2d2e2e"), text_color=("gray90"),
                                                    hover_color=("red"), anchor="center", command=self.apply_filter)
        self.apply_button.pack(side="left", padx=5, pady=5)

        # Кнопка показать весь список
        self.show_all_button = customtkinter.CTkButton(self.filter_frame, image=self.image_show_all, text="", corner_radius=2, height=28, width=50,
                                                       fg_color=("#2d2e2e"), text_color=("gray90"),
                                                       hover_color=("red"), anchor="center", command=self.load_data)
        self.show_all_button.pack(side="left", padx=5, pady=5)

        self.excel_btn = customtkinter.CTkButton(self.second_button_frame, image=self.image_excel, text="", corner_radius=2, height=28, width=50,
                                                    fg_color=("#2d2e2e"), text_color=("gray90"),
                                                    hover_color=("red"), anchor="center", command=self.open_excel_file)
        self.excel_btn.pack(side="left", padx=5, pady=5)



        self.plan_number_entry.bind('<Return>', lambda event=None: self.apply_filter())
        self.bind("<Escape>", self.show_all)

    def open_excel_file(self):
        product_kostenstelle = self.kostenstelle
        parts = product_kostenstelle.split("-")

        # Проверяем, есть ли в тексте после знака "-" значение "24"
        if len(parts) > 1 and "24" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        elif len(parts) > 1 and "23" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2023\02 Verkehrssicherung"
        elif len(parts) > 1 and "22" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2022\02 Verkehrssicherung"
        elif len(parts) > 1 and "21" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2021\02 Verkehrssicherung"
        elif len(parts) > 1 and "20" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2020\02 Verkehrssicherung"
        elif len(parts) > 1 and "25" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2025\02 Verkehrssicherung"
        elif len(parts) > 1 and "26" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2026\02 Verkehrssicherung"
        elif len(parts) > 1 and "27" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2027\02 Verkehrssicherung"
        elif len(parts) > 1 and "28" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2028\02 Verkehrssicherung"
        else:
            # По умолчанию
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        prefix_to_match = "11"
        items = os.listdir(os.path.normpath(base_path))
        matching_folders = [folder for folder in items if product_kostenstelle.lower() in folder.lower()]
        if matching_folders:
            target_folder = os.path.join(base_path, matching_folders[0])
            # Ищем подпапку внутри найденной папки, начинающуюся с префикса "11"
            nested_folder_match = [nested_folder for nested_folder in os.listdir(target_folder) if nested_folder.startswith(prefix_to_match)]
            
            if nested_folder_match:
                nested_folder = nested_folder_match[0]
                document_path = os.path.join(target_folder, nested_folder, "Materialliste.xlsx")
                # self.check_connection()
                # cursor = self.conn.cursor()
                # cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status FROM bau WHERE kostenstelle_vvo = %s",(product_kostenstelle, ))
                # data = cursor.fetchone()
                # data_table1 = [
                #     ["", data[2], "", "", f"{data[6]} - {data[7]}"],
                #     ["", "", "", "", ""],
                #     ["", data[3], "","",f"{data[6]} - {data[7]}"],
                #     ["", f"{data[5]}, {data[4]}","","", data[8]],
                # ]

                # # Вставляем данные в файл Excel
                # insert_data_into_tables(document_path,document_path, data_table1)

                # # Открываем файл
                os.startfile(document_path)
            else:
                print(f"No folders matching the keyword '{product_kostenstelle}' found.")

    def load_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT plan_number, vz_nr, größe, quantity FROM test2 WHERE kostenstelle = %s", (self.kostenstelle,))
        results = cursor.fetchall()

        # Подсчет суммарного количества по Plan Number и Größe
        self.data_dict = {}  # сохраняем данные в self.data_dict для дальнейшей сортировки
        special_vz_nr = {"3001", "3002", "3003", "3004", "3005", "3006", "3007", "3008", "3009", "3010"}
        for row in results:
            plan_number, vzp_nr, größe, quantity = row
            quantity = int(quantity)  # Убедимся, что quantity интерпретируется как число
            if vzp_nr in special_vz_nr:
                größe = f"Sonderschild({größe})"
            key = (plan_number, größe)
            if key in self.data_dict:
                self.data_dict[key]['Anzahl'] += quantity
            else:
                self.data_dict[key] = {'VZP.Nr.': vzp_nr, 'Plan Nr.': plan_number, 'Anzahl': quantity}

        # Очистка таблицы перед вставкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Сортировка данных по Plan Nr.
        sorted_data = sorted(self.data_dict.items(), key=lambda x: x[0][0])

        # Debug: выводим данные перед вставкой в таблицу
        print("Data to be inserted into the table:", sorted_data)

        # Вставка данных в таблицу
        for key, data in sorted_data:
            self.table.insert("", "end", values=(data['Plan Nr.'], key[1], data['Anzahl']))

    def apply_filter(self):
        plan_number = self.plan_number_entry.get()
        cursor = self.conn.cursor()
        cursor.execute("SELECT plan_number, vz_nr, größe, quantity FROM test2 WHERE kostenstelle = %s AND plan_number = %s", (self.kostenstelle, plan_number))
        results = cursor.fetchall()

        # Подсчет суммарного количества по Plan Number и Größe
        self.data_dict = {}  # сохраняем данные в self.data_dict для дальнейшей сортировки
        special_vz_nr = {"3001", "3002", "3003", "3004", "3005", "3006", "3007", "3008", "3009", "3010"}
        for row in results:
            plan_number, vzp_nr, größe, quantity = row
            quantity = int(quantity)  # Убедимся, что quantity интерпретируется как число
            if vzp_nr in special_vz_nr:
                größe = f"Sonderschild({größe})"
            key = (plan_number, größe)
            if key in self.data_dict:
                self.data_dict[key]['Anzahl'] += quantity
            else:
                self.data_dict[key] = {'VZP.Nr.': vzp_nr, 'Plan Nr.': plan_number, 'Anzahl': quantity}

        # Очистка таблицы перед вставкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Сортировка данных по Plan Nr.
        sorted_data = sorted(self.data_dict.items(), key=lambda x: x[0][0])

        # Debug: выводим данные перед вставкой в таблицу
        print("Filtered data to be inserted into the table:", sorted_data)

        # Вставка данных в таблицу
        for key, data in sorted_data:
            self.table.insert("", "end", values=(data['Plan Nr.'], key[1], data['Anzahl']))

    def sort_by_plan_number(self):
        # Сортируем данные в зависимости от текущего порядка
        sorted_data = sorted(self.data_dict.items(), key=lambda x: x[0][0], reverse=not self.sort_ascending)
        self.sort_ascending = not self.sort_ascending  # Переключаем порядок сортировки

        # Очистка таблицы перед вставкой новых данных
        for row in self.table.get_children():
            self.table.delete(row)

        # Вставка данных в таблицу
        for key, data in sorted_data:
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
