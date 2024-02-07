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
from PIL import Image






class App(customtkinter.CTkToplevel):

    APP_NAME = "VVO Bau"
    WIDTH = 300   
    HEIGHT = 700
    
    def __init__(self,parent,product_id,conn, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.product_id = product_id
        self.conn = conn

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.two_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.two_frame.grid(row=0, column=0, padx=10, pady=10, sticky= "nsew")

        self.status_bau = customtkinter.CTkOptionMenu(self.two_frame, values=["Aktiv","Inaktiv", "Abgeschlossen"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")
        
        self.kostenstelle_vvo = customtkinter.CTkEntry(self.two_frame, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo.grid(column= 0, row=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        

        self.kostenstelle_plannung_var = StringVar()

        self.kostenstelle_plannung_button = customtkinter.CTkButton(self.two_frame, text="VZP ordner auswählen", 
                                                                    command=self.choose_folder, width=250,
                                                                    fg_color=("gray70", "gray30"), corner_radius=2, 
                                                                    text_color=("gray10", "gray90"), hover_color=("red"),
                                                                    font=customtkinter.CTkFont(size=14, weight="bold"),
                                                                    anchor="center")
        self.kostenstelle_plannung_button.grid(column=0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.kostenstelle_plannung_nr = customtkinter.CTkEntry(self.two_frame, placeholder_text="Kostenstelle planung:", width= 250, corner_radius = 3)
        self.kostenstelle_plannung_nr.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bauvorhaben = customtkinter.CTkEntry(self.two_frame, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ansprechpartner = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse = customtkinter.CTkEntry(self.two_frame, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label.grid(row=10, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis.grid(column= 0, row=10, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.umbau_datum_label = customtkinter.CTkLabel(self.two_frame, text="Umbau:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.umbau_datum_label.grid(column=0, row=11, padx=10, pady=(0,10), sticky = "nw")

        check_var = customtkinter.StringVar(value="off")
        self.check_umbau = customtkinter.CTkCheckBox(self.two_frame,variable=check_var, text="",width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red", onvalue="1", offvalue="0")
        self.check_umbau.grid(column=0, row=11, padx=(10, 100), pady=(0,10), sticky = "ne")

        self.umbau_datum = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.umbau_datum.grid(column= 0, row=11, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.uber = customtkinter.CTkSwitch(self.two_frame, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber.grid(column = 0, row = 12, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.btn_frame = customtkinter.CTkFrame(self.two_frame, fg_color="transparent")
        self.btn_frame.grid(row=13, column=0, padx=10, pady=10, sticky= "nw")

        self.image_change = customtkinter.CTkImage(light_image=Image.open("images/save.png"), dark_image=Image.open("images/save.png"), size=(50, 50))
        self.change_bau_btn = customtkinter.CTkButton(master=self.btn_frame, corner_radius=0, height=50, width=50, text="", image = self.image_change,
                                                fg_color=("#2d2e2e"), text_color=("gray90"), hover_color=("red"),
                                                    anchor="center", command=self.chanhe_bau)
        self.change_bau_btn.pack(side='left', padx=(10,30), anchor="nw")

        self.image_complete = customtkinter.CTkImage(light_image=Image.open("images/complete.png"), dark_image=Image.open("images/complete.png"), size=(50, 50))
        self.complete_btn = customtkinter.CTkButton(master=self.btn_frame, corner_radius=0, height=50, width=50,text="", image = self.image_complete,
                                                fg_color=("#2d2e2e"), text_color=("gray90"), hover_color=("red"),
                                                    anchor="center", command=self.complete_bau)
        self.complete_btn.pack(side='left', padx=(0,30), anchor="nw")

        self.image_delete = customtkinter.CTkImage(light_image=Image.open("images/delete2.png"), dark_image=Image.open("images/delete2.png"), size=(50, 50))
        deactive_button = customtkinter.CTkButton(self.btn_frame, image=self.image_delete, text="", command=self.deactive_bau,corner_radius=0, height=50, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),
                                                anchor="center" )
        deactive_button.pack(side='left',pady=(0,10), padx=1, anchor="nw")
        self.show_all_info()



    def check_connection(self):
        try:
            if self.conn is None or self.conn.closed != 0:
                # Если соединения нет или оно закрыто, создаем новое соединение
                self.conn = regbase.create_conn()
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def check_connection_with_thread(self):
        threading.Thread(target=self.check_connection).start()

    def complete_bau(self):
        cursor = self.conn.cursor()
        complete = "1"
        cursor.execute("UPDATE bau SET complete = %s WHERE id = %s", (complete, self.product_id))
        self.on_closing()

    def deactive_bau(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bau SET status = 'Inaktiv' WHERE id = %s", (self.product_id,))
        self.on_closing()


    def show_all_info(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, kostenstelle_plannung, uberwachung, kostenstelle_plannung_nr, umbau_datum, check_umbau FROM Bau WHERE id = %s",(self.product_id,))
        data = cursor.fetchone()
        self.status_bau.set(data[8])
        # self.name_bau.insert(0, data[1])
        self.kostenstelle_vvo.insert(0, data[1])
        self.bauvorhaben.insert(0, data[2])
        self.ort.insert(0, data[3])
        self.strasse.insert(0, data[4])
        self.ausfurung_von.set_date(data[5])
        self.ausfurung_bis.set_date(data[6])
        self.ansprechpartner.insert(0, data[7])
        self.kostenstelle_plannung_var.set(data[9])

        if data[10] == "1":
            self.uber.select()
        else:
            self.uber.deselect()

        if data[11] != None:
            self.kostenstelle_plannung_nr.insert(0, data[11])

        self.umbau_datum.set_date(data[12])

        if data[13] == "1":
            self.check_umbau.select()
        else:
            self.check_umbau.deselect()

    def chanhe_bau(self):
        self.check_connection_with_thread()
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
        if not kostenstelle_plannung:
            kostenstelle_plannung = None
        check = self.check_umbau.get()
        kostenstelle_plannung_nr = self.kostenstelle_plannung_nr.get()
        if not kostenstelle_plannung_nr:
            kostenstelle_plannung_nr = None
        umbau = self.umbau_datum.get()

        if not strasse or not kostenstelle_vvo or not bauvorhaben or not ort or not ansprechpartner:
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

        cursor.execute("UPDATE bau SET kostenstelle_vvo = %s, bauvorhaben = %s, ort = %s, strasse = %s, ausfurung_von = %s, ausfurung_bis = %s, ansprechpartner = %s, status = %s, kostenstelle_plannung = %s, uberwachung = %s, check_umbau = %s, kostenstelle_plannung_nr = %s, umbau_datum = %s WHERE id = %s", (kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, kostenstelle_plannung, uberwacht,check, kostenstelle_plannung_nr, umbau, self.product_id))
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
        
    def on_closing(self, event=0):
        self.destroy()

