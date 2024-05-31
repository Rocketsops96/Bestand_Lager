import customtkinter
from tkinter import messagebox
from PIL import Image



class Privacy(customtkinter.CTkToplevel):

    APP_NAME = "Administrationsmenü"
    WIDTH = 800
    HEIGHT = 500
    
    def __init__(self, parent, conn, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title(Privacy.APP_NAME)
        self.geometry(str(Privacy.WIDTH) + "x" + str(Privacy.HEIGHT))
        self.minsize(Privacy.WIDTH, Privacy.HEIGHT)
        self.resizable(False, True)
        self.conn = conn
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.image_delete = customtkinter.CTkImage(light_image=Image.open("images/delete.png"), dark_image=Image.open("images/delete.png"), size=(15, 15))
        self.main_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill='both', expand=True) 

  
        self.left_side = customtkinter.CTkFrame(self.main_frame)
        self.left_side.pack(side='left', padx=1, expand=True, fill='both')

        self.title_left_side = customtkinter.CTkFrame(self.left_side, fg_color="transparent")
        self.title_left_side.pack(side='top', padx=1, fill='x')

        self.login_main_frame = customtkinter.CTkFrame(self.left_side, fg_color="transparent")
        self.login_main_frame.pack(side='top', padx=1, fill='both')


        self.bedeutung = customtkinter.CTkFrame(self.left_side, corner_radius=0)
        self.bedeutung.pack(side='bottom', padx=1, fill='x')

        text_label = "*B - Bearbeiten – Weisen Sie einen Benutzer zu, der Tabellen bearbeiten kann \n*A - Administrator – kann Benutzern Rechte zuweisen und auch Benutzer im Programm erstellen."

        self.bedeutung_label = customtkinter.CTkLabel(self.bedeutung, text = text_label, font=customtkinter.CTkFont(size=10, weight="bold"), text_color=("white"), anchor="w", justify="left")
        self.bedeutung_label.pack(side='left', padx=1, fill='x')

        self.right_side = customtkinter.CTkFrame(self.main_frame)
        self.right_side.pack(side='right', padx=1, expand=True, fill='both')

        self.login_name = customtkinter.CTkLabel(self.title_left_side, text="Benutzer", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.login_name.pack(side="left", anchor='w', fill='x', padx = (30,0))

        

        self.admin_state_check = customtkinter.CTkLabel(self.title_left_side, text="A", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.admin_state_check.pack(side = "right", fill='x', padx = (0,10))

        self.bearbeitung = customtkinter.CTkLabel(self.title_left_side, text="B", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.bearbeitung.pack(side = "right", fill='x', padx = (0,20))
        
        # Создаем соединение с базой данных (замените 'example.db' на имя вашей базы данных)

        self.cursor = self.conn.cursor()
        # Получаем логины и статусы из базы данных (замените 'users' на имя вашей таблицы)
        self.cursor.execute('SELECT login, role, admin_status FROM users WHERE login != %s', ('admin',))
        self.user_statuses = {row[0]: (row[1], row[2]) for row in self.cursor.fetchall()}

        # Создаем лейбл и чекбоксы для каждого логина
        for login in self.user_statuses.keys():
            self.login_frame = customtkinter.CTkFrame(self.login_main_frame, corner_radius=0, fg_color="#343638")
            self.login_frame.pack(side='top', fill='both', pady=5, anchor='w')  # anchor='w' для прикрепления к левому краю
            delete_button = customtkinter.CTkButton( self.login_frame, image = self.image_delete, text='', command=lambda l=login: self.delete_user(l), width= 30, corner_radius=0, 
                                                fg_color=("#343638"),
                                                hover_color=("red"),
                                                anchor="center" )
            delete_button.pack(side='left')
            label = customtkinter.CTkLabel( self.login_frame, text=login, font=customtkinter.CTkFont(size=12, weight="bold"), text_color=("white"))
            label.pack(side='left', fill='x', padx=5)

            role_status, admin_status = self.user_statuses[login]

            
            admin_var = customtkinter.IntVar(value=admin_status)
            checkbox_admin_status = customtkinter.CTkCheckBox( self.login_frame, text='', variable=admin_var, command=lambda l=login, var=admin_var: self.on_admin_checkbox_click(l, var), width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red",)
            checkbox_admin_status.pack(side='right')

            role_var = customtkinter.IntVar(value=role_status)
            checkbox_role = customtkinter.CTkCheckBox( self.login_frame, text='', variable=role_var, command=lambda l=login, var=role_var: self.on_role_checkbox_click(l, var), width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red")
            checkbox_role.pack(side='right')




    # Добавляем элементы для ввода логина, пароля и чекбоксов в правый фрейм
        self.main_label = customtkinter.CTkLabel(self.right_side, text = "Neuer Benutzer", font=customtkinter.CTkFont(size=15, weight="bold"), text_color=("white"), justify="center")
        self.main_label.pack(pady=5)

        self.login_entry = customtkinter.CTkEntry(self.right_side, placeholder_text="Login",corner_radius = 3, width= 200)
        self.login_entry.pack(pady=5)

        self.password_entry = customtkinter.CTkEntry(self.right_side, placeholder_text="Passwort",corner_radius = 3, width= 200)
        self.password_entry.pack(pady=5)

        self.repaet_password = customtkinter.CTkEntry(self.right_side, placeholder_text="Passwort",corner_radius = 3, width= 200)
        self.repaet_password.pack(pady=5)


        self.role_var = customtkinter.IntVar()
        self.checkbox_role = customtkinter.CTkCheckBox(self.right_side, text='Bearbeiten', variable=self.role_var, width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red",)
        self.checkbox_role.pack(pady=5)

        self.admin_var = customtkinter.IntVar()
        self.checkbox_admin_status = customtkinter.CTkCheckBox(self.right_side, text='Administrator', variable=self.admin_var, width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red",)
        self.checkbox_admin_status.pack(pady=5)

        # Кнопка для создания нового пользователя
        self.create_user_button = customtkinter.CTkButton(self.right_side, text="Erstellen", command=self.create_user, corner_radius= 1, fg_color="#343638", hover_color="red", font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white") )
        self.create_user_button.pack(pady=10)
    

    def create_user(self):
        # Создание нового пользователя при нажатии на кнопку
        login = self.login_entry.get()
        password = self.password_entry.get()
        repaet_password = self.repaet_password.get()
        role_status = self.role_var.get()
        admin_status = self.admin_var.get()

        # Проверка наличия логина и пароля
        if login and password:
            if password == repaet_password:
                # Вставляем нового пользователя в базу данных
                self.cursor.execute('INSERT INTO users (login, password, role, admin_status) VALUES (%s, %s, %s, %s)', (login, password, role_status, admin_status))


                # Обновляем интерфейс, добавляя нового пользователя в левый фрейм
                self.login_frame = customtkinter.CTkFrame(self.login_main_frame, corner_radius= 0, fg_color="#343638")
                self.login_frame.pack(side='top', fill='both', pady=5, anchor='w')  # anchor='w' для прикрепления к левому краю
        
                delete_button = customtkinter.CTkButton( self.login_frame,image = self.image_delete, text='', command=lambda l=login: self.delete_user(l), width= 30, corner_radius=0, 
                                                fg_color=("#343638"),
                                                hover_color=("red"),
                                                anchor="center" )
                delete_button.pack(side='left')
                label = customtkinter.CTkLabel( self.login_frame, text=login, font=customtkinter.CTkFont(size=12, weight="bold"), text_color=("white"))
                label.pack(side='left', fill='x', padx=5)

                self.cursor.execute('SELECT login, role, admin_status FROM users WHERE login != %s', ('admin',))
                self.user_statuses = {row[0]: (row[1], row[2]) for row in self.cursor.fetchall()}
                role_status, admin_status = self.user_statuses[login]

                
                admin_var = customtkinter.IntVar(value=admin_status)
                checkbox_admin_status = customtkinter.CTkCheckBox( self.login_frame, text='', variable=admin_var, command=lambda l=login, var=admin_var: self.on_admin_checkbox_click(l, var), width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red",)
                checkbox_admin_status.pack(side='right')

                role_var = customtkinter.IntVar(value=role_status)
                checkbox_role = customtkinter.CTkCheckBox( self.login_frame, text='', variable=role_var, command=lambda l=login, var=role_var: self.on_role_checkbox_click(l, var), width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red")
                checkbox_role.pack(side='right')
            else:
                messagebox.showinfo("Fehler", "Die Passwörter stimmen nicht überein.")



    def delete_user(self, login):
        try:
            # Удаление пользователя из базы данных
            query = "DELETE FROM users WHERE login = %s"
            self.cursor.execute(query, (login,))
            print(f"Deleting user: {login}")

            # Удаление всех дочерних виджетов в login_main_frame
            for widget in self.login_main_frame.winfo_children():
                widget.destroy()

            # Обновление списка логинов
            self.cursor.execute('SELECT login, role, admin_status FROM users WHERE login != %s', ('admin',))
            user_statuses = {row[0]: (row[1], row[2]) for row in self.cursor.fetchall()}

            # Создание лейблов и чекбоксов на основе обновленного списка логинов
            for login in user_statuses.keys():
                self.login_frame = customtkinter.CTkFrame(self.login_main_frame, corner_radius=0, fg_color="#343638")
                self.login_frame.pack(side='top', fill='both', pady=5, anchor='w')

                delete_button = customtkinter.CTkButton(self.login_frame,image = self.image_delete, text='', command=lambda l=login: self.delete_user(l), width=30, corner_radius=0, 
                                                fg_color=("#343638"),
                                                hover_color=("red"),
                                                anchor="center" )
                delete_button.pack(side='left')

                label = customtkinter.CTkLabel(self.login_frame, text=login, font=customtkinter.CTkFont(size=12, weight="bold"), text_color=("white"))
                label.pack(side='left', fill='x', padx=5)

                role_status, admin_status = user_statuses[login]

                admin_var = customtkinter.IntVar(value=admin_status)
                checkbox_admin_status = customtkinter.CTkCheckBox(self.login_frame, text='', variable=admin_var, command=lambda l=login, var=admin_var: self.on_admin_checkbox_click(l, var), width=0, checkbox_height=20, checkbox_width=20, corner_radius=1, border_width=2, hover_color="red", fg_color="red",)
                checkbox_admin_status.pack(side='right')
                
                role_var = customtkinter.IntVar(value=role_status)
                checkbox_role = customtkinter.CTkCheckBox(self.login_frame, text='', variable=role_var, command=lambda l=login, var=role_var: self.on_role_checkbox_click(l, var), width=0, checkbox_height=20, checkbox_width=20, corner_radius=1, border_width=2, hover_color="red", fg_color="red")
                checkbox_role.pack(side='right')

        except Exception as e:
            print(f"Error deleting user: {e}")



    def on_role_checkbox_click(self, login, role_var):
        # Обработка события для чекбокса Role Status с учетом логина и статуса
        new_status = role_var.get()
        print(f"Role checkbox clicked for {login} with status {new_status}")
        self.cursor.execute('UPDATE users SET role = %s WHERE login = %s', (new_status, login))


    def on_admin_checkbox_click(self, login, admin_var):
        # Обработка события для чекбокса Admin Status с учетом логина и статуса
        new_status = admin_var.get()
        print(f"Admin checkbox clicked for {login} with status {new_status}")
        self.cursor.execute('UPDATE users SET admin_status = %s WHERE login = %s', (new_status, login))



    def on_closing(self, event=0):

        self.destroy()


