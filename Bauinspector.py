import customtkinter
import customtkinter as CTk
import sqlite3
from PIL import Image, ImageTk 
from tkinter import *
from tkinter import ttk
import Autorisation
import PIL.Image
import dialog
import CTkTable

customtkinter.set_appearance_mode("dark")

class Bauinspector(CTk.CTk):
    def __init__(self): 
        super().__init__()
        self.iconbitmap(default=r"vvo.ico")
        self.geometry("1280x720+300+300")
        self.title("Bestand Lager")
        self.resizable(False, False)

        table_style = ttk.Style()
        
        table_style.configure("Treeview.Heading", font=("Arial", 14), background="black")  # Для заголовков столбцов
        table_style.configure("Treeview", font=("Arial", 14), foreground="white")  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
    
        

        self.f1 = customtkinter.CTkFrame(self,width=413, fg_color="transparent")
        self.f1.grid( row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f2 = customtkinter.CTkFrame(self, width=413, fg_color="transparent", border_width=2)
        self.f2.grid( row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f3 = customtkinter.CTkFrame(self, width=413, fg_color="transparent")
        self.f3.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f4 = customtkinter.CTkFrame(self,width=413, fg_color="transparent")
        self.f4.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f5 = customtkinter.CTkFrame(self,width=413, fg_color="transparent")
        self.f5.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f6 = customtkinter.CTkFrame(self, width=413, fg_color="transparent")
        self.f6.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f7 = customtkinter.CTkFrame(self, width=413, fg_color="transparent")
        self.f7.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f8 = customtkinter.CTkFrame(self, width=413, fg_color="transparent")
        self.f8.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.f9 = customtkinter.CTkFrame(self, width=413, fg_color="transparent")
        self.f9.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")


############################################################################################################################################        
############################################################################################################################################
        # Создаем таблицу
        
        self.table = ttk.Treeview(self.f1, columns=("", "Bar Code", "VZ Nr.", "Bedeutung", "Größe","Bestand Lager", "Aktueller bestand"), style="Treeview", height=26)
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

        self.show_all_data()


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



if __name__ == '__main__':
    app = Bauinspector()
    app.mainloop()