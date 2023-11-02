import customtkinter
import customtkinter as CTk
import sqlite3
from tkinter import *
import main
import PIL.Image
import localizations
import psycopg2
import regbase
customtkinter.set_appearance_mode("dark")





class App(CTk.CTk): # Окно авторизации
    def __init__(self):
        super().__init__()
        self.iconbitmap(default=r"vvo.ico")
        self.geometry('1280x720+300+300')
        self.title('Bestand Lager')
        self.resizable(False, False)
        self.language = self.load_language_from_file()

        self.entrylogin = CTk.CTkEntry(self, placeholder_text="Login:", corner_radius = 3)
        self.entrylogin.grid(row=3, column=1, columnspan=2, padx=(550, 0), pady=(100, 20), sticky="nsew") # Поле для ввода логина
        
        self.entrypass = customtkinter.CTkEntry(self, placeholder_text="Password:", show="*", corner_radius = 3)
        self.entrypass.grid(row=5, column=1, columnspan=2, padx=(550, 0), pady=(00, 20), sticky="nsew") # Поле для ввода пароля

        self.main_button_1 = customtkinter.CTkButton(master=self, corner_radius=2, height=30, width= 200, 
                                                fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
                                                font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center", text='Log in', command=self.getpass)
        self.main_button_1.grid(row=6, column=1, padx=(550, 0), pady=(00, 20), sticky="nsew")
        self.main_button_1.configure(text=self.get_button_text_for_language(self.language))
        

        self.language_menu = customtkinter.CTkOptionMenu(self, values=["Russian","English","Deutsch"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.update_ui_language)
        self.language_menu.grid(row=7, column=1, padx=(550, 0), pady=(00, 20), sticky= "s")
        self.saved_language = self.load_language_from_file()
        self.language_menu.set(self.saved_language)


        self.entrypass.bind('<Return>', lambda event=None: self.getpass()) # При нажатии на кнопку энетер нажимается кнопка Войти
        
        
        image_path = f"vvo_label.png" 
        image = PIL.Image.open(image_path)
        ctk_image = CTk.CTkImage(image, size=(90, 125))
        self.image_label = CTk.CTkLabel(self, image=ctk_image, text="")
        self.image_label.grid(row=0, column=3, padx=(425, 0), pady=(10, 0), sticky="nsew")


        self.after(100, lambda: self.entrylogin.focus_set())
        self.update()

        self.login = None  # Создаем атрибут для хранения логина
        self.password = None  # Создаем атрибут для хранения пароля
        self.error_label = None # Создаем атрибут для хранения вывода текста
        
    def get_button_text_for_language(self, language):
        texts = localizations.language_texts.get(language, {})
        return texts.get("Log in", "Log in")

    def getpass(self):
        self.login = self.entrylogin.get()
        self.password = self.entrypass.get()
        if not self.login or not self.password:
            self.display_error("You did not enter your username \n or password")
            return  # Завершаем функцию, если поля пустые

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = %s AND password = %s" , (self.login, self.password))
        data = cursor.fetchone()
        if data is not None and len(data) >= 2:
            self.role = str(data[2])
        else:
            # Обработка случая, когда data равен None или длина меньше 4
            # Может быть, вы хотите установить значение по умолчанию или выдать ошибку.
            # Пример:
            self.role = "Default Role"
        
        print(self.role)
        if data is not None:
            self.display_error("Есть такая учетная запись")
            #self.withdraw()  # Сворачиваем окно
            self.destroy()
            new_window = main.BestandLager(self.login,self.role, conn)
            new_window.mainloop()  # Запускаем главный цикл нового окна
            
        else:
            self.display_error("Wrong login or password")
            print(self.login, self.password)
            
     
   
    def update_ui_language(self, language):      
        # Получите словарь с текстами для выбранного языка
        texts = localizations.language_texts.get(language, {})
        
        # Обновите тексты для виджетов, кнопок, лейблов и других элементов
        self.main_button_1.configure(text=texts.get("Log in", "Log in"))
       

        selected_language = language
        self.save_language_to_file(selected_language)


    def display_error(self, message):
        if self.error_label:
            self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было
        
        self.error_label = CTk.CTkLabel(self, text=message, text_color="gray") # создаем лейбл
        self.error_label.grid(row=8, column=1, columnspan= 2, padx=(550, 0), pady=(0, 20), sticky="nsew") # положение вывода лейбла
     
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
    
    app = App()
    conn = regbase.create_conn()
    app.mainloop()
    

