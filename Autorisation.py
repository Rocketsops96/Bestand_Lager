import customtkinter
import customtkinter as CTk
import sqlite3
# from PIL import Image, ImageTk
from tkinter import *
import main
import PIL.Image

customtkinter.set_appearance_mode("dark")





class App(CTk.CTk): # Окно авторизации
    def __init__(self):
        super().__init__()
        self.iconbitmap(default=r"vvo.ico")
        self.geometry('1280x720+300+300')
        self.title('Bestand Lager')
        self.resizable(False, False)
        

        self.entrylogin = CTk.CTkEntry(self, placeholder_text="Логин:")
        self.entrylogin.grid(row=3, column=1, columnspan=2, padx=(550, 0), pady=(100, 20), sticky="nsew") # Поле для ввода логина
        
        self.entrypass = customtkinter.CTkEntry(self, placeholder_text="Пароль:", show="*")
        self.entrypass.grid(row=5, column=1, columnspan=2, padx=(550, 0), pady=(00, 20), sticky="nsew") # Поле для ввода пароля

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Войти', command=self.getpass)
        self.main_button_1.grid(row=6, column=1, padx=(570, 20), pady=(00, 20), sticky="nsew")\
        
        self.entrypass.bind('<Return>', lambda event=None: self.getpass()) # При нажатии на кнопку энетер нажимается кнопка Войти
        
        
        image_path = f"vvo_label.png" 
        image = PIL.Image.open(image_path)
        ctk_image = CTk.CTkImage(image, size=(90, 125))
        self.image_label = CTk.CTkLabel(self, image=ctk_image, text="")
        self.image_label.grid(row=0, column=3, padx=(450, 0), pady=(10, 0), sticky="nsew")


        self.after(100, lambda: self.entrylogin.focus_set())
        self.update()

        self.login = None  # Создаем атрибут для хранения логина
        self.password = None  # Создаем атрибут для хранения пароля
        self.error_label = None # Создаем атрибут для хранения вывода текста
        
    

    def getpass(self):
        self.login = self.entrylogin.get()
        self.password = self.entrypass.get()
        if not self.login or not self.password:
            self.display_error("введите логин и пароль")
            return  # Завершаем функцию, если поля пустые

        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT login, password FROM users WHERE login = ? AND password = ?", (self.login, self.password)).fetchone()

        
        if data is not None:
            self.display_error("есть такая учетная запись")
            #self.withdraw()  # Сворачиваем окно
            self.destroy()
            new_window = main.BestandLager(self.login)
            new_window.mainloop()  # Запускаем главный цикл нового окна
            
        else:
            self.display_error("Неверный пароль")
            print(self.login, self.password)
            
        
        conn.close()



    def display_error(self, message):
        if self.error_label:
            self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было

        self.error_label = CTk.CTkLabel(self, text=message, text_color="gray") # создаем лейбл
        self.error_label.grid(row=8, column=1, padx=(550, 0), pady=(0, 20), sticky="nsew") # положение вывода лейбла




if __name__ == '__main__':
    app = App()
    app.mainloop()
    

