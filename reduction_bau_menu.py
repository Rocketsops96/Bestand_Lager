import customtkinter
import regbase
from tkcalendar import DateEntry
import threading
import time
from tkinter import filedialog
import base64
from win10toast import ToastNotifier
import os






class App(customtkinter.CTkToplevel):

    APP_NAME = "VVO Bau"
    WIDTH = 300   
    HEIGHT = 700
    
    def __init__(self,parent,product_id, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.product_id = product_id
        self.conn = regbase.create_conn()

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.two_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.two_frame.grid(row=0, column=0, padx=10, pady=10, sticky= "nsew")

        self.status_bau = customtkinter.CTkOptionMenu(self.two_frame, values=["Aktiv","Inaktiv"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")

        self.name_bau = customtkinter.CTkEntry(self.two_frame, placeholder_text="Name:", width= 250, corner_radius = 3)
        self.name_bau.grid(column= 0, row=1, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.kostenstelle_vvo = customtkinter.CTkEntry(self.two_frame, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo.grid(column= 0, row=2, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bauvorhaben = customtkinter.CTkEntry(self.two_frame, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben.grid(column= 0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse = customtkinter.CTkEntry(self.two_frame, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.vzp = customtkinter.CTkEntry(self.two_frame, placeholder_text="VZP:", width= 250, corner_radius = 3)
        self.vzp.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label.grid(row=7, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label = customtkinter.CTkLabel(self.two_frame, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label.grid(row=8, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.vrao_ab_label = customtkinter.CTkLabel(self.two_frame, text="VA. ab:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.vrao_ab_label.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.vrao_ab = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.vrao_ab.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.vrao_bis_label = customtkinter.CTkLabel(self.two_frame, text="VA. bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.vrao_bis_label.grid(row=10, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.vrao_bis = DateEntry(self.two_frame, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.vrao_bis.grid(column= 0, row=10, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ansprechpartner = customtkinter.CTkEntry(self.two_frame, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner.grid(column= 0, row=11, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.uber = customtkinter.CTkSwitch(self.two_frame, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber.grid(column = 0, row = 12, padx=(10, 10), pady=(0, 10), sticky="nw")


        self.select_plan_pdf = customtkinter.CTkButton(master=self.two_frame, corner_radius=5, height=30, width=250, border_spacing=5, text="Open VZP...",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.select_pdf)
        self.select_plan_pdf.grid(column = 0,row=14, padx=(10,0), pady=(0, 10), sticky="nw")

        self.selcteded_pdf_files = customtkinter.CTkLabel(self.two_frame, text="", 
                                                            font=customtkinter.CTkFont(size=11), text_color=("gray30"))
        self.selcteded_pdf_files.grid(row=15, column=0, padx=10, pady=(0,10), sticky = "e")

        self.change_bau_btn = customtkinter.CTkButton(master=self.two_frame, corner_radius=5, height=30, width=250, border_spacing=5, text="Upload",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.chanhe_bau)
        self.change_bau_btn.grid(column = 0,row=16, padx=(10,0), pady=(0, 10), sticky="nw")

        self.show_all_info()
    def show_all_info(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab, vrao_bis, ansprechpartner, status, vzp FROM Bau WHERE id = %s",(self.product_id,))
        data = cursor.fetchone()
        vzp_data = data[12]
        self.status_bau.set(data[11])
        self.name_bau.insert(0, data[1])
        self.kostenstelle_vvo.insert(0, data[2])
        self.bauvorhaben.insert(0, data[3])
        self.ort.insert(0, data[4])
        self.strasse.insert(0, data[5])
        if vzp_data:
            self.vzp.insert(0, data[12])
        self.ausfurung_von.set_date(data[6])
        self.ausfurung_bis.set_date(data[7])
        self.vrao_ab.set_date(data[8])
        self.vrao_bis.set_date(data[9])
        self.ansprechpartner.insert(0, data[10])

    def chanhe_bau(self):
        cursor = self.conn.cursor()
        name = self.name_bau.get()
        status = self.status_bau.get()
        kostenstelle_vvo = self.kostenstelle_vvo.get()
        bauvorhaben = self.bauvorhaben.get()
        strasse = self.strasse.get()
        ort = self.ort.get()
        ausfurung_von = self.ausfurung_von.get()
        ausfurung_bis = self.ausfurung_bis.get()
        vrao_ab = self.vrao_ab.get()
        vrao_bis = self.vrao_bis.get()
        uberwacht = self.uber.get()
        ansprechpartner = self.ansprechpartner.get()
        vzp = self.vzp.get()

        if not name or not strasse or not kostenstelle_vvo or not bauvorhaben or not ort or not ansprechpartner or not vzp:
            
            if not name:
                threading.Thread(target=lambda: self.flash_error_color(self.name_bau), args=()).start()
            else:
                self.name_bau.configure(border_color="grey")

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
            if not vzp:
                threading.Thread(target=lambda: self.flash_error_color(self.strasse), args=()).start()
            else:
                self.vzp.configure(border_color = "grey")
            if not ort:
                threading.Thread(target=lambda: self.flash_error_color(self.ort), args=()).start()
            else:
                self.ort.configure(border_color = "grey")

            if not ansprechpartner: 
                threading.Thread(target=lambda: self.flash_error_color(self.ansprechpartner), args=()).start()
            else:
                self.ansprechpartner.configure(border_color = "grey")
            return  # Прерываем выполнение функции, так как не все обязательные поля заполнены

        cursor.execute("UPDATE bau SET name_bau = %s, kostenstelle_vvo = %s, bauvorhaben = %s, ort = %s, strasse = %s, ausfurung_von = %s, ausfurung_bis = %s, vrao_ab = %s, vrao_bis = %s, ansprechpartner = %s, status = %s, vzp = %s, pdf_data = %s WHERE id = %s", (name, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis,vrao_ab, vrao_bis, ansprechpartner, status, vzp, self.pdf_data, self.product_id))
        self.on_closing()



    def select_pdf(self):
        pdf_file_paths = filedialog.askopenfilenames(title="Выберите PDF файлы", filetypes=[("PDF files", "*.pdf")])
        def encode_pdf_to_base64(pdf_file_path):
            with open(pdf_file_path, 'rb') as pdf_file:
                pdf_content = pdf_file.read()
                encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')
            return encoded_pdf
        # Если файлы не выбраны, выход из программы
        if not pdf_file_paths:
            print("No PDF files selected. Exiting.")
            exit()
       
        # self.selcteded_pdf_files.configure(text = pdf_file_path)
        pdf_files_base64 = []
        for pdf_file_path in pdf_file_paths:
            pdf_files_base64.append(encode_pdf_to_base64(pdf_file_path))

            # Преобразование списка в строку с разделителем запятой
        self.pdf_data = ','.join(pdf_files_base64)
        for pdf_file_path in pdf_file_paths:
            file_name = os.path.basename(pdf_file_path)
            self.selcteded_pdf_files.configure(text = file_name)
 
       
        threading.Thread(target=self.show_notification, args=("Уведомление", "Планы успешно загружены!")).start()

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

