import customtkinter
import customtkinter as CTk
from tkinter import *
import main
import PIL.Image
import localizations
import psycopg2
import regbase
import socket
import time
import os
import requests
import tkinter.messagebox
import multiprocessing
import subprocess
import threading

customtkinter.set_appearance_mode("dark")





class App(CTk.CTk): # Окно авторизации
    def __init__(self):
        super().__init__()
        self.iconbitmap(default=r"vvo.ico")
        self.geometry('1280x720+300+180')
        self.title('VVO')
        self.resizable(False, False)
        self.language = self.load_language_from_file()
        self.conn = regbase.create_conn()
        self.image_frame= customtkinter.CTkFrame(self, height=20, width= 1280, fg_color="transparent")
        self.image_frame.pack(side = "top")
        image_path = f"vvo_label.png" 
        image = PIL.Image.open(image_path)
        ctk_image = CTk.CTkImage(image, size=(90, 125))
        self.image_label = CTk.CTkLabel(self.image_frame, image=ctk_image, text="")
        self.image_label.grid(padx = (1170,0),pady = 10)

        self.entrylogin = CTk.CTkEntry(self, placeholder_text="Login:", corner_radius = 3, width= 200)
        self.entrylogin.pack(pady=(110,10)) # Поле для ввода логина
        
        self.entrypass = customtkinter.CTkEntry(self, placeholder_text="Password:", show="*", corner_radius = 3, width= 200)
        self.entrypass.pack(pady=(0,10)) # Поле для ввода пароля
        login, password = self.load_saved_login_and_password()
        if login:
            self.entrylogin.insert('0', login)
        if password:
            self.entrypass.insert('0',password)
        self.main_button_1 = customtkinter.CTkButton(master=self, corner_radius=2, height=30, width= 200, 
                                                fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
                                                font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center", text='Log in', command=self.getpass)
        self.main_button_1.pack(pady=(0,10))
        self.main_button_1.configure(text=self.get_button_text_for_language(self.language))
        
        self.remember_me = customtkinter.CTkCheckBox(self, text="Remember me", border_width = 2, hover_color = "red", fg_color = "red", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.remember_me.pack(pady=(0,10))

        self.language_menu = customtkinter.CTkOptionMenu(self, values=["Russian","English","Deutsch"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.update_ui_language)
        self.language_menu.pack(pady=(0,10))
        self.saved_language = self.load_language_from_file()
        self.language_menu.set(self.saved_language)
        
        self.statusbar_connection= customtkinter.CTkFrame(self, height=20, width= 1280, corner_radius= 1)
        self.statusbar_connection.pack(side = "bottom")
        

        self.entrypass.bind('<Return>', lambda event=None: self.getpass()) # При нажатии на кнопку энетер нажимается кнопка Войти
        
        
        

        self.after(1000, lambda: self.entrylogin.focus_set())
        self.update()

        self.login = None  # Создаем атрибут для хранения логина
        self.password = None  # Создаем атрибут для хранения пароля
        self.error_label = None # Создаем атрибут для хранения вывода текста
        self.status_label = None
        
        
        self.after(100, self.updata_action)
        self.check_update()
        
    def check_update(self):
        # proxies = {
        # 'http': 'http://d.dobin:dd1710dd@192.168.2.254:3128',
        # 'https': 'http://d.dobin:d1710dd@192.168.2.254:3128',
        # }
        github_api_url = 'https://api.github.com/repos/Rocketsops96/Bestand_Lager/releases/latest'
        # Загрузите информацию о последнем релизе с GitHub API
        response = requests.get(github_api_url) #, proxies=proxies
        if response.status_code == 200:
            release_info = response.json()
            assets = release_info.get('assets', [])

            # Проверяем, есть ли какие-то ассеты (архивы) в релизе
            if assets:
                download_url = assets[0].get('browser_download_url', '')

                # Получите текущую версию
                current_version_path = 'version.txt'
                if os.path.exists(current_version_path):
                    with open(current_version_path, 'r') as current_version_file:
                        current_version = current_version_file.read().strip()
                        self.latest_current_version = current_version
                        if current_version != release_info['tag_name']:
                            confirmation = tkinter.messagebox.askyesno("Подтверждение", f"Вы уверены что хотите обновить?")
                         
                            if confirmation:
                                    threading.Thread(target=self.start_update_process).start()
                            else:
                                print("no")
                else:
                    current_version = 'v0.0.0.0'
        

    def start_update_process(self):
        
        subprocess.Popen(["cmd", "/c", "start", "update.bat"])
        exit = App()
        exit.destroy()
        

    def updata_action(self):
        if self.status_label is not None:
                self.status_label.destroy()
        try:
            socket.create_connection(("www.google.com", 80), timeout=10)
            if not self.conn:
                # Если соединение с базой данных отсутствует, пробуем его восстановить
                self.conn = regbase.create_conn()
                print("Database connection re-established")
            self.connected_status_label(f"  Connected {self.latest_current_version}")
            print("connected")
        except (socket.timeout, socket.error):
            self.connected_status_label("Connection error")
            print("Nihuya")
            if self.conn:
                # Если есть соединение с базой данных, закрываем его
                self.conn.close()
                self.conn = None
                print("Database connection closed")
        self.after(1000, self.updata_action)


    def get_button_text_for_language(self, language):
        texts = localizations.language_texts.get(language, {})
        return texts.get("Log in", "Log in")

    def getpass(self):
        self.login = self.entrylogin.get()
        self.password = self.entrypass.get()
        if not self.login or not self.password:
            self.display_error("You did not enter your username \n or password")
            return  # Завершаем функцию, если поля пустые

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE login = %s AND password = %s" , (self.login, self.password))
        data = cursor.fetchone()
        if data is not None and len(data) >= 2:
            self.role = str(data[2])
            if self.remember_me.get():  # Проверка, отмечен ли флажок "Запомнить меня"
                self.save_login_and_password(self.login, self.password)
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
            new_window = main.BestandLager(self.login,self.role, self.conn)
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
        self.error_label.pack(pady=(0, 10)) # положение вывода лейбла
    
    def connected_status_label(self, message):
            self.status_label = customtkinter.CTkLabel(self.statusbar_connection, text=message, text_color="gray", height= 20)
            self.status_label.grid(sticky = 'nsew', padx = (0,1280))
            
        
    def save_language_to_file(self, language):
        with open("language.txt", "w") as file:
            file.write(language)

    def load_language_from_file(self):
        try:
            with open("language.txt", "r") as file:
                return file.read()
        except FileNotFoundError:
            # Если файл не найден, вернуть значение по умолчанию (например, "English")
            return "English"
    
    def save_login_and_password(self, login, password):
        with open("login_password.txt", "w") as file:
            file.write(f"{login}\n{password}")

    def load_saved_login_and_password(self):
        try:
            with open("login_password.txt", "r") as file:
                login = file.readline().strip()
                password = file.readline().strip()
                return login, password
        except FileNotFoundError:
            return None, None

def run_update_process():
    exe_path = r'update.exe'
    subprocess.run(exe_path, shell=True, check=True)

if __name__ == '__main__':
    app = App()
    
    app.mainloop()
    

