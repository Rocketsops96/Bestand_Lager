import customtkinter
import regbase
from tkcalendar import DateEntry
import threading
import time
from tkinter import filedialog
import base64
from win10toast import ToastNotifier
import os
from tkinter import StringVar






class Bau(customtkinter.CTkToplevel):

    APP_NAME = "VVO Erstellen"
    WIDTH = 300   
    HEIGHT = 700
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = regbase.create_conn()
        self.title(Bau.APP_NAME)
        self.geometry(str(Bau.WIDTH) + "x" + str(Bau.HEIGHT))
        self.minsize(Bau.WIDTH, Bau.HEIGHT)
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.bind("<Command-q>", self.on_closing)
        # self.bind("<Command-w>", self.on_closing)

        self.two_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.two_frame.grid(row=0, column=0, padx=10, pady=10, sticky= "nsew")

        self.status_bau = customtkinter.CTkOptionMenu(self.two_frame, values=["Aktiv","Inaktiv"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")
        
        # self.name_bau = customtkinter.CTkEntry(self.two_frame, placeholder_text="Name:", width= 250, corner_radius = 3)
        # self.name_bau.grid(column= 0, row=1, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.kostenstelle_vvo = customtkinter.CTkEntry(self.two_frame, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo.grid(column= 0, row=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        # self.kostenstelle_plannung = customtkinter.CTkEntry(self.two_frame, placeholder_text="Kostenstelle Verkehrsplannung:", width= 250, corner_radius = 3)
        # self.kostenstelle_plannung.grid(column= 0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.kostenstelle_plannung_var = StringVar()

        self.kostenstelle_plannung_button = customtkinter.CTkButton(self.two_frame, text="VZP ordner auswählen", 
                                                                    command=self.choose_folder, width=250,
                                                                    fg_color=("gray70", "gray30"), corner_radius=2, 
                                                                    text_color=("gray10", "gray90"), hover_color=("red"),
                                                                    font=customtkinter.CTkFont(size=14, weight="bold"),
                                                                    anchor="center")
        self.kostenstelle_plannung_button.grid(column=0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")


        self.bauvorhaben = customtkinter.CTkEntry(self.two_frame, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ansprechpartner = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse = customtkinter.CTkEntry(self.two_frame, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label.grid(row=8, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.uber = customtkinter.CTkSwitch(self.two_frame, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber.grid(column = 0, row = 10, padx=(10, 10), pady=(0, 10), sticky="nw")


        self.create_bau = customtkinter.CTkButton(master=self.two_frame, corner_radius=2, height=30, width=250, border_spacing=5, text="Speichern",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.create)
        self.create_bau.grid(column = 0,row=11, padx=(10,0), pady=(0, 10), sticky="nw")


    def create(self):
        cursor = self.conn.cursor()
        # name = self.name_bau.get()
        status = self.status_bau.get()
        kostenstelle_vvo = self.kostenstelle_vvo.get()
        bauvorhaben = self.bauvorhaben.get()
        strasse = self.strasse.get()
        ort = self.ort.get()
        ausfurung_von = self.ausfurung_von.get()
        ausfurung_bis = self.ausfurung_bis.get()
        uberwacht = self.uber.get()
        ansprechpartner = self.ansprechpartner.get()
        kostenstelle_plannung = self.kostenstelle_plannung_var.get()
 

        if not strasse or not kostenstelle_vvo or not bauvorhaben or not ort or not ansprechpartner:
            
            # if not name:
            #     threading.Thread(target=lambda: self.flash_error_color(self.name_bau), args=()).start()
            # else:
            #     self.name_bau.configure(border_color="grey")

            if not kostenstelle_vvo:
                threading.Thread(target=lambda: self.flash_error_color(self.kostenstelle_vvo), args=()).start()
            else:
                self.kostenstelle_vvo.configure(border_color="grey")
            if not bauvorhaben:
                threading.Thread(target=lambda: self.flash_error_color(self.bauvorhaben), args=()).start()
            else:
                self.bauvorhaben.configure(border_color = "grey")

            if not strasse:
                threading.Thread(target=lambda: self.flash_error_color(self.strasse), args=()).start()
            else:
                self.strasse.configure(border_color = "grey")
            
            if not ort:
                threading.Thread(target=lambda: self.flash_error_color(self.ort), args=()).start()
            else:
                self.ort.configure(border_color = "grey")

            if not ansprechpartner: 
                threading.Thread(target=lambda: self.flash_error_color(self.ansprechpartner), args=()).start()
            else:
                self.ansprechpartner.configure(border_color = "grey")
            return  # Прерываем выполнение функции, так как не все обязательные поля заполнены
        
        cursor.execute("SELECT kostenstelle_vvo FROM Bau WHERE kostenstelle_vvo = %s", (kostenstelle_vvo,))
        existing_record = cursor.fetchone()
        if existing_record:
            threading.Thread(target=self.show_notification, args=("Ошибка", "Стройка с таким номером уже существует!")).start()
            threading.Thread(target=lambda: self.flash_error_color(self.kostenstelle_vvo), args=()).start()
            return  # Прерываем выполнение функции, так как запись уже существует
        
        cursor.execute(f"CREATE TABLE IF NOT EXISTS Bau (id SERIAL PRIMARY KEY,name_bau text, kostenstelle_vvo text,bauvorhaben text,ort text, strasse text,ausfurung_von text,ausfurung_bis text, ansprechpartner text, status text, uberwachung text, set_capo text, kostenstelle_plannung text)")

        meta_data = None
        checkbox_values = [
            None,
            None,
            None,
            None,
            
        ]
        set_capo = ", ".join(filter(None, checkbox_values))  # Собираем текст через запятую, удаляя пустые значения
        cursor.execute(f"INSERT INTO Bau (kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, uberwachung, set_capo, kostenstelle_plannung) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status,  uberwacht, set_capo, kostenstelle_plannung))

        # self.name_bau.delete(0, 'end')
        self.kostenstelle_vvo.delete(0, 'end')
        self.bauvorhaben.delete(0, 'end')
        self.strasse.delete(0, 'end')
        self.ort.delete(0, 'end')
        self.ansprechpartner.delete(0, 'end')
        threading.Thread(target=self.show_notification, args=("Уведомление", "Стройка создана!")).start()
        self.on_closing()
    
    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.kostenstelle_plannung_var.set(folder_path)

    def show_notification(self, title, message):
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)
  
    def flash_error_color(self, widget):
        for _ in range(5):  # Меняем цвет 5 раз
            widget.configure(border_color="grey")
            time.sleep(0.2)
            widget.configure(border_color="red")
            time.sleep(0.2)  # Задержка в 200 миллисекунд
    def flash_error_color_for_btn(self, widget):
        for _ in range(5):  # Меняем цвет 5 раз
            self.kostenstelle_plannung_button.configure(fg_color="grey")
            time.sleep(0.2)
            self.kostenstelle_plannung_button.configure(fg_color="red")
            time.sleep(0.2)  # Задержка в 200 миллисекунд
        
    def on_closing(self, event=0):
        self.destroy()

