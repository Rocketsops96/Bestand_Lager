import customtkinter
import customtkinter as CTk
import sqlite3
from PIL import Image, ImageOps
from tkinter import *
from tkinter import ttk
import Autorisation
import PIL.Image
import dialog
import CTkTable

customtkinter.set_appearance_mode("dark")

class BestandLager(CTk.CTk):
    def __init__(self): # После теста добавить аргумент login и не забыть убрать комментарий ниже!!!!
        super().__init__()

        # Установите геометрию окна
        self.geometry("1280x720")
        self.iconbitmap(default=r"vvo.ico")
        self.title("Bestand Lager")
        self.resizable(True, True)  # Запрещаем или разрешаем изменение размера окна

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

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")


        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["60%","70%","80%", "90%", "100%", "110%", "120%"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky= "s")
        self.scaling_optionemenu.set("100%")


        #Создаем фреймы для каждого окна
        self.f1 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f1.grid_columnconfigure(0, weight=1)

        self.f2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f2.grid_columnconfigure(0, weight=1)

        self.f3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f3.grid_columnconfigure(0, weight=1)

        #Создаем дефолтный фрейм
        self.select_frame_by_name("home")



############## ############## ############## ############## #Настройка фрейма №1 ############## ############## ############## ############## ############## 
        
        table_style = ttk.Style()
        table_style.configure("Treeview.Heading", font=("Arial", 14), background="black")  # Для заголовков столбцов
        table_style.configure("Treeview", font=("Arial", 14), foreground="white")  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
        self.table = ttk.Treeview(self.f1, columns=("","Bar Code", "VZ Nr.", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.table.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
       
        
        
        self.table.column("#0", width=0)
        self.table.column("#1", width=120)
        self.table.column("#2", width=100)
        self.table.column("#3", width=700)
        self.table.column("#4", width=100)
        self.table.column("#5", width=70)
        self.table.column("#6", width=150)
        
        # Добавляем заголовки столбцов
        
        self.table.heading("#1", text="Bar Code")
        self.table.heading("#2", text="VZ Nr.")
        self.table.heading("#3", text="Bedeutung")
        self.table.heading("#4", text="Größe")
        self.table.heading("#5", text="Lager")
        self.table.heading("#6", text="Aktueller")


        self.home_frame1 = customtkinter.CTkFrame(self.f1)#self.f3.grid_columnconfigure(0, weight=1)
        self.home_frame1.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame1.grid_columnconfigure(0, weight=1)
        self.home_frame2 = customtkinter.CTkFrame(self.f1)
        self.home_frame2.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame2.grid_columnconfigure(0, weight=1)
        

        self.bar_code = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Bar Code:", width= 250)
        self.bar_code.grid(column= 0, row=0, padx=(10, 10), pady=(10, 10), sticky="nw",)
        

        self.vz_nr = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Vz Nr.:", width= 250)
        self.vz_nr.grid(column= 0, row=1, padx=(10, 10), pady=(0, 10), sticky="nw",)

        self.plus = customtkinter.CTkButton(master=self.home_frame1, corner_radius=5, height=40, width=250, border_spacing=10, text="Suchen",
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.kol2)
        self.plus.grid(column = 0,row=2, padx=(10,10), pady=(0, 10), sticky="nw")

        self.show_all = customtkinter.CTkButton(master=self.home_frame1, corner_radius=5, height=40, width=250, border_spacing=10, text="Show all",
                                                   fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.show_all_data)
        self.show_all.grid(column = 0,row=3, padx=(10,0), pady=(0, 10), sticky="nw")

############## ############## ############## ############## #Настройка фрейма №2 ############## ############## ############## ############## ##############        
        


############## ############## ############## ############## #Настройка фрейма №3 ############## ############## ############## ############## ############## 
        




        
        #Показываем всю таблицу 

        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
        self.after(100, lambda: self.bar_code.focus_set())
        self.update()


        #self.login = login
        self.barcode = None
        self.error_label= None
        


        self.show_all_data()

    

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


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
        self.bar_code.delete(0, 'end')
        self.vz_nr.delete(0, 'end')
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
                self.image_label.grid(row=1, column=1, padx=(0, 0), pady=(0, 0), sticky="nsew")
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
   

if __name__ == '__main__':
    app = BestandLager()
    app.mainloop()