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
        self.geometry(f"{1280}x{720}")
        self.iconbitmap(default=r"vvo.ico")
        self.title("Bestand Lager")
        self.resizable(False, False)  # Запрещаем изменение размера окна
        
        table_style = ttk.Style()
        
        table_style.configure("Treeview.Heading", font=("Arial", 14), background="black")  # Для заголовков столбцов
        table_style.configure("Treeview", font=("Arial", 14), foreground="white")  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
    
        

        self.f1 = customtkinter.CTkFrame(self,width=413,fg_color="transparent")
        self.f1.grid( row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f2 = customtkinter.CTkFrame(self, width=413,fg_color="transparent", border_width=2)
        self.f2.grid( row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f3 = customtkinter.CTkFrame(self, width=400,fg_color="transparent")
        self.f3.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f4 = customtkinter.CTkFrame(self,width=413,fg_color="transparent")
        self.f4.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f5 = customtkinter.CTkFrame(self,width=413,fg_color="transparent")
        self.f5.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f6 = customtkinter.CTkFrame(self, width=400,fg_color="transparent")
        self.f6.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

       
        
        image_path = f"vvo_label.png" 
        image = PIL.Image.open(image_path)
        ctk_image = CTk.CTkImage(image, size=(90, 125))
        self.image_label_logo = CTk.CTkLabel(self, image=ctk_image, text="")
        self.image_label_logo.grid(sticky="nw")

        self.bar_code = customtkinter.CTkEntry(self.f1, placeholder_text="Bar Code:", width=320)
        self.bar_code.grid(column= 0, row=0, padx=(40, 0), pady=(20, 10), sticky="nsew",)

        self.vz_nr = customtkinter.CTkEntry(self.f1, placeholder_text="Vz Nr.:", width=320)
        self.vz_nr.grid(column= 0, row=1, padx=(40, 0), pady=(0, 20), sticky="nsew",)


        self.plus = customtkinter.CTkButton(master=self.f1, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Количество', command=self.kol2)
        self.plus.grid(column = 0,row=2, padx=(40,0), pady=(20, 0), sticky="nsew")


        self.koll = customtkinter.CTkButton(master=self.f1, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Добавить', command=self.open_dialog_plus)
        self.koll.grid(column = 0,row=3, padx=(40,0), pady=(10, 0), sticky="nsew")


        self.minus = customtkinter.CTkButton(master=self.f1, fg_color="transparent",  border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Убрать', command=self.open_dialog_minus)
        self.minus.grid(column = 0,row=4, padx=(40,0), pady=(10, 0), sticky="nsew")


        self.zamena = customtkinter.CTkButton(master=self.f1, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='заменить', command=self.open_dialog_zamena)
        self.zamena.grid(column = 0,row=5, padx=(40,0), pady=(10, 0), sticky="nsew")

        self.bau = customtkinter.CTkButton(master=self.f1, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Отправить на стройку', command=self.bau2)
        self.bau.grid(column = 0,row=6, padx=(40,0), pady=(10, 0), sticky="nsew")

        self.show_all = customtkinter.CTkButton(master=self.f1, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='вывести всю таблицу', command=self.show_all_data)
        self.show_all.grid(column = 0,row=7, padx=(40,0), pady=(10, 20), sticky="nsew")
        
        self.exit = customtkinter.CTkButton(master=self.f6, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Выход', command=self.exit)
        self.exit.grid(pady=(20,20), sticky="sw")
       
           
        
############################################################################################################################################        
############################################################################################################################################
        # Создаем таблицу
        
        self.table = ttk.Treeview(self.f2, columns=("", "Bar Code", "VZ Nr.", "Bedeutung", "Größe","Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.table.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        self.table.column("#0", width=0)  # Устанавливаем ширину столбца "Bar Code" в 0 пикселей
        self.table.column("#1", width=120)
        self.table.column("#2", width=100)
        self.table.column("#3", width=300)
        self.table.column("#4", width=70)
        self.table.column("#5", width=70)
        self.table.column("#6", width=150)
        self.table.column("#7", width=0)
        
        # Добавляем заголовки столбцов
        self.table.heading("#0", text="")
        self.table.heading("#1", text="Bar Code")
        self.table.heading("#2", text="VZ Nr.")
        self.table.heading("#3", text="Bedeutung")
        self.table.heading("#4", text="Größe")
        self.table.heading("#5", text="Lager")
        self.table.heading("#6", text="Aktueller")

 ############################################################################################################################################      
 ############################################################################################################################################

        

        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        
     

        # self.login = login
        self.barcode = None
        self.error_label= None
        
        self.show_all_data()

        
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

                self.image_label = CTk.CTkLabel(self.f3, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}
        

        

    def kol2(self):
        self.barcode = self.bar_code.get()
        self.vz = self.vz_nr.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        # Получаем данные из базы данных (замените на ваш SQL-запрос)
        data = cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = ? OR VZ_Nr = ?", (self.barcode, self.vz)).fetchall()
        # Очищаем текущие строки в таблице
        if self.bar_code == "":
            self.result_show("Забыл ввести")
        for row in self.table.get_children():
            self.table.delete(row)

        if data:
            for item in data:
                # Добавляем новые строки с данными в таблицу
                self.show_img_for_barcode(self.bar_code.get())
                self.show_img_for_vz(self.vz_nr.get())
                self.table.insert("", "end", values=item)
        else:
            self.result_show("Данных не найдено")
        
        cursor.close()
        conn.close()


    def check_vz_nr(self, event):
        # Функция вызывается при изменении баркода
        if self.bar_code.get():
            # Если баркод не пустой, очищаем поле Vz Nr
            self.vz_nr.delete(0, 'end')
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())

    def check_barcode(self, event):
        # Функция вызывается при изменении Vz Nr
        if self.vz_nr.get():
            # Если Vz Nr не пустой, очищаем поле баркода
            self.bar_code.delete(0, 'end')
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
        
        
    def bau(self):
        self.barcode = self.bar_code.get()
        self.vz = self.vz_nr.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = ? OR VZ_Nr = ?", (self.barcode,self.vz)).fetchone()
        
        if  self.vz == "" and self.barcode or self.barcode == "" and self.vz:
            new_window = dialog.TableListWindow()
            new_window.mainloop()
       
        else:
            self.result_show("выберите товар")
            print(f"Сработало {self.vz} {self.barcode}")
        cursor.close()  
        conn.close()
    
    def bau2(self):
        selected_items = self.table.selection()
        if selected_items:
            selected_item = selected_items[0]
            barcode = self.table.item(selected_item, "values")[0]  # Получаем значение Bar Code из выбранной строки
            print("выбранный баркод: ", barcode)
        if barcode is not None:
            new_window = dialog.TableListWindow()
            new_window.mainloop()
        


    def show_all_data(self):
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        
        # Получаем все записи из таблицы "Lager_Bestand"
        data = cursor.execute("SELECT * FROM Lager_Bestand").fetchall()

        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)
            self.image_label.destroy()

        # Вставляем данные в таблицу
        for item in data:
            self.table.insert("", "end", values=item)

        cursor.close()
        conn.close()    

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

                self.image_label = CTk.CTkLabel(self.f3, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
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

                self.image_label = CTk.CTkLabel(self.f3, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}")
        
        cursor.close()
        conn.close()   

    def open_dialog_plus(self):
        self.barcode = self.bar_code.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
        
        if data is not None:
            dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
            num = dialog.get_input()
            Kol = data[3]
            num = int(num) + int(Kol)
            cursor.execute("UPDATE Lager_Bestand SET Aktueller_bestand = ? WHERE Bar_Code = ?", (num, self.barcode))
            conn.commit()

            barcode_text = f"Bar Code: {data[0]}"
            vznr_text = f"VZ Nr: {data[1]}"
            bedeutung_text = f"Bedeutung: {data[2]}"
            Kol = f"Aktueller bestand: {num}"
        
            # Объединяем текст с значениями
            result_text = f"{barcode_text}\n{vznr_text}\n{bedeutung_text}\n{Kol}"
        
            self.result_show(result_text)
            print(num)
        else:
            self.result_show("Данного Bar Code не существует")
            if hasattr(self, "image_label"):
                self.image_label.destroy()

    def open_dialog_minus(self): # Кнопка вычитания с открытием диалогового окна
        self.barcode = self.bar_code.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
        
        if data is not None:
            dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
            num = dialog.get_input()
            Kol = data[3]
            num = int(Kol) - int(num)
            data = cursor.execute("UPDATE Lager_Bestand SET Aktueller_bestand = ? WHERE Bar_Code = ?", (num, self.barcode))
            conn.commit()

            data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
            barcode_text = f"Bar Code: {data[0]}"
            vznr_text = f"VZ Nr: {data[1]}"
            bedeutung_text = f"Bedeutung: {data[2]}"
            Kol = f"Aktueller_bestand: {num}"
        
            # Объединяем текст с значениями
            result_text = f"{barcode_text}\n{vznr_text}\n{bedeutung_text}\n{Kol}"
        
            self.result_show(result_text)
            print(num)
        else:
            self.result_show("Данного Bar Code не существует")
            if hasattr(self, "image_label"):
                self.image_label.destroy()

    

    def open_dialog_zamena(self):
        self.barcode = self.bar_code.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
        if data is not None:
            dialog = customtkinter.CTkInputDialog(text="Введиите количество для замены:", title="Заменить")
            dialog.iconbitmap(default=r"vvo.ico")
            num = dialog.get_input()
            data = cursor.execute("UPDATE Lager_Bestand SET Aktueller_bestand = ? WHERE Bar_Code = ?", (num, self.barcode))
            conn.commit()
            data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
            barcode_text = f"Bar Code: {data[0]}"
            vznr_text = f"VZ Nr: {data[1]}"
            bedeutung_text = f"Bedeutung: {data[2]}"
            Kol = f"Aktueller_bestand: {num}"
        
            # Объединяем текст с значениями
            result_text = f"{barcode_text}\n{vznr_text}\n{bedeutung_text}\n{Kol}"
        
            self.result_show(result_text)
            print(num)
        else:
            self.result_show("Данного Bar Code не существует")
            if hasattr(self, "image_label"):
                self.image_label.destroy()
        print("Zamenna")
 
    def result_show(self, message):
            
            if self.error_label:
                self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было
            if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
            self.error_label = CTk.CTkLabel(self.f3, font=('<Arial>', 20)  , bg_color="transparent", text=message, text_color="gray")
            self.error_label.grid( row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def exit (self):
        self.destroy()  # Сворачиваем окно
        new_window = Autorisation.App()
        new_window.mainloop()  # Запускаем главный цикл нового окна




if __name__ == '__main__':
    app = BestandLager()
    app.mainloop()