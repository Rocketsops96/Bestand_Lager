import sqlite3
import customtkinter as tk

app = tk.Tk()
app.title("Авторизация")
# def main():


    
#     login = get_login()
#     if login is not None:
#         pswd = get_pswd(login)
#     else:
#         print('Неизвестный пользователь!')
#         return main()
#     print('-'*10)
#     print(f'Welcome {login}!')
    
# def get_login():
#     data = input('Enter login: ')
#     login = db(['login', 'login', data])
#     return login

# def get_pswd(login):
#     data = input('Enter password: ')
#     pswd = db(['pswd', login, data])
#     return pswd

# def db(data):
#     d_type = data[0]
#     val = data[1]
#     data = data[2]

#     conn = sqlite3.connect("bd.db")
#     cursor = conn.cursor()

    # try:
    #     if d_type == 'login':
    #         get = f"SELECT login FROM users WHERE login='{data}'"
    #     elif d_type == 'pswd':
    #         get = f"SELECT password FROM users WHERE login='{val}'"
    #     cursor.execute(get)
    #     result = cursor.fetchone()[0]
    #     if d_type == 'pswd':
    #         if result != data:
    #             print('Не правильный пароль!')
    #             return main()
    # except Exception as err:
    #     #print('Ошибка:', err)
    #     result = None
    # cursor.close()
    # conn.close()

    # return result


def vibor():
    print('1- Вставить')
    print('2- Удалить')
    print('3- ОБновить')
    print('4- Показать')
    vibor = input('Введите что вы хотите сделать: ')
  
    if vibor == "1":
        insert()
    elif vibor == "2":
        delete()
    elif vibor == "3":
        update()
    elif vibor == "4":
        select()
    elif vibor == "":
        print("Вы ничего не ввели")
    else:
        print("Вы ввели не правильное значение, введите из списка выше")



def inp():
    login = input('Введите логин: ')
    pswd = input('Введите пароль: ')
    return login, pswd

def log_select():
    login = input('Введите логин: ')
    return login
    

    



def insert():
    login, pswd = inp()
    conn = sqlite3.connect("bd.db")
    cursor = conn.cursor()
    sql = """INSERT INTO users
                        (login, password) 
                        VALUES (?, ?);"""
                        
    
    data_tuple = (login, pswd)
    cursor.execute(sql, data_tuple)
    conn.commit()
    cursor.close()
    conn.close()
    
    print('Inserted!')
    vibor()
    


def update():
    log = input("Введите логин: ")
    new_pass = input("Введите новый пароль: ")
    conn = sqlite3.connect("bd.db")
    cursor = conn.cursor()
    sql = """UPDATE users
             SET password=?
             WHERE login=?"""
    data_tuple = (new_pass, log)
    cursor.execute(sql, data_tuple)
    conn.commit()
    cursor.close()
    conn.close()

    print('Updated!')

def select():
    login = log_select()
    conn = sqlite3.connect("bd.db")
    cursor = conn.cursor()
    
    

    sql = "SELECT login, password FROM users WHERE login=?"
    
    cursor.execute(sql, [login])
    output = cursor.fetchall()
    if len(output) == 0:
        print('Такой пользователь не найден')
    else:
        cursor.close()
        conn.close()
        print('Output:', output)
        print(len(output))

    



def delete():
    log_del = input("Введите логин который хотите удалить: ")
    conn = sqlite3.connect("bd.db")
    cursor = conn.cursor()
    sql = """DELETE FROM users WHERE login=?"""
    cursor.execute(sql, [log_del])
    conn.commit()
    cursor.close()
    conn.close()

    print('Deleted!')


vibor()





class BestandLager(CTk.CTk):
    def __init__(self): # После теста добавить аргумент login и не забыть убрать комментарий ниже!!!!
        super().__init__()
        self.iconbitmap(default=r"vvo.ico")
        self.geometry("1280x720")
        self.title("Bestand Lager")
        self.resizable(False, False)

        self.result = CTk.CTkLabel(self, text=None, text_color="gray")
        self.result.grid(row=4, column=3, padx=(0, 0), pady=(50, 20), sticky="nsew")


        self.bar_code = customtkinter.CTkEntry(self, placeholder_text="Bar Code:", width=320)
        self.bar_code.grid(column= 3, row=2, padx=(0, 0), pady=(150, 20), sticky="nsew",)


        self.plus = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Добавить', command=self.open_dialog_plus)
        self.plus.grid(column = 2,row=3,padx=(340,10), pady=(50, 0), sticky="nsew")


        self.koll = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Количество', command=self.kol)
        self.koll.grid(column = 3,row=3,padx=(0,165), pady=(50, 0), sticky="nsew")


        self.minus = customtkinter.CTkButton(master=self, fg_color="transparent",  border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Убрать', command=self.open_dialog_minus)
        self.minus.grid(column = 3,row=3, padx=(165,0), pady=(50, 0), sticky="nsew")


        self.zamena = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='заменить', command=self.open_dialog_zamena)
        self.zamena.grid(column = 4,row=3, padx=(10,0), pady=(50, 0), sticky="nsew")



        self.exit = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, 
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text='Выход', command=self.exit)
        self.exit.grid(column = 5 ,row=4, padx=(165,0), pady=(400, 0), sticky="nsew")

        #self.login = login
        self.barcode = None
        self.error_label= None



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
            data = cursor.execute("UPDATE Lager_Bestand SET Aktueller_bestand = ? WHERE Bar_Code = ?", (num, self.barcode))
            conn.commit()

            data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
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


    def kol(self):
        self.barcode = self.bar_code.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand, Image_path FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()

        if data is not None:
            
            barcode_text = f"Bar Code: {data[0]}"
            vznr_text = f"VZ Nr: {data[1]}"
            bedeutung_text = f"Bedeutung: {data[2]}"
            Kol = f"Aktueller_bestand: {data[3]}"
        
            # Объединяем текст с значениями
            result_text = f"{barcode_text}\n{vznr_text}\n{bedeutung_text}\n{Kol}"
        
            self.result_show(result_text)

        else:
            self.result_show("Данного Bar Code не существует")

        cursor.close()
        conn.close()


    def open_dialog_zamena(self):
        self.barcode = self.bar_code.get()
        conn = sqlite3.connect("bd.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT Bar_Code, VZ_Nr, Bedeutung, Aktueller_bestand FROM Lager_Bestand WHERE Bar_Code = ?", (self.barcode,)).fetchone()
        
        if data is not None:
            dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="Test")
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
        print("Zamenna")


    

    def result_show(self, message):
            if self.error_label:
                self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было

            self.error_label = CTk.CTkLabel(self, text=message, text_color="gray")
            self.error_label.grid(row=4, column=3, padx=(0, 0), pady=(50, 20), sticky="nsew")


    def exit (self):
        self.destroy()  # Сворачиваем окно
        new_window = Autorisation.App()
        new_window.mainloop()  # Запускаем главный цикл нового окна


