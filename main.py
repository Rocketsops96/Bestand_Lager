import customtkinter
import customtkinter as CTk
from tkinter import *
from tkinter import ttk
import Autorisation
import PIL.Image
from CTkListbox import *
from tkinter.simpledialog import askstring
import tkinter.messagebox
from CTkTable import *
import export_to_exel
import os
import localizations
import logging
import regbase
from tkinter import filedialog
import base64
from PIL import Image
from io import BytesIO
from tkcalendar import DateEntry
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import threading
from win10toast import ToastNotifier
import time
from set_capo_toplevel import Set_Capo
import test_map
from tkintermapview import TkinterMapView
from CTkToolTip import *
from export_to_word_stunden import insert_data_into_excel
from export_to_word_material import insert_data_into_tables
from tkinter import messagebox







customtkinter.set_appearance_mode("dark")

class BestandLager(CTk.CTk):
    def __init__(self,login, role, conn, admin): # После теста добавить аргумент login и role  не забыть убрать комментарий ниже!!!!
        super().__init__()
        threading.Thread(target=self.load_image).start()
         # Настройки логирования
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Создайте объект логгера для вашего класса или модуля
        self.logger = logging.getLogger(__name__)
        self.role = role # Для полного функционала изменить 1 на role
        self.admin = admin
        self.language = self.load_language_from_file()  # Загружаем язык из файла
        # Установите геометрию окна
        self.geometry("1280x720")
        self.iconbitmap(default=r"vvo.ico")
        self.title("VVO GmbH")
        self.resizable(True, True)  # Запрещаем или разрешаем изменение размера окна
        self.state("zoomed")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #Создаем навигационный фрейм
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.conn = conn

        #Создаем текст вверху слева
        text = f"VVO\nWillkommen {login}"
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=text, 
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.sign = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Road signs", font=("Arial", 14, "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.home_button_event)
        self.sign.grid(row=1, column=0, sticky="ew")
        
        self.material_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Traffic safety", font=("Arial", 14, "bold"),
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.material_button_event)
        self.material_frame.grid(row=2, column=0, sticky="ew")
        

        self.bau_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Traffic monitoring", font=("Arial", 14, "bold"),
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.bau_button_event)
        self.bau_frame.grid(row=3, column=0, sticky="ew")

        self.log_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Logs", font=("Arial", 14, "bold"),
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.log_button_event)
        self.log_frame.grid(row=4, column=0, sticky="ew")
      
        
        self.language_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Russian","English","Deutsch"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.update_ui_language)
        self.language_menu.grid(row=10, column=0, padx=20, pady=(10, 0), sticky= "s")
        self.saved_language = self.load_language_from_file()
        self.language_menu.set(self.saved_language)

       
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["60%","70%","80%", "90%", "100%", "110%", "120%"],
                                                               fg_color="gray10", button_color="red",
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20), sticky= "s")
        self.scaling_optionemenu.set("100%")
        if self.admin == "1":
            image_map = customtkinter.CTkImage(light_image=Image.open("images/map.png"),
                                    dark_image=Image.open("images/map.png"),
                                    size=(30, 30))
            self.map_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=0, image = image_map, text="",
                                                        fg_color="gray10", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                            command=self.map)
            self.map_button.grid(row=12, column=0,pady = (0,5), sticky="ew")
        else:
            pass
        image_info = customtkinter.CTkImage(light_image=Image.open("images/info.png"),
                                  dark_image=Image.open("images/info.png"),
                                  size=(20, 20))
        self.info_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=0, image = image_info,  text="", font=("Arial", 14, "bold"),
                                                      fg_color="gray10", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        command=self.info)
        self.info_button.grid(row=13, column=0,pady = (0,5), sticky="ew")

        image_logout = customtkinter.CTkImage(light_image=Image.open("images/logout.png"),
                                  dark_image=Image.open("images/logout.png"),
                                  size=(20, 20))
        self.logout_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=0, image = image_logout,  text="", font=("Arial", 14, "bold"),
                                                      fg_color="gray10", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        command=self.exit)
        self.logout_button.grid(row=14, column=0,pady = (0,5), sticky="ew")

        #Создаем фреймы для каждого окна
        self.f1 = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.f1.grid_columnconfigure(0, weight=1)
        self.f1.grid_rowconfigure(0, weight=1)
        self.f1.grid_rowconfigure(1, weight=0)
     

        self.f2 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f2.grid_columnconfigure(0, weight=1)
        self.f2.grid_rowconfigure(0, weight=1)
      
        

        self.f3 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f3.grid_columnconfigure(0, weight=0)
        self.f3.grid_columnconfigure(1, weight=0)
        self.f3.grid_columnconfigure(2, weight=1)

        self.f4 = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.f4.grid_columnconfigure(0, weight=1)

        #Создаем дефолтный фрейм
        



############## ############## ############## ############## #Настройка фрейма №1 ############## ############## ############## ############## ############## 
       
        self.tabview = customtkinter.CTkTabview(self.f1, fg_color="#242424")
        self.tabview.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.tabview.add("View")
        self.tabview.add("Editing")
        self.tabview.add("Material")
        self.tabview.add("Werkzeug")
        self.tabview.tab("View").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Editing").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Material").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Werkzeug").grid_columnconfigure(0, weight=1)
        self.tabview.configure(segmented_button_selected_color="red")
        


        table_style = ttk.Style()
        table_style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="black")  # Для заголовков столбцов 
        table_style.configure("Treeview", font=("Arial", 14), foreground="white", rowheight=30)  # Для текста в ячейках
        table_style.configure("Treeview", background="#333333") 
        self.table = ttk.Treeview(self.tabview.tab("View"), columns=("","Bar Code", "VZ Nr.", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=21)
        self.table.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        self.table_for_editing = ttk.Treeview(self.tabview.tab("Editing"), columns=("","Bar Code", "VZ Nr.", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.table_for_editing.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
        
        
        self.table.column("#0", width=0, stretch=False)
        self.table.column("#1", minwidth=120)
        self.table.column("#2", minwidth=100)
        self.table.column("#3", minwidth=700)
        self.table.column("#4", minwidth=100)
        self.table.column("#5", minwidth=70)
        self.table.column("#6", minwidth=150)
        self.table.column("#7", width=0, stretch=False)
        
        # Добавляем заголовки столбцов
        
        self.table.heading("#1", text="Bar Code")
        self.table.heading("#2", text="VZ Nr.")
        self.table.heading("#3", text="Bedeutung")
        self.table.heading("#4", text="Größe")
        self.table.heading("#5", text="Lager")
        self.table.heading("#6", text="Aktueller")


        self.table_for_editing.column("#0", width=0, stretch=False)
        self.table_for_editing.column("#1", minwidth=120)
        self.table_for_editing.column("#2", minwidth=100)
        self.table_for_editing.column("#3", minwidth=700)
        self.table_for_editing.column("#4", minwidth=100)
        self.table_for_editing.column("#5", minwidth=70)
        self.table_for_editing.column("#6", minwidth=150)
        self.table_for_editing.column("#7", width=0, stretch=False)
        
        # Добавляем заголовки столбцов
        
        self.table_for_editing.heading("#1", text="Bar Code")
        self.table_for_editing.heading("#2", text="VZ Nr.")
        self.table_for_editing.heading("#3", text="Bedeutung")
        self.table_for_editing.heading("#4", text="Größe")
        self.table_for_editing.heading("#5", text="Lager")
        self.table_for_editing.heading("#6", text="Aktueller")

        self.home_frame1 = customtkinter.CTkFrame(self.tabview.tab("View"),fg_color="transparent")
        self.home_frame1.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame1.grid_columnconfigure(0, weight=1)
        self.home_frame2 = customtkinter.CTkFrame(self.tabview.tab("View"),fg_color="transparent")
        self.home_frame2.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame2.grid_columnconfigure(1, weight=1)

        self.home_frame3 = customtkinter.CTkFrame(self.tabview.tab("Editing"),fg_color="transparent")
        self.home_frame3.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame3.grid_columnconfigure(0, weight=1)
        self.home_frame4 = customtkinter.CTkFrame(self.tabview.tab("Editing"),fg_color="transparent")
        self.home_frame4.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame4.grid_columnconfigure(1, weight=1)

        self.home_frame5 = customtkinter.CTkFrame(self.tabview.tab("Material"),fg_color="transparent")
        self.home_frame5.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame5.grid_columnconfigure(0, weight=1)
        self.home_frame6 = customtkinter.CTkFrame(self.tabview.tab("Material"),fg_color="transparent")
        self.home_frame6.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame6.grid_columnconfigure(1, weight=1)

        self.home_frame7 = customtkinter.CTkFrame(self.tabview.tab("Werkzeug"),fg_color="transparent")
        self.home_frame7.grid(row=1, column=0, padx=(0,10), sticky="nw")
        self.home_frame7.grid_columnconfigure(0, weight=1)
        self.home_frame8 = customtkinter.CTkFrame(self.tabview.tab("Werkzeug"),fg_color="transparent")
        self.home_frame8.grid(row=1, column=1, padx=(10,10), sticky="ne")
        self.home_frame8.grid_columnconfigure(1, weight=1)
        
        self.tab1_label_search = customtkinter.CTkLabel(self.home_frame1, text="Search", 
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.tab1_label_search.grid(row=0, column=0, padx=20)

        self.bar_code = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
        self.bar_code.grid(column= 0, row=1, padx=(10, 10), pady=(5, 10), sticky="nw",)
        
        self.vz_nr = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Vz Nr.:", width= 250, corner_radius = 3)
        self.vz_nr.grid(column= 0, row=2, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bedeutung = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Bedeutung:", width= 250, corner_radius = 3)
        self.bedeutung.grid(column= 0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.btn_frame = customtkinter.CTkFrame(self.home_frame1, fg_color = "transparent")
        self.btn_frame.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        image_search = customtkinter.CTkImage(light_image=Image.open("images/search.png"),
                                    dark_image=Image.open("images/search.png"),
                                    size=(30, 30))
        self.plus = customtkinter.CTkButton(master=self.btn_frame, corner_radius=1, width=80, height= 40, border_spacing=0, image = image_search,  text="",
                                                fg_color=("#343638"), hover_color=("red"),
                                                    anchor="center", command=self.kol2)
        self.plus.grid(column = 0,row=0, padx=(0,5), pady=(0, 10), sticky="nw")

        image_show_all = customtkinter.CTkImage(light_image=Image.open("images/show_all.png"),
                                    dark_image=Image.open("images/show_all.png"),
                                    size=(30, 30))
        self.show_all = customtkinter.CTkButton(master=self.btn_frame, corner_radius=1,width=80,height= 40, border_spacing=0, image = image_show_all, text="",
                                                fg_color=("#343638"), hover_color=("red"),
                                                    anchor="center", command=self.show_all_data)
        self.show_all.grid(column = 1,row=0, padx=(0,5), pady=(0, 10), sticky="nw")
        if self.admin == "1":
            image_excel = customtkinter.CTkImage(light_image=Image.open("images/excel.png"),
                                    dark_image=Image.open("images/excel.png"),
                                    size=(30, 30))
            self.export_to_exel_button = customtkinter.CTkButton(master=self.btn_frame, corner_radius=1,width=80,height= 40, border_spacing=0, text="", image= image_excel,
                                                    fg_color=("#343638"), hover_color=("red"),
                                                        anchor="center", command=self.export_to_excel_button_click)
            self.export_to_exel_button.grid(column = 2,row=0, padx=(0,0), pady=(0, 10), sticky="nw")
            self.export_to_exel_button.grid_rowconfigure(5, weight=1)
        else:
            pass

    
        self.reduction = customtkinter.CTkOptionMenu(self.home_frame3, values=["Current","Total on account","Defect"],
                                                               fg_color="gray10", button_color="red", command= self.handle_reduction_change, corner_radius = 1, button_hover_color = "black")
        self.reduction.grid(row=0, column=0, padx=10, pady=(20, 0), sticky= "nsew")

        self.selected_action = tkinter.StringVar()  # Создаем переменную для хранения выбранной радиокнопки

        self.plus_to_table = customtkinter.CTkRadioButton(self.home_frame3, text="Add", variable=self.selected_action, value="Add", fg_color = "red", hover_color = "red",
                                                          border_width_unchecked = 2, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.plus_to_table.grid(row=1, column=0, padx=(10, 10), pady=(5, 0), sticky="nsew")

        self.minus_to_table = customtkinter.CTkRadioButton(self.home_frame3, text="Decrease", variable=self.selected_action, value="Decrease", fg_color = "red", hover_color = "red",
                                                           border_width_unchecked = 2, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.minus_to_table.grid(row=2, column=0, padx=(10, 10), pady=(5, 0), sticky="nsew")

        self.zamena_to_table = customtkinter.CTkRadioButton(self.home_frame3, text="Replace", variable=self.selected_action, value="Replace", fg_color = "red", hover_color = "red",
                                                            border_width_unchecked = 2, font=customtkinter.CTkFont(size=14, weight="bold"))
        self.zamena_to_table.grid(row=3, column=0, padx=(10, 10), pady=(5, 0), sticky="nsew")

        self.vz_frame3 = customtkinter.CTkEntry(self.home_frame3, placeholder_text="VZ Nr.:", width= 250, corner_radius = 3)
        self.vz_frame3.grid(column= 1, row=0,  pady=(20, 0),padx = 10, sticky="nsew")

        self.bar_code_home_frame3 = customtkinter.CTkEntry(self.home_frame3, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
        self.bar_code_home_frame3.grid(column= 1, row=1,  pady=(10, 0),padx = 10, sticky="nsew")
        

        self.sum_home_frame3 = customtkinter.CTkEntry(self.home_frame3, placeholder_text="Введите количество", width= 250, corner_radius = 3)
        self.sum_home_frame3.grid(column= 1, row=2, pady=(10, 0),padx = 10, sticky="nsew")

        self.apply = customtkinter.CTkButton(master=self.home_frame3, corner_radius=5, height=40, width=250, border_spacing=5, text="Apply",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.reduction_main_table)
        self.apply.grid(column = 1,row=3, padx=10, pady=20, sticky="nw")



        self.material_table = ttk.Treeview(self.tabview.tab("Material"), columns=("","Bar Code", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.material_table.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
    
        
        
        self.material_table.column("#0", width=0, stretch=False)
        self.material_table.column("#1", minwidth=50)
        self.material_table.column("#2", minwidth=700)
        self.material_table.column("#3", minwidth=100)
        self.material_table.column("#4", minwidth=70)
        self.material_table.column("#5", minwidth=150)
        self.material_table.column("#6", width=0, stretch=False)
        
        # Добавляем заголовки столбцов
        
        self.material_table.heading("#1", text="Bar Code")
        self.material_table.heading("#2", text="Bedeutung")
        self.material_table.heading("#3", text="Größe")
        self.material_table.heading("#4", text="Lager")
        self.material_table.heading("#5", text="Aktueller")


        #_________________________________________________________________________##################_________#############_______________________________________________________________#


        self.werkzeug_table = ttk.Treeview(self.tabview.tab("Werkzeug"), columns=("","Bar Code", "Bedeutung", "Größe", "Bestand Lager", "Aktueller bestand"), style="Treeview", height=24)
        self.werkzeug_table.grid(columnspan=2,row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
    
        
        
        self.werkzeug_table.column("#0", width=0, stretch=False)
        self.werkzeug_table.column("#1", minwidth=50)
        self.werkzeug_table.column("#2", minwidth=700)
        self.werkzeug_table.column("#3", minwidth=100)
        self.werkzeug_table.column("#4", minwidth=70)
        self.werkzeug_table.column("#5", minwidth=150)
        self.werkzeug_table.column("#6", width=0, stretch=False)
        
        # Добавляем заголовки столбцов
        
        self.werkzeug_table.heading("#1", text="Bar Code")
        self.werkzeug_table.heading("#2", text="Bedeutung")
        self.werkzeug_table.heading("#3", text="Größe")
        self.werkzeug_table.heading("#4", text="Lager")
        self.werkzeug_table.heading("#5", text="Aktueller")
############## ############## ############## ############## #Настройка фрейма №2 ############## ############## ############## ############## ##############    
       
        self.tabview_baustellen = customtkinter.CTkTabview(self.f2, fg_color="#242424")
        self.tabview_baustellen.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.tabview_baustellen.add("Bearbeitung")
        self.tabview_baustellen.add("Inaktiv")
        self.tabview_baustellen.add("Abgeschlossen")

        self.tabview_baustellen.tab("Bearbeitung").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Bearbeitung").grid_rowconfigure(2, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_rowconfigure(1, weight=1)
        self.tabview_baustellen.tab("Abgeschlossen").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Abgeschlossen").grid_rowconfigure(2, weight=1)

        self.tabview_baustellen.configure(segmented_button_selected_color="red")

        self.bau_frame1 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame1.grid(row=0, column=0, padx=(5,10),pady=(0,10), sticky="nsew")
        self.bau_frame1.grid_columnconfigure(0, weight=1)
        
        self.bau_frame2 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2.grid(row=1, column=0, padx=(5,10),pady=(10,10), sticky="nsew")
        self.bau_frame2.grid_columnconfigure(0, weight=1)
        
        self.bau_frame2_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2_2.grid(row=2, column=0, padx=(5,10),pady=(0,10), sticky="nsew")
        self.bau_frame2_2.grid_columnconfigure(0, weight=1)
        
        
        self.bau_frame3 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3.grid(row=0, column=0, padx=(5,10),pady=(0,5), sticky="nsew")
        self.bau_frame3.grid_columnconfigure(0, weight=1)
        
        self.bau_frame3_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3_2.grid(row=1, column=0, padx=(5,10),pady=(0,5), sticky="nsew")
        self.bau_frame3_2.grid_columnconfigure(0, weight=1)

        self.bau_frame4 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Abgeschlossen"),fg_color="transparent")
        self.bau_frame4.grid(row=0, column=0, padx=(5,10),pady=(0,10), sticky="nsew")
        self.bau_frame4.grid_columnconfigure(0, weight=1)
        
        self.bau_frame4_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Abgeschlossen"),fg_color="transparent")
        self.bau_frame4_2.grid(row=2, column=0, padx=(5,10),pady=(0,5), sticky="nsew")
        self.bau_frame4_2.grid_columnconfigure(0, weight=1)
       
        
############################



        
        
############## ############## ############## ############## #Настройка фрейма №3 ############## ############## ############## ############## ##############        
        
        
############## ############## ############## ############## #Настройка фрейма №4 ############## ############## ############## ############## ############## 
        # self.log_view = customtkinter.CTkTextbox(master=self.f4, width=400, corner_radius=3)
        # self.log_view.grid(row=0, column=0, padx=(5,5), pady=(5,0), sticky="nsew")
        # self.clear_log_button = customtkinter.CTkButton(self.f4,  corner_radius=2, height=30, width=250, border_spacing=5,
        #                                         fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
        #                                         font=customtkinter.CTkFont(size=15, weight="bold"),
        #                                         anchor="center", text="Clear logs", command=self.clear_logs)
        # self.clear_log_button.grid(row=1, column=0, pady=5, sticky="nsew")
        

        self.log_table_frame = customtkinter.CTkFrame(self.f4,fg_color="transparent")
        self.log_table_frame.grid(row=0, column=0, columnspan = 3, padx=(0,10), sticky="nsew")
        self.log_table_frame.grid_columnconfigure(0, weight=1)

        self.log_left = customtkinter.CTkFrame(self.f4)
        self.log_left.grid(row=1, column=0, padx=(0,10), pady=(5,10), sticky="ne")

        self.log_center = customtkinter.CTkFrame(self.f4)
        self.log_center.grid(row=1, column=1, padx=(0,10), pady=(5,10), sticky="nsew")
        self.log_center.configure(width=100)

        self.log_right = customtkinter.CTkFrame(self.f4)
        self.log_right.grid(row=1, column=2, padx=(0,10), pady=(5,10), sticky="nw")

        self.f4.grid_columnconfigure(0, weight=1)
        self.f4.grid_rowconfigure(0, weight=1)
        # self.f4.grid_columnconfigure(1, weight=1)
        self.f4.grid_columnconfigure(2, weight=1)
    
        self.log_table =  ttk.Treeview(self.log_table_frame, columns=("", "id", "Zeit", "Benutzer", "Aktion", "Kostenstelle", "Bauvorhaben"), style="Treeview", height=24)
        self.log_table.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
    
        self.log_table.column("#0", width=0, stretch=False)
        self.log_table.column("#1", width=80,minwidth = 50, anchor="center", stretch=False)
        self.log_table.column("#2", minwidth=200, anchor="center", stretch=False)
        self.log_table.column("#3", minwidth=100, anchor="center")
        self.log_table.column("#4", minwidth=70, anchor="center")
        self.log_table.column("#5", minwidth=150, anchor="center")
        self.log_table.column("#6", width=150, anchor="center")
        self.log_table.column("#7", width=0, stretch=False)
      
        
        # Добавляем заголовки столбцов
        self.log_table.heading("#1", text="id")
        self.log_table.heading("#2", text="Zeit")
        self.log_table.heading("#3", text="Benutzer")
        self.log_table.heading("#4", text="Aktion")
        self.log_table.heading("#5", text="Kostenstelle")
        self.log_table.heading("#6", text="Bauvorhaben")

        
        









############## ############## ############## ############## #Настройка фрейма №5 ############## ############## ############## ############## ##############         
        
        self.select_frame_by_name("home")
        # Открываем сразу стройки если зашел в учетную запись под Славой
        # if login == "v.jaufmann":
        #     self.select_frame_by_name("Traffic safety")
        # else:
        #     self.select_frame_by_name("home")

        self.bedeutung.bind("<KeyRelease>", self.check_bedeutung)
        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
        self.bedeutung.bind('<Return>', lambda event=None: self.kol2())
        self.log_table.bind("<<TreeviewSelect>>", self.on_log_select)
        # self.bar_code_f2.bind('<Return>', lambda event=None: self.add_button_bau())
        # self.sum.bind('<Return>', lambda event=None: self.add_button_bau())
        self.sum_home_frame3.bind('<Return>', lambda event=None: self.reduction_main_table())
        self.update_ui_language(self.language)
        self.update()
        self.after(300000, self.check_connection_periodically)  # Периодическая проверка каждые 5 минут

        
        self.login = login
        self.barcode = None
        self.error_label= None
        self.show_past_due_products = False
        
        self.show_logs()
        self.show_all_data()
        self.show_material_table()
        self.show_werkzeug_table()
        self.create_labels()
        self.display_existing_products()
        self.create_log_frames()
        

    def load_image(self):
        self.image_reduction = customtkinter.CTkImage(light_image=Image.open("images/reduction.png"), dark_image=Image.open("images/reduction.png"), size=(20, 20))
        self.image_photo = customtkinter.CTkImage(light_image=Image.open("images/photo.png"), dark_image=Image.open("images/photo.png"), size=(20, 20))
        self.image_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"), dark_image=Image.open("images/capo.png"), size=(20, 20))
        self.image_clock = customtkinter.CTkImage(light_image=Image.open("images/clock.png"), dark_image=Image.open("images/clock.png"), size=(20, 20))
        self.image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"), dark_image=Image.open("images/material.png"), size=(20, 20))
        self.image_delete = customtkinter.CTkImage(light_image=Image.open("images/delete.png"), dark_image=Image.open("images/delete.png"), size=(20, 20))
        self.image_search = customtkinter.CTkImage(light_image=Image.open("images/search.png"), dark_image=Image.open("images/search.png"), size=(20, 20))
        self.image_show_all = customtkinter.CTkImage(light_image=Image.open("images/show_all.png"),dark_image=Image.open("images/show_all.png"),size=(20, 20))
        self.image_add = customtkinter.CTkImage(light_image=Image.open("images/add_btn.png"),dark_image=Image.open("images/add_btn.png"),size=(20, 20))
        self.image_admin = customtkinter.CTkImage(light_image=Image.open("images/admin.png"),dark_image=Image.open("images/admin.png"),size=(20, 20))
        self.image_next = customtkinter.CTkImage(light_image=Image.open("images/next.png"),dark_image=Image.open("images/next.png"),size=(100, 100))

    def create_labels(self):
        heute = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Heute",width= 150, fg_color="#8c0303")
        heute.pack(side='left', padx=5, anchor="nw")
        diese_woche = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Diese Woche", width= 150, fg_color="#CE5145")
        diese_woche.pack(side='left', padx=(10,5), anchor="nw")
        nachste_woche = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Nächste Woche",width= 150, fg_color="#F89820", text_color = "black")
        nachste_woche.pack(side='left', padx=5, anchor="nw")
        bei_der_arbeit = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Wird Uberwacht",width= 150, fg_color="#66B032",text_color = "black")
        bei_der_arbeit.pack(side='left', padx=5, anchor="nw")
        self.search = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Suchen:", width= 250, height=28, corner_radius = 3)
        self.search.pack(side='left', padx=5, anchor="nw")
        
        search_btn = customtkinter.CTkButton(self.bau_frame1, image = self.image_search,text="", command=self.search_bau, corner_radius=2, height=28, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),
                                                anchor="center" )
        search_btn.pack(side='left', padx=5, anchor="center")

        
        show_all_items = customtkinter.CTkButton(self.bau_frame1, image= self.image_show_all, text="", command=self.update_product_list, corner_radius=2, height=28, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),
                                                anchor="center" )
        show_all_items.pack(side='left', padx=5, anchor="nw")

        if self.role == "1":
            add_btn = customtkinter.CTkButton(self.bau_frame1,image=self.image_add, text="", command=self.open_add_bau_menu_toplevel, corner_radius=2, height=28, width=50, 
                                                    fg_color=("#2d2e2e"), text_color=("gray90"),
                                                    hover_color=("red"),
                                                    anchor="center" )
            add_btn.pack(side='left', padx=5, anchor="nw")
        else:
            pass

        if self.admin == "1":
            self.adminpanel = customtkinter.CTkButton(self.bau_frame1,image = self.image_admin, text="", command=self.open_admin_panel, corner_radius=2, height=28, width=50, 
                                                    fg_color=("#2d2e2e"), text_color=("gray90"),
                                                    hover_color=("red"),
                                                    anchor="center" )
            self.adminpanel.pack(side='left', padx=5, anchor="nw")
        else:
            pass

        self.sort = customtkinter.CTkOptionMenu(self.bau_frame1, values=("Bauvorhaben", "Kostenstelle", "Ausführung von", "Ausführung bis"),
                                                               fg_color="gray10", button_color="red", corner_radius = 1,
                                                               command=self.update_product_list)
        self.sort.pack(side='left', padx=(5,0), anchor="nw")
        self.sort.set("Bauvorhaben")
        check_var = customtkinter.StringVar(value="on")
        self.on_sort = customtkinter.CTkCheckBox(self.bau_frame1,variable=check_var, text="",width = 0, checkbox_height = 28, checkbox_width = 28, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red", font=customtkinter.CTkFont(size=14, weight="bold"),onvalue="on", offvalue="off", command=self.update_product_list)
        self.on_sort.pack(side='left', padx=(0,5), anchor="nw")

        self.show_hide_product = customtkinter.CTkButton(self.bau_frame1, text="", command=self.show_hide_porduct_fun, corner_radius=2, height=28, width=50, font=customtkinter.CTkFont(size=15, weight="bold"),
                                                fg_color="#A7C393", text_color="black",
                                                hover_color=("red"),
                                                anchor="center" )
        self.show_hide_product.pack(side='left', padx=5, anchor="nw")
 

        label = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN", width= 330, fg_color="#0f5925")
        label.pack(side='left', padx=(5,1), anchor="nw")
        label2 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE",width= 150, fg_color="#0f5925")
        label2.pack(side='left', padx=0, anchor="nw")
        label3 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="ANSPRECHPARTNER",width= 180, fg_color="#0f5925")
        label3.pack(side='left', padx=0, anchor="nw")
        label4 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="VZP",width= 80, fg_color="#0f5925")
        label4.pack(side='left', padx=0, anchor="nw")
        label5 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSF, H.VERBOT",width= 150, fg_color="#0f5925")
        label5.pack(side='left', padx=0, anchor="nw")
        label6 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFÜHRUNG VON",width= 150, fg_color="#0f5925")
        label6.pack(side='left', padx=0, anchor="nw")
        umbau_datum = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="UMBAU",width= 100, fg_color="#0f5925")
        umbau_datum.pack(side='left', padx=0, anchor="nw")
        label7 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSF. BIS/VRAO ENDE",width= 180, fg_color="#0f5925")
        label7.pack(side='left', padx=0, anchor="nw")
        

        

        inaktiv_label2 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN",width= 330, fg_color="#0f5925")
        inaktiv_label2.pack(side='left', padx=(5,1), anchor="nw")
        inaktiv_label3 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE",width= 150, fg_color="#0f5925")
        inaktiv_label3.pack(side='left', padx=0, anchor="nw")
        inaktiv_label4 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="ANSPRECHPARTNER",width= 180, fg_color="#0f5925")
        inaktiv_label4.pack(side='left', padx=0, anchor="nw")
        inaktiv_label5 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="VZP",width= 80, fg_color="#0f5925")
        inaktiv_label5.pack(side='left', padx=0, anchor="nw")
        inaktiv_label7 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSFÜHRUNG VON",width= 150, fg_color="#0f5925")
        inaktiv_label7.pack(side='left', padx=0, anchor="nw")
        inaktiv_label8 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSF. BIS/VRAO ENDE",width= 180, fg_color="#0f5925")
        inaktiv_label8.pack(side='left', padx=0, anchor="nw")


        abgeschlossen_label2 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN",width= 330, fg_color="#0f5925")
        abgeschlossen_label2.pack(side='left', padx=(5,1), anchor="nw")
        abgeschlossen_label3 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE",width= 150, fg_color="#0f5925")
        abgeschlossen_label3.pack(side='left', padx=0, anchor="nw")
        abgeschlossen_label4 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text="ANSPRECHPARTNER",width= 180, fg_color="#0f5925")
        abgeschlossen_label4.pack(side='left', padx=0, anchor="nw")
        abgeschlossen_label5 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text="VZP",width= 80, fg_color="#0f5925")
        abgeschlossen_label5.pack(side='left', padx=0, anchor="nw")
        abgeschlossen_label7 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSFÜHRUNG VON",width= 150, fg_color="#0f5925")
        abgeschlossen_label7.pack(side='left', padx=0, anchor="nw")
        abgeschlossen_label8 = customtkinter.CTkLabel(self.bau_frame4, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSF. BIS/VRAO ENDE",width= 180, fg_color="#0f5925")
        abgeschlossen_label8.pack(side='left', padx=0, anchor="nw")
        self.search.bind('<Return>', lambda event=None: self.search_bau())
    
    def open_admin_panel(self):
        import privacy
        privacy_menu = privacy.Privacy(self, self.conn)  # создаем окно, если его нет или оно уничтожено
        privacy_menu.grab_set()  # захватываем фокус
        privacy_menu.wait_window()  # ждем закрытия дочернего окна
        privacy_menu.grab_release()  # освобождаем фокус после его закрытия

    def show_hide_porduct_fun(self):
        print(self.show_past_due_products)
        if self.show_past_due_products is False:
            products = self.get_products_from_database()
            past_due_products = [product for product in products if self.days_until_due(product) < 0 and 7 <= self.abbau_datum(product) and product['check_umbau'] == "0"]
            alternate_color = True

            for product in past_due_products:
                if product['complete'] in ("0", "1", None):
                    self.create_product_frame(product, alternate_color)
                    alternate_color = not alternate_color
            self.show_past_due_products = True
            
        elif self.show_past_due_products:
            self.show_past_due_products = False
            self.update_product_list()

    def days_until_due(self, product):
        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days
        return days_until_due
    
    def abbau_datum(self, product):
        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_bis'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days
        return days_until_due
    
    def expired_products_show_two_days(self, product):
        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_bis'], '%d.%m.%Y').date()
        days_until_due = (current_date - product_date).days
        return days_until_due
    
    def expired_umbau(self, product):
        current_date = datetime.now().date()
        product_date = datetime.strptime(product['umbau_datum'], '%d.%m.%Y').date()
        days_until_due = (current_date - product_date).days
        return days_until_due

    def umbau_datum(self, product):
        if product['check_umbau'] == "1":
            current_date = datetime.now().date()
            product_date = datetime.strptime(product['umbau_datum'], '%d.%m.%Y').date()
            umbau_days = (product_date - current_date).days
            return umbau_days
        return None  # Добавьте возврат None для случая, когда условие не выполняется
    
    def update_expired_products_show_two_days(self, product):
        id = product['id']
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bau SET status = 'Abgeschlossen' WHERE id = %s", (id,))

    def update_completed_products(self, product):
        id = product['id']
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bau SET complete = '0' WHERE id = %s", (id,))

    def display_existing_products(self):
        products = self.get_products_from_database()
        future_products = None
        abbau_products = None
        past_due_products = None
        expired_two_days = None
        umbau_products = None
        self.check_connection_with_thread()
        for product in products:
            if self.expired_products_show_two_days(product) > 2:
                self.update_expired_products_show_two_days(product)
            if product['umbau_datum'] is not None and product['umbau_datum'] != "0":
                if self.expired_umbau(product) > 0:
                    id = product['id']
                    self.check_connection_with_thread()
                    cursor = self.conn.cursor()
                    cursor.execute("UPDATE bau SET check_umbau = '0' WHERE id = %s", (id,))
                
            if self.days_until_due(product) < 0 and 7 <= self.abbau_datum(product):
                self.update_completed_products(product)
        products = self.get_products_from_database()
        
        future_products = [product for product in products if self.days_until_due(product) >= 0]
        abbau_products = [product for product in products if 0 <= self.abbau_datum(product) < 7 and self.days_until_due(product) < 0]
        umbau_products = [product for product in products if self.umbau_datum(product) is not None and 0 <= self.umbau_datum(product) < 7 and self.days_until_due(product) < 0 and product['check_umbau'] == "1"]
        umbau_past_due_products = [product for product in products if self.umbau_datum(product) is not None and 7 <= self.umbau_datum(product) and self.days_until_due(product) < 0 and product['check_umbau'] == "1"]
        past_due_products = [product for product in products if self.days_until_due(product) < 0 and 7 <= self.abbau_datum(product) and product['check_umbau'] == "0"]
        expired_two_days = [product for product in products if self.expired_products_show_two_days(product) >= 1 and self.expired_products_show_two_days(product) <= 2 and product['check_umbau'] == "0"]
        self.num_products = len(past_due_products) + len(abbau_products) +len(umbau_products) + len(umbau_past_due_products) +len(expired_two_days)
        self.show_hide_product.configure(text=self.num_products)
        
        # Сортируем товары, у которых дата еще предстоит
        sorted_future_products = sorted(future_products, key=self.days_until_due)
        
        alternate_color = True

        #Сортируем предстоящие стройки все
        for product in sorted_future_products:
            if product['complete'] == "0":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color

        #  Включаем сортировку по умбау
        for product in umbau_products:
            if product['complete'] == "0":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color

        # Включаем сортировку по аббау
        for product in abbau_products:
            if product['complete'] == "0":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color

        # Включаем сортировку  для строек у которых дата аббау уже прошла и оставляем еще на пару дней, после чего отправляем в абгешлесен
        for product in expired_two_days:
            if product['complete'] == "0":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color
            
        # Включаем сортировку для строек у котроых скоро будет умбау
        for product in umbau_past_due_products:
            if product['complete'] == "0":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color

        # Создаем фреймы для товаров, у которых дата уже прошла(зеленые, Wird uberwacht)
        if self.show_past_due_products:
            for product in past_due_products:
                if product['complete'] in ("0", "1", None):
                    self.create_product_frame(product, alternate_color)
                    alternate_color = not alternate_color

        for product in products:
            if product['complete'] == "1":
                self.create_product_frame(product, alternate_color)
                alternate_color = not alternate_color

        # Берем из бд стройки которые уже закрытые и выводим во вкладке Abgeschlosen
        abgeschlossen_products = self.get_abgeschlossen_from_database()
        for abgeschlossen_product in abgeschlossen_products:
            self.create_abgeschlossen_frame(abgeschlossen_product, alternate_color)
            alternate_color = not alternate_color

        # Берем данные из бд о неактивных стройках и создаем их во вкладке инактив
        inaktiv_products = self.get_inaktiv_from_database()
        for inaktiv_product in inaktiv_products:
            self.create_inaktiv_frame(inaktiv_product, alternate_color)
            alternate_color = not alternate_color     

    def get_abgeschlossen_from_database(self, status = 'Abgeschlossen'):
        # Открываете курсор для выполнения SQL-запроса
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, kostenstelle_plannung FROM bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'ansprechpartner': product_tuple[8],
                            'status': product_tuple[9], 'kostenstelle_plannung': product_tuple[10]}
            product_dicts.append(product_dict)
        return product_dicts

    def get_inaktiv_from_database(self, status = 'Inaktiv'):
        # Открываете курсор для выполнения SQL-запроса
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, kostenstelle_plannung FROM bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'ansprechpartner': product_tuple[8],
                            'status': product_tuple[9], 'kostenstelle_plannung': product_tuple[10]}
            product_dicts.append(product_dict)
        return product_dicts

    def get_products_from_database(self, status = 'Aktiv'):
        # Открываете курсор для выполнения SQL-запроса
        self.check_connection_with_thread()
        sort_field = self.sort.get()
        check = self.on_sort.get()
        if sort_field == "Bauvorhaben":
            sort_field = "bauvorhaben"
        if sort_field == "Kostenstelle":
            sort_field = "kostenstelle"
        if sort_field == "Ausführung von":
            sort_field = "ausfurung_von"
        if sort_field == "Ausführung bis": 
            sort_field = "ausfurung_bis"
        cursor = self.conn.cursor()
        if check == "on":
            print("включено")
            if sort_field == "bauvorhaben":
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE status = %s ORDER BY bauvorhaben", (status,))
            if sort_field == "kostenstelle":
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE status = %s ORDER BY kostenstelle_vvo", (status,))    
            if sort_field == "ausfurung_von":
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
            if sort_field == "ausfurung_bis": 
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE status = %s ORDER BY TO_DATE(ausfurung_bis, 'DD.MM.YYYY')", (status,))
        else:
            cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))

        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'ansprechpartner': product_tuple[8],
                            'status': product_tuple[9], 'set_capo': product_tuple[10],'kostenstelle_plannung': product_tuple[11], 'umbau_datum': product_tuple[12], 'check_umbau': product_tuple[13], 'complete': product_tuple[14]  }
            product_dicts.append(product_dict)

        return product_dicts
    
    def create_abgeschlossen_frame(self, product, alternate_color=False):
        self.product_frame = customtkinter.CTkFrame(self.bau_frame4_2, fg_color="transparent")
        self.product_frame.pack(fill='x', pady=0, anchor="nw")

        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        ausfurung_bis_date = datetime.strptime(product['ausfurung_bis'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days

        new_date = product_date - timedelta(days=6) #12.12.2023


            # Создаем поле с данными о товаре
        label1_text = product['bauvorhaben'][:38] + "..." if len(product['bauvorhaben']) > 38 else product['bauvorhaben']     
        label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label1_text, width= 330, anchor="w")
        label.pack(side='left',pady=0, padx=0, anchor="nw")
        CTkToolTip(label, message=f"{product['bauvorhaben']}")
        kostenstelle_btn = customtkinter.CTkButton(self.product_frame, text=f"{product['kostenstelle']}", command=lambda p=product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=0, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=0, padx=0, anchor="nw")
        label3 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ansprechpartner']}",width= 180)
        label3.pack(side='left',pady=0, padx=0, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.product_frame, text="VZP", command=lambda p=product['kostenstelle_plannung']: self.open_vzp_folder(p),corner_radius=0, height=28, width=80, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left',pady=0, padx=(0,1), anchor="nw")
        label5 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_von']}",width= 150)
        label5.pack(side='left',pady=0, padx=0, anchor="nw")
        label6 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_bis']}",width= 180)
        label6.pack(side='left',pady=0, padx=0, anchor="nw")


        
        reduction_btn = customtkinter.CTkButton(self.product_frame,image=self.image_reduction, text="", command=lambda p=product['id']: self.open_reduction_menu(p),corner_radius=0, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left',pady=0, padx=(1,1), anchor="nw")

         
        photo_button = customtkinter.CTkButton(self.product_frame,image=self.image_photo, text="", command=lambda p=product['kostenstelle']: self.open_photo_menu(p),corner_radius=0, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left',pady=0, padx=1, anchor="nw")

        
        set_capo = customtkinter.CTkButton(self.product_frame, image=self.image_capo, text="", command=lambda p=product['id']: self.set_capo_top_level(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left',pady=0, padx=1, anchor="nw")
        
        
        stunden = customtkinter.CTkButton(self.product_frame, image=self.image_clock, text="", command=lambda p=product['kostenstelle']: self.stunden_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left',pady=0, padx=1, anchor="nw")

        
        material = customtkinter.CTkButton(self.product_frame, image=self.image_material, text="", command=lambda p=product['kostenstelle']: self.material_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left',pady=0, padx=1, anchor="nw")

        label.configure(fg_color="grey")
        kostenstelle_btn.configure(fg_color="grey")
        label3.configure(fg_color="grey")
        label5.configure(fg_color="grey")
        label6.configure(fg_color="grey")
        vzp_btn.configure(fg_color="grey")
        reduction_btn.configure(fg_color="grey")
        photo_button.configure(fg_color="grey")
        set_capo.configure(fg_color="grey")
        stunden.configure(fg_color="grey")
        material.configure(fg_color="grey")

        if alternate_color:
                # Если условие выполнено, меняем цвет на альтернативный
                label.configure(fg_color="#A7C393", text_color="black")
                kostenstelle_btn.configure(fg_color="#A7C393", text_color="black")
                label3.configure(fg_color="#A7C393", text_color="black")
                label5.configure(fg_color="#A7C393", text_color="black")
                label6.configure(fg_color="#A7C393", text_color="black")
                vzp_btn.configure(fg_color="#A7C393", text_color="black")
                reduction_btn.configure(fg_color="#A7C393",text_color = "black")
                photo_button.configure(fg_color="#A7C393",text_color = "black")
                set_capo.configure(fg_color="#A7C393",text_color = "black")
                stunden.configure(fg_color="#A7C393",text_color = "black")
                material.configure(fg_color="#A7C393",text_color = "black")

    def create_inaktiv_frame(self, inaktiv_product, alternate_color=False):
        self.inaktiv_frame = customtkinter.CTkFrame(self.bau_frame3_2, fg_color="transparent")
        self.inaktiv_frame.pack(fill='x', anchor="nw")
       
        label1_text = inaktiv_product['bauvorhaben'][:38] + "..." if len(inaktiv_product['bauvorhaben']) > 38 else inaktiv_product['bauvorhaben']
        label2 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label1_text, width= 330, anchor="w")
        label2.pack(side='left', anchor="nw")
        CTkToolTip(label2, message=f"{inaktiv_product['bauvorhaben']}")
        kostenstelle_btn = customtkinter.CTkButton(self.inaktiv_frame, text=f"{inaktiv_product['kostenstelle']}", command=lambda p=inaktiv_product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=2, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=0, padx=0, anchor="nw")
        label4 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ansprechpartner']}",width= 180)
        label4.pack(side='left',pady=0, padx=0, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.inaktiv_frame, text="VZP", command=lambda p=inaktiv_product['kostenstelle_plannung']: self.open_vzp_folder(p),corner_radius=2, height=28, width=80, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left', anchor="nw")
        label5 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_von']}",width= 150)
        label5.pack(side='left', anchor="nw")
        label6 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_bis']}",width= 180)
        label6.pack(side='left', anchor="nw")


        image_reduction = customtkinter.CTkImage(light_image=Image.open("images/reduction.png"),
                                  dark_image=Image.open("images/reduction.png"),
                                  size=(20, 20))
        reduction_btn = customtkinter.CTkButton(self.inaktiv_frame,image=image_reduction, text="", command=lambda p=inaktiv_product['id']: self.open_reduction_menu(p),corner_radius=2, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left', anchor="nw")

        photo_image = customtkinter.CTkImage(light_image=Image.open("images/photo.png"),
                                  dark_image=Image.open("images/photo.png"),
                                  size=(20, 20))
        photo_button = customtkinter.CTkButton(self.inaktiv_frame,image=photo_image, text="", command=lambda p=inaktiv_product['kostenstelle']: self.open_photo_menu(p),corner_radius=2, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left', anchor="nw")

        image_set_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"),
                                  dark_image=Image.open("images/capo.png"),
                                  size=(20, 20))
        set_capo = customtkinter.CTkButton(self.inaktiv_frame, image=image_set_capo, text="", command=lambda p=inaktiv_product['id']: self.set_capo_top_level(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left', anchor="nw")
        
        image_stunden = customtkinter.CTkImage(light_image=Image.open("images/clock.png"),
                                  dark_image=Image.open("images/clock.png"),
                                  size=(20, 20))
        stunden = customtkinter.CTkButton(self.inaktiv_frame, image=image_stunden, text="", command=lambda p=inaktiv_product['kostenstelle']: self.stunden_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left', anchor="nw")

        image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        material = customtkinter.CTkButton(self.inaktiv_frame, image=image_material, text="", command=lambda p=inaktiv_product['kostenstelle']: self.material_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left', anchor="nw")

        image_return = customtkinter.CTkImage(light_image=Image.open("images/return.png"),
                                  dark_image=Image.open("images/return.png"),
                                  size=(20, 20))
        activate_button = customtkinter.CTkButton(self.inaktiv_frame, image=image_return, text="", command=lambda p=inaktiv_product['id']: self.activate_bau(p),corner_radius=2, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        activate_button.pack(side='left', anchor="nw")
        
        label2.configure(fg_color="grey")
        kostenstelle_btn.configure(fg_color="grey")
        label4.configure(fg_color="grey")
        label5.configure(fg_color="grey")
        label6.configure(fg_color="grey")
        vzp_btn.configure(fg_color="grey")
        reduction_btn.configure(fg_color="grey")
        photo_button.configure(fg_color="grey")
        set_capo.configure(fg_color="grey")
        stunden.configure(fg_color="grey")
        material.configure(fg_color="grey")
        if alternate_color:
                # Если условие выполнено, меняем цвет на альтернативный

                kostenstelle_btn.configure(fg_color="#A7C393", text_color="black")
                label2.configure(fg_color="#A7C393", text_color="black")
                label4.configure(fg_color="#A7C393", text_color="black")
                label5.configure(fg_color="#A7C393", text_color="black")
                label6.configure(fg_color="#A7C393", text_color="black")
                vzp_btn.configure(fg_color="#A7C393", text_color="black")
                reduction_btn.configure(fg_color="#A7C393",text_color = "black")
                photo_button.configure(fg_color="#A7C393",text_color = "black")
                set_capo.configure(fg_color="#A7C393",text_color = "black")
                stunden.configure(fg_color="#A7C393",text_color = "black")
                material.configure(fg_color="#A7C393",text_color = "black")

    def create_search_frame(self, product, alternate_color=False):
        self.product_frame = customtkinter.CTkFrame(self.bau_frame2_2, fg_color="transparent")
        self.product_frame.pack(fill='x', pady=0, anchor="nw")
        umbau_datum = None
        if product['check_umbau'] == "1":
            umbau_datum = product['umbau_datum']
            umbau_day = datetime.strptime(umbau_datum, '%d.%m.%Y').date()
        else:
            umbau_datum = ""

        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
       
        new_date = product_date - timedelta(days=6) #12.12.2023
        h_verbot=new_date.strftime('%d.%m.%Y')      #12.12.2023

            # Создаем поле с данными о товаре
        label1_text = product['bauvorhaben'][:38] + "..." if len(product['bauvorhaben']) > 38 else product['bauvorhaben']     
        label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label1_text, width= 330, anchor="w")
        label.pack(side='left',pady=0, padx=0, anchor="nw")
        CTkToolTip(label, message=f"{product['bauvorhaben']}")
        kostenstelle_btn = customtkinter.CTkButton(self.product_frame, text=f"{product['kostenstelle']}", command=lambda p=product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=0, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=0, padx=0, anchor="nw")
        label3 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ansprechpartner']}",width= 180)
        label3.pack(side='left',pady=0, padx=0, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.product_frame, text="VZP", command=lambda p=product['id']: self.open_vzp_folder(p),corner_radius=0, height=28, width=80, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left',pady=0, padx=(0,1), anchor="nw")
        label4 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold"), text=h_verbot, width=150)
        label4.pack(side='left',pady=0, padx=0, anchor="nw")
        label5 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_von']}",width= 150)
        label5.pack(side='left',pady=0, padx=0, anchor="nw")
        umbau_datum_label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=umbau_datum,width= 100)
        umbau_datum_label.pack(side='left',pady=0, padx=0, anchor="nw")
        label6 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_bis']}",width= 180)
        label6.pack(side='left',pady=0, padx=0, anchor="nw")


        
        reduction_btn = customtkinter.CTkButton(self.product_frame,image=self.image_reduction, text="", command=lambda p=product['id']: self.open_reduction_menu(p),corner_radius=0, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left',pady=0, padx=(1,1), anchor="nw")

         
        photo_button = customtkinter.CTkButton(self.product_frame,image=self.image_photo, text="", command=lambda p=product['kostenstelle']: self.open_photo_menu(p),corner_radius=0, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left',pady=0, padx=1, anchor="nw")

        
        set_capo = customtkinter.CTkButton(self.product_frame, image=self.image_capo, text="", command=lambda p=product['id']: self.set_capo_top_level(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left',pady=0, padx=1, anchor="nw")
        
        
        stunden = customtkinter.CTkButton(self.product_frame, image=self.image_clock, text="", command=lambda p=product['kostenstelle']: self.stunden_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left',pady=0, padx=1, anchor="nw")

        
        material = customtkinter.CTkButton(self.product_frame, image=self.image_material, text="", command=lambda p=product['kostenstelle']: self.material_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left',pady=0, padx=1, anchor="nw")
        label.configure(fg_color="grey",text_color = "white")
        kostenstelle_btn.configure(fg_color="grey",text_color = "white")
        label3.configure(fg_color="grey",text_color = "white")
        label4.configure(fg_color="grey",text_color = "white")
        label5.configure(fg_color="grey",text_color = "white")
        umbau_datum_label.configure(fg_color="grey",text_color = "white") 
        label6.configure(fg_color="grey",text_color = "white")
        vzp_btn.configure(fg_color="grey",text_color = "white")
        reduction_btn.configure(fg_color="grey",text_color = "white")
        photo_button.configure(fg_color="grey",text_color = "white")
        set_capo.configure(fg_color="grey",text_color = "white")
        stunden.configure(fg_color="grey",text_color = "white")
        material.configure(fg_color="grey",text_color = "white")
        if alternate_color:
            # Если условие выполнено, меняем цвет на альтернативный
            label.configure(fg_color="#A7C393", text_color="black")
            kostenstelle_btn.configure(fg_color="#A7C393", text_color="black")
            label3.configure(fg_color="#A7C393", text_color="black")
            label4.configure(fg_color="#A7C393", text_color="black")
            label5.configure(fg_color="#A7C393", text_color="black")
            umbau_datum_label.configure(fg_color="#A7C393",text_color = "black") 
            label6.configure(fg_color="#A7C393", text_color="black")
            vzp_btn.configure(fg_color="#A7C393", text_color="black")
            reduction_btn.configure(fg_color="#A7C393",text_color = "black")
            photo_button.configure(fg_color="#A7C393",text_color = "black")
            set_capo.configure(fg_color="#A7C393",text_color = "black")
            stunden.configure(fg_color="#A7C393",text_color = "black")
            material.configure(fg_color="#A7C393",text_color = "black")

    def create_product_frame(self, product, alternate_color=False):
        self.product_frame = customtkinter.CTkFrame(self.bau_frame2_2, fg_color="transparent")
        self.product_frame.pack(fill='x', pady=0, anchor="nw")
        umbau_day = None
        umbau_datum = None
        if product['check_umbau'] == "1":
            umbau_datum = product['umbau_datum']
            umbau_day = datetime.strptime(umbau_datum, '%d.%m.%Y').date()
        else:
            umbau_datum = ""

        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        ausfurung_bis_date = datetime.strptime(product['ausfurung_bis'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days


        new_date = product_date - timedelta(days=6) #12.12.2023
        h_verbot=new_date.strftime('%d.%m.%Y')      #12.12.2023

            # Создаем поле с данными о товаре
        label1_text = product['bauvorhaben'][:35] + "..." if len(product['bauvorhaben']) > 35 else product['bauvorhaben']     
        label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label1_text, width= 330, anchor="w")
        label.pack(side='left',pady=0, padx=0, anchor="nw")
        CTkToolTip(label, message=f"{product['bauvorhaben']}")
        kostenstelle_btn = customtkinter.CTkButton(self.product_frame, text=f"{product['kostenstelle']}", command=lambda p=product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=0, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=0, padx=0, anchor="nw")
        label3 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ansprechpartner']}",width= 180)
        label3.pack(side='left',pady=0, padx=0, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.product_frame, text="VZP", command=lambda p=product['id']: self.open_vzp_folder(p),corner_radius=0, height=28, width=80, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left',pady=0, padx=(0,1), anchor="nw")
        label4 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold"), text=h_verbot, width=150)
        label4.pack(side='left',pady=0, padx=0, anchor="nw")
        label5 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_von']}",width= 150)
        label5.pack(side='left',pady=0, padx=0, anchor="nw")
        umbau_datum_label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=umbau_datum,width= 100)
        umbau_datum_label.pack(side='left',pady=0, padx=0, anchor="nw")
        label6 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_bis']}",width= 180)
        label6.pack(side='left',pady=0, padx=0, anchor="nw")


        
        reduction_btn = customtkinter.CTkButton(self.product_frame,image=self.image_reduction, text="", command=lambda p=product['id']: self.open_reduction_menu(p),corner_radius=0, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left',pady=0, padx=(1,1), anchor="nw")

         
        photo_button = customtkinter.CTkButton(self.product_frame,image=self.image_photo, text="", command=lambda p=product['kostenstelle']: self.open_photo_menu(p),corner_radius=0, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left',pady=0, padx=1, anchor="nw")

        
        set_capo = customtkinter.CTkButton(self.product_frame, image=self.image_capo, text="", command=lambda p=product['id']: self.set_capo_top_level(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left',pady=0, padx=1, anchor="nw")
        
        
        stunden = customtkinter.CTkButton(self.product_frame, image=self.image_clock, text="", command=lambda p=product['kostenstelle']: self.stunden_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left',pady=0, padx=1, anchor="nw")

        
        material = customtkinter.CTkButton(self.product_frame, image=self.image_material, text="", command=lambda p=product['kostenstelle']: self.material_bau(p),corner_radius=0, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left',pady=0, padx=1, anchor="nw")

        

        label.configure(fg_color="grey")
        kostenstelle_btn.configure(fg_color="grey")
        label3.configure(fg_color="grey")
        label4.configure(fg_color="grey")
        label5.configure(fg_color="grey")
        umbau_datum_label.configure(fg_color="grey")        
        label6.configure(fg_color="grey")
        vzp_btn.configure(fg_color="grey")
        reduction_btn.configure(fg_color="grey")
        photo_button.configure(fg_color="grey")
        set_capo.configure(fg_color="grey")
        stunden.configure(fg_color="grey")
        material.configure(fg_color="grey")

        if product_date < current_date:
            # Если время прошло, устанавливаем зеленый цвет цвет
            label.configure(fg_color="#66B032",text_color = "black")
            kostenstelle_btn.configure(fg_color="#66B032",text_color = "black")
            label3.configure(fg_color="#66B032",text_color = "black")
            label4.configure(fg_color="#66B032",text_color = "black")
            label5.configure(fg_color="#66B032",text_color = "black")
            umbau_datum_label.configure(fg_color="#66B032",text_color = "black") 
            label6.configure(fg_color="#66B032",text_color = "black")
            vzp_btn.configure(fg_color="#66B032",text_color = "black")
            reduction_btn.configure(fg_color="#66B032",text_color = "black")
            photo_button.configure(fg_color="#66B032",text_color = "black")
            set_capo.configure(fg_color="#66B032",text_color = "black")
            stunden.configure(fg_color="#66B032",text_color = "black")
            material.configure(fg_color="#66B032",text_color = "black")
            if alternate_color:
                # Если условие выполнено, меняем цвет на альтернативный
                label.configure(fg_color="#A7C393", text_color="black")
                kostenstelle_btn.configure(fg_color="#A7C393", text_color="black")
                label3.configure(fg_color="#A7C393", text_color="black")
                label4.configure(fg_color="#A7C393", text_color="black")
                label5.configure(fg_color="#A7C393", text_color="black")
                umbau_datum_label.configure(fg_color="#A7C393",text_color = "black") 
                label6.configure(fg_color="#A7C393", text_color="black")
                vzp_btn.configure(fg_color="#A7C393", text_color="black")
                reduction_btn.configure(fg_color="#A7C393",text_color = "black")
                photo_button.configure(fg_color="#A7C393",text_color = "black")
                set_capo.configure(fg_color="#A7C393",text_color = "black")
                stunden.configure(fg_color="#A7C393",text_color = "black")
                material.configure(fg_color="#A7C393",text_color = "black")


        #Если остается 7 дней или менее до даты, устанавливаем красный цвет
        if 1 <= days_until_due <= 7:
            label.configure(fg_color="#CE5145",text_color = "black")
            kostenstelle_btn.configure(fg_color="#CE5145",text_color = "black")
            label3.configure(fg_color="#CE5145",text_color = "black")
            label4.configure(fg_color="#CE5145",text_color = "black")
            label5.configure(fg_color="#CE5145",text_color = "black")
            umbau_datum_label.configure(fg_color="#CE5145",text_color = "black") 
            label6.configure(fg_color="#CE5145",text_color = "black")
            vzp_btn.configure(fg_color="#CE5145",text_color = "black")
            reduction_btn.configure(fg_color="#CE5145",text_color = "black")
            photo_button.configure(fg_color="#CE5145",text_color = "black")
            set_capo.configure(fg_color="#CE5145",text_color = "black")
            stunden.configure(fg_color="#CE5145",text_color = "black")
            material.configure(fg_color="#CE5145",text_color = "black")

        # ставим ярко красный для стройки которая должна быть сегодня
        elif days_until_due == 0:
            label.configure(fg_color="#8c0303")
            kostenstelle_btn.configure(fg_color="#8c0303")
            label3.configure(fg_color="#8c0303")
            label4.configure(fg_color="#8c0303")
            label5.configure(fg_color="#8c0303")
            umbau_datum_label.configure(fg_color="#8c0303") 
            label6.configure(fg_color="#8c0303")
            vzp_btn.configure(fg_color="#8c0303")
            reduction_btn.configure(fg_color="#8c0303")
            photo_button.configure(fg_color="#8c0303")
            set_capo.configure(fg_color="#8c0303")
            stunden.configure(fg_color="#8c0303")
            material.configure(fg_color="#8c0303")
            
        if product_date > current_date:
            # current_week, _ = current_date.isocalendar()[1:]
            # current_month = current_date.month
            # current_year = current_date.year
            # due_week, _ = product_date.isocalendar()[1:]
            # due_month = product_date.month
            # due_year = product_date.year
            delta = product_date - current_date
            # Красим стройки в оранжевый, когда будет следующая неделя
            if delta.days <= 7 and 0 < delta.days <= 7 + current_date.weekday():
                label.configure(fg_color="#F89820", text_color="black")
                kostenstelle_btn.configure(fg_color="#F89820", text_color="black")
                label3.configure(fg_color="#F89820", text_color="black")
                label4.configure(fg_color="#F89820", text_color="black")
                label5.configure(fg_color="#F89820", text_color="black")
                umbau_datum_label.configure(fg_color="#F89820",text_color = "black") 
                label6.configure(fg_color="#F89820", text_color="black")
                vzp_btn.configure(fg_color="#F89820", text_color="black")
                reduction_btn.configure(fg_color="#F89820",text_color = "black")
                photo_button.configure(fg_color="#F89820",text_color = "black")
                set_capo.configure(fg_color="#F89820",text_color = "black")
                stunden.configure(fg_color="#F89820",text_color = "black")
                material.configure(fg_color="#F89820",text_color = "black")


        # Красим красныфм цветом дату установки H verbot если до даты постройки остается от 6 до 7 дней
        if 6 <= (product_date - current_date).days <= 7:
            label4.configure(fg_color = "#8c0303", text_color = "white")
        # Красим красныфм цветом дату постройки если до даты постройки остается от 1 до 2 дней
        if 1 <= (product_date - current_date).days <= 2:
            label5.configure(fg_color = "#8c0303", text_color = "white")
        if umbau_day is not None:
            if 3 <= (umbau_day - current_date).days <=7:
                umbau_datum_label.configure(fg_color = "#F89820", text_color = "black")
            if 0 <= (umbau_day - current_date).days <=2:
                umbau_datum_label.configure(fg_color = "#8c0303", text_color = "white")

        # Красим значок для капо серым, если для этой стройки назначен капо
        if not product['set_capo'] =="":
            set_capo.configure(fg_color="#bec1c4")
        
        if (ausfurung_bis_date - current_date).days <= 5:
            label6.configure(fg_color="#8c0303", text_color="white")
        if (current_date - ausfurung_bis_date).days >= 1 and (current_date - ausfurung_bis_date).days <= 2:
            label6.configure(fg_color="#CE5145", text_color="white")
        
        if product['complete'] == "1":

            # Если время прошло, устанавливаем зеленый цвет цвет
            label.configure(fg_color="#66B032",text_color = "black")
            kostenstelle_btn.configure(fg_color="#66B032",text_color = "black")
            label3.configure(fg_color="#66B032",text_color = "black")
            label4.configure(fg_color="#66B032",text_color = "black")
            label5.configure(fg_color="#66B032",text_color = "black")
            umbau_datum_label.configure(fg_color="#66B032",text_color = "black") 
            label6.configure(fg_color="#66B032",text_color = "black")
            vzp_btn.configure(fg_color="#66B032",text_color = "black")
            reduction_btn.configure(fg_color="#66B032",text_color = "black")
            photo_button.configure(fg_color="#66B032",text_color = "black")
            set_capo.configure(fg_color="#66B032",text_color = "black")
            stunden.configure(fg_color="#66B032",text_color = "black")
            material.configure(fg_color="#66B032",text_color = "black")
            if alternate_color:
                # Если условие выполнено, меняем цвет на альтернативный
                label.configure(fg_color="#A7C393", text_color="black")
                kostenstelle_btn.configure(fg_color="#A7C393", text_color="black")
                label3.configure(fg_color="#A7C393", text_color="black")
                label4.configure(fg_color="#A7C393", text_color="black")
                label5.configure(fg_color="#A7C393", text_color="black")
                umbau_datum_label.configure(fg_color="#A7C393",text_color = "black") 
                label6.configure(fg_color="#A7C393", text_color="black")
                vzp_btn.configure(fg_color="#A7C393", text_color="black")
                reduction_btn.configure(fg_color="#A7C393",text_color = "black")
                photo_button.configure(fg_color="#A7C393",text_color = "black")
                set_capo.configure(fg_color="#A7C393",text_color = "black")
                stunden.configure(fg_color="#A7C393",text_color = "black")
                material.configure(fg_color="#A7C393",text_color = "black")

    def search_bau(self):
        search= self.search.get()
        print(search)
        if search:
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            # Получаем данные из базы данных (замените на ваш SQL-запрос)
            cursor.execute("SELECT bauvorhaben FROM Bau WHERE LOWER(bauvorhaben) ILIKE LOWER(%s)", (f"%{search}%",))
            data = cursor.fetchall()
            if data:
                self.item = [item[0] for item in data]
                    
                for widget in self.bau_frame2_2.winfo_children():
                    widget.destroy()
                self.display_search_products()
            else:
                for widget in self.bau_frame2_2.winfo_children():
                    widget.destroy()
                print("Нет такой стройки")
        else:
            print("Не введены данные в поиск")
        self.search.delete(0, 'end')

    def display_search_products(self):
        products = self.get_products_for_serach()
        sorted_future_products = sorted(products, key=self.days_until_due)
        alternate_color = True

        for product in sorted_future_products:
            self.create_search_frame(product, alternate_color)
            alternate_color = not alternate_color

    def get_products_for_serach(self):
        # Открываете курсор для выполнения SQL-запроса
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        product_dicts = []
        for item in self.item:
            cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung, umbau_datum, check_umbau, complete FROM Bau WHERE bauvorhaben = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (item,))
            products = cursor.fetchall()
            for product_tuple in products:
                product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                                'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'ansprechpartner': product_tuple[8],
                                'status': product_tuple[9], 'set_capo': product_tuple[10],'kostenstelle_plannung': product_tuple[11], 'umbau_datum': product_tuple[12], 'check_umbau': product_tuple[13], 'complete': product_tuple[14]  }
                product_dicts.append(product_dict)

        return product_dicts

    def open_kostenstelle_folder(self, product_id):
            # Разбиваем текст по знаку "-"
        parts = product_id.split("-")

        # Проверяем, есть ли в тексте после знака "-" значение "24"
        if len(parts) > 1 and "24" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        elif len(parts) > 1 and "23" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2023\02 Verkehrssicherung"
        elif len(parts) > 1 and "22" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2022\02 Verkehrssicherung"
        elif len(parts) > 1 and "21" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2021\02 Verkehrssicherung"
        elif len(parts) > 1 and "20" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2020\02 Verkehrssicherung"
        elif len(parts) > 1 and "25" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2025\02 Verkehrssicherung"
        elif len(parts) > 1 and "26" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2026\02 Verkehrssicherung"
        elif len(parts) > 1 and "27" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2027\02 Verkehrssicherung"
        elif len(parts) > 1 and "28" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2028\02 Verkehrssicherung"
        else:
            # По умолчанию
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        items = os.listdir(os.path.normpath(base_path))
        matching_folders = [folder for folder in items if product_id.lower() in folder.lower()]
        if matching_folders:
            target_folder = os.path.join(base_path, matching_folders[0])
            os.startfile(target_folder)
   
    def open_vzp_folder(self, product_id):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT kostenstelle_plannung_nr, kostenstelle_plannung FROM bau WHERE id = %s ",(product_id,))
        data = cursor.fetchone()
        if data[1] != "" and data[0] is None:
            print(data[1])
            folder_vzp = os.path.normpath(data[1])
            os.startfile(folder_vzp)
        elif data[0] is not None and data[1] == "":
            print(data[0])
            vzp_nr = data[0]
            parts = vzp_nr.split("-")
            # Проверяем, есть ли в тексте после знака "-" значение "24"
            if len(parts) > 1 and "24" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2024\01 Verkehrsplannung"
            elif len(parts) > 1 and "23" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2023\01 Verkehrsplannung"
            elif len(parts) > 1 and "22" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2022\01 Verkehrsplannung"
            elif len(parts) > 1 and "21" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2021\01 Verkehrsplannung"
            elif len(parts) > 1 and "20" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2020\01 Verkehrsplannung"
            elif len(parts) > 1 and "25" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2025\01 Verkehrsplannung"
            elif len(parts) > 1 and "26" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2026\01 Verkehrsplannung"
            elif len(parts) > 1 and "27" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2027\01 Verkehrsplannung"
            elif len(parts) > 1 and "28" in parts[1]:
                base_path = r"\\FILESRV1\Abteilungen\VVO\2028\01 Verkehrsplannung"
            else:
                # По умолчанию
                base_path = r"\\FILESRV1\Abteilungen\VVO\2024\01 Verkehrsplannung"
            items = os.listdir(os.path.normpath(base_path))
            matching_folders = [folder for folder in items if vzp_nr.lower() in folder.lower()]
            if matching_folders:
                target_folder = os.path.join(base_path, matching_folders[0], "09 Verkehrszeichenpläne")
                os.startfile(target_folder)
        else:
            print(f"No folders matching the keyword '{product_id}' found.")

    def open_reduction_menu(self,product_id):
        if self.role == "1":
            import reduction_bau_menu
            action = "Änderung"
            cursor = self.conn.cursor()
            cursor.execute("SELECT kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, uberwachung, umbau_datum, check_umbau, kostenstelle_plannung_nr FROM bau WHERE id = %s ",(product_id,))
            data = cursor.fetchone()
            kostenstelle = data[0]
            bauvorhaben = data[1]
            ort = data[2]
            strasse = data[3]
            ausfurung_von = data[4]
            ausfurung_bis = data[5]
            ansprechpartner = data[6]
            status = data[7]
            uberwachung = data[8]
            umbau_datum = data[9]
            check_umbau = data[10]
            kostestelle_plannung_nr = data[11]

            cursor.execute("INSERT INTO app_logs (log_time, log_user, log_action,kostenstelle, bauvorhaben, status_do, kostenstelle_vvo_do, kostenstelle_plannung_nr_do, bauvorhaben_do, ansprechpartner_do, ort_do, strasse_do, ausfurung_von_do, ausfurung_bis_do, check_umbau_do, umbau_datum_do, uber_do ) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING log_id",(self.login,action, kostenstelle,bauvorhaben, status, kostenstelle, kostestelle_plannung_nr, bauvorhaben, ansprechpartner, ort, strasse, ausfurung_von, ausfurung_bis, check_umbau, umbau_datum, uberwachung ))
            last_insert_id = cursor.fetchone()[0]
            print(last_insert_id)
            reduction_menu = reduction_bau_menu.App(self, product_id, self.conn, last_insert_id)  # создаем окно, если его нет или оно уничтожено
            reduction_menu.grab_set()  # захватываем фокус
            reduction_menu.wait_window()  # ждем закрытия дочернего окна
            reduction_menu.grab_release()  # освобождаем фокус после его закрытия
            self.update_product_list()

    def stunden_bau(self, product_kostenstelle):
            # Разбиваем текст по знаку "-"
        parts = product_kostenstelle.split("-")

        # Проверяем, есть ли в тексте после знака "-" значение "24"
        if len(parts) > 1 and "24" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        elif len(parts) > 1 and "23" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2023\02 Verkehrssicherung"
        elif len(parts) > 1 and "22" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2022\02 Verkehrssicherung"
        elif len(parts) > 1 and "21" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2021\02 Verkehrssicherung"
        elif len(parts) > 1 and "20" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2020\02 Verkehrssicherung"
        elif len(parts) > 1 and "25" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2025\02 Verkehrssicherung"
        elif len(parts) > 1 and "26" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2026\02 Verkehrssicherung"
        elif len(parts) > 1 and "27" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2027\02 Verkehrssicherung"
        elif len(parts) > 1 and "28" in parts[1]:
            base_path = r"\\FILESRV1\Abteilungen\VVO\2028\02 Verkehrssicherung"
        else:
            # По умолчанию
            base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        prefix_to_match = "11"
        items = os.listdir(os.path.normpath(base_path))
        matching_folders = [folder for folder in items if product_kostenstelle.lower() in folder.lower()]
        if matching_folders:
            target_folder = os.path.join(base_path, matching_folders[0])
            # Ищем подпапку внутри найденной папки, начинающуюся с префикса "11"
            nested_folder_match = [nested_folder for nested_folder in os.listdir(target_folder) if nested_folder.startswith(prefix_to_match)]
            if nested_folder_match:
                nested_folder = nested_folder_match[0]
                # Путь к файлу "Stundenbericht Verkehrssicherung.docx"
                document_path = os.path.join(target_folder, nested_folder, "Stundenbericht Verkehrssicherung_VVO.xlsx")
            #     self.check_connection()
            #     cursor = self.conn.cursor()
            #     cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status FROM bau WHERE kostenstelle_vvo = %s", (product_kostenstelle, ))
            #     data = cursor.fetchone()
            #     data_dict = {
            #     'C5': data[2],
            #     'C9': data[3],
            #     'C11': f"{data[5]}, {data[4]}",
            #     'I11': data[8],
            # }
            #     # Вставляем данные в документ
            #     insert_data_into_excel(document_path, data_dict)
                # Открываем файл
                os.startfile(document_path)
            else:
                print(f"No folders starting with prefix '{prefix_to_match}' found inside folder '{target_folder}'.")
        else:
            print(f"No folders matching the keyword '{product_kostenstelle}' found.")

    def material_bau(self, product_kostenstelle):
        from material_window import Material

        material_window = Material(self, self.conn, product_kostenstelle)  # создаем окно, если его нет или оно уничтожено
        material_window.grab_set()  # захватываем фокус
        material_window.wait_window()  # ждем закрытия дочернего окна
        material_window.grab_release()  # освобождаем фокус после его закрытия   
        # parts = product_kostenstelle.split("-")

        # # Проверяем, есть ли в тексте после знака "-" значение "24"
        # if len(parts) > 1 and "24" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        # elif len(parts) > 1 and "23" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2023\02 Verkehrssicherung"
        # elif len(parts) > 1 and "22" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2022\02 Verkehrssicherung"
        # elif len(parts) > 1 and "21" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2021\02 Verkehrssicherung"
        # elif len(parts) > 1 and "20" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2020\02 Verkehrssicherung"
        # elif len(parts) > 1 and "25" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2025\02 Verkehrssicherung"
        # elif len(parts) > 1 and "26" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2026\02 Verkehrssicherung"
        # elif len(parts) > 1 and "27" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2027\02 Verkehrssicherung"
        # elif len(parts) > 1 and "28" in parts[1]:
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2028\02 Verkehrssicherung"
        # else:
        #     # По умолчанию
        #     base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        # prefix_to_match = "11"
        # items = os.listdir(os.path.normpath(base_path))
        # matching_folders = [folder for folder in items if product_kostenstelle.lower() in folder.lower()]
        # if matching_folders:
        #     target_folder = os.path.join(base_path, matching_folders[0])
        #     # Ищем подпапку внутри найденной папки, начинающуюся с префикса "11"
        #     nested_folder_match = [nested_folder for nested_folder in os.listdir(target_folder) if nested_folder.startswith(prefix_to_match)]
            
        #     if nested_folder_match:
        #         nested_folder = nested_folder_match[0]
        #         document_path = os.path.join(target_folder, nested_folder, "Materialliste.xlsx")
        #         # self.check_connection()
        #         # cursor = self.conn.cursor()
        #         # cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status FROM bau WHERE kostenstelle_vvo = %s",(product_kostenstelle, ))
        #         # data = cursor.fetchone()
        #         # data_table1 = [
        #         #     ["", data[2], "", "", f"{data[6]} - {data[7]}"],
        #         #     ["", "", "", "", ""],
        #         #     ["", data[3], "","",f"{data[6]} - {data[7]}"],
        #         #     ["", f"{data[5]}, {data[4]}","","", data[8]],
        #         # ]

        #         # # Вставляем данные в файл Excel
        #         # insert_data_into_tables(document_path,document_path, data_table1)

        #         # # Открываем файл
        #         os.startfile(document_path)
        #     else:
        #         print(f"No folders matching the keyword '{product_kostenstelle}' found.")

    def set_capo_top_level(self,product_id):
        if self.role == "1":
            self.toplevel_window = Set_Capo(self, product_id)  # создаем окно, если его нет или оно уничтожено
            self.toplevel_window.grab_set()  # захватываем фокус
            self.toplevel_window.wait_window()  # ждем закрытия дочернего окна
            self.toplevel_window.grab_release()  # освобождаем фокус после его закрытия
    
    def open_add_bau_menu_toplevel(self):
        from add_bau_menu import Bau
        self.toplevel_window = Bau()  # создаем окно, если его нет или оно уничтожено
        self.toplevel_window.grab_set()  # захватываем фокус
        self.toplevel_window.wait_window()  # ждем закрытия дочернего окна
        self.toplevel_window.grab_release()  # освобождаем фокус после его закрытия
        self.update_product_list()

        
    def deactive_bau(self, product_id):
        if self.role == "1":
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            cursor.execute("UPDATE bau SET status = 'Inaktiv' WHERE id = %s", (product_id,))
            self.update_product_list()
        else:
            messagebox.showinfo("Keine Zugriffsrechte", "Sie verfügen nicht über die erforderlichen Rechte, um diese Aktion auszuführen.")

    def activate_bau(self, product_id):
        if self.role == "1":
            current_date = datetime.now().date()
            today=current_date.strftime('%d.%m.%Y')  
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            cursor.execute("UPDATE bau SET status = 'Aktiv', ausfurung_bis = %s WHERE id = %s", (today, product_id))
            self.update_product_list()
        else:
            messagebox.showinfo("Keine Zugriffsrechte", "Sie verfügen nicht über die erforderlichen Rechte, um diese Aktion auszuführen.")

    def update_product_list(self, selected_option=None):
        # Очистите фреймы для активных и неактивных продуктов

        for widget in self.bau_frame2_2.winfo_children():
            widget.destroy()

        for widget in self.bau_frame3_2.winfo_children():
            widget.destroy()

        for widget in self.bau_frame4_2.winfo_children():
            widget.destroy()

        self.display_existing_products()

    def open_photo_menu(self,product_kostenstelle):
        from photo_top_level import Photo_menu
        photo_menu = Photo_menu(self, product_kostenstelle)  # создаем окно, если его нет или оно уничтожено
        photo_menu.grab_set()  # захватываем фокус
        photo_menu.wait_window()  # ждем закрытия дочернего окна
        photo_menu.grab_release()  # освобождаем фокус после его закрытия
    
    def show_notification(self, title, message):
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)

    def map(self):
        map_window = test_map.App()  # создаем окно, если его нет или оно уничтожено
        map_window.grab_set()  # захватываем фокус
        map_window.wait_window()  # ждем закрытия дочернего окна
        map_window.grab_release()  # освобождаем фокус после его закрытия     
    
    def handle_reduction_change(self, event):
        selected_reduction = self.reduction.get()  # Получаем выбранный параметр
        if selected_reduction == "Defect":
            self.minus_to_table.configure(state="disabled")
            self.zamena_to_table.configure(state="disabled")
        else: 
            self.plus_to_table.configure(state="normal")
            self.minus_to_table.configure(state="normal")
            self.zamena_to_table.configure(state="normal")

    def reduction_main_table(self):
        
        selected_reduction = self.reduction.get()
        selected_action = self.selected_action.get()
        bar_code = self.bar_code_home_frame3.get()
        sum_value = self.sum_home_frame3.get()
        vz = self.vz_frame3.get()
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        try:
            if selected_reduction == "Current":
                if selected_action == "Add":
                    cursor.execute("SELECT aktueller_bestand FROM Lager_Bestand WHERE bar_Code = %s OR vz_nr = %s", (bar_code,vz))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data + int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s OR vz_nr = %s", (new_value, bar_code,vz))
                    self.show_all_data()

                elif selected_action == "Decrease":
                    cursor.execute("SELECT aktueller_bestand FROM Lager_Bestand WHERE bar_Code = %s OR vz_nr = %s", (bar_code,vz))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data  - int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s OR vz_nr = %s", (new_value, bar_code, vz))
                    self.show_all_data()

                elif selected_action == "Replace":
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s OR vz_nr = %s", (sum_value, bar_code, vz))
                    self.show_all_data()

            if selected_reduction == "Total on account":
                if selected_action == "Add":
                    cursor.execute("SELECT bestand_lager FROM Lager_Bestand WHERE bar_Code = %s OR vz_nr = %s", (bar_code,vz))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data + int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s OR vz_nr = %s", (new_value, bar_code,vz))
                    self.show_all_data()

                elif selected_action == "Decrease":
                    cursor.execute("SELECT bestand_lager FROM Lager_Bestand WHERE bar_Code = %s OR vz_nr = %s", (bar_code,vz))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data  - int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s OR vz_nr = %s", (new_value, bar_code,vz))
                    self.show_all_data()

                elif selected_action == "Replace":
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s OR vz_nr = %s", (sum_value, bar_code, vz))
                    self.show_all_data()

            if selected_reduction == "Defect":
                if selected_action == "Add":
                    cursor.execute("SELECT * FROM Lager_Bestand WHERE bar_Code = %s OR vz_nr = %s", (bar_code, vz))
                    data = cursor.fetchone()
                    new_data = data[5]
                    new_data2 = data[4]
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data - int(sum_value) 
                    new_value2 = new_data2 - int(sum_value)
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s, bestand_lager = %s  WHERE bar_Code = %s OR vz_nr = %s", (new_value, new_value2, bar_code, vz))
                    if data:
                        # Если данные были найдены, извлекаем нужные значения
                        (bar_code, vz_nr, bedeutung, größe, bestand_lager, aktueller_bestand) = data
                        cursor.execute("SELECT * FROM Defekt WHERE bar_code = %s OR vz_nr = %s", (bar_code, vz))
                        existing_defekt_data = cursor.fetchone()
                        # Выполняем запрос на вставку данных в Defekt
                        if existing_defekt_data:
                            rest_data = existing_defekt_data[4] + int(sum_value)
                            cursor.execute("UPDATE Defekt SET bestand = %s WHERE bar_code = %s OR vz_nr = %s",(rest_data, bar_code, vz))
                        else:
                            cursor.execute("INSERT INTO Defekt (bar_code, vz_nr, bedeutung, größe, bestand) VALUES (%s, %s, %s, %s, %s)", (bar_code, vz_nr, bedeutung, größe, sum_value))
        except Exception as e:
            # Обработка ошибок, например, вывод сообщения
            print(f"Ошибка: {e}")
            self.show_all_data()
        self.bar_code_home_frame3.delete(0, 'end')
        self.sum_home_frame3.delete(0, 'end')
        self.vz_frame3.delete(0, 'end')
        self.after(100, lambda: self.bar_code_home_frame3.focus_set())

    def export_to_excel_button_click(self):
        try:
            export_to_exel.export_to_excel()  # Вызываем функцию из другого файла
            threading.Thread(target=self.show_notification, args=("Done", "Tabelle erstellt")).start()
        except Exception as e:
            print("Произошла ошибка при создании файла Excel:", str(e))

    # Проверяем наличие файла Excel
        if os.path.exists("Bestand_Lager.xlsx"):
            print("Файл Excel уже существует.")
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        font = ("Arial", int(14 * new_scaling_float))
        style = ttk.Style()
        style.configure("Treeview", font=font)

    def update_ui_language(self, language):      
        # Получите словарь с текстами для выбранного языка
        texts = localizations.language_texts.get(language, {})
        
        # Обновите тексты для виджетов, кнопок, лейблов и других элементов
        self.sign.configure(text=texts.get("Road signs", "Road signs"))
        
        self.bau_frame.configure(text=texts.get("Traffic monitoring", "Traffic monitoring"))
        self.material_frame.configure(text=texts.get("Traffic safety", "Traffic safety"))
        self.log_frame.configure(text=texts.get("Logs", "Logs"))
        #     self.create_button.configure(text=texts.get("Create a construction site", "Create a construction site"))
        #     self.delete_button.configure(text=texts.get("Delete a construction site", "Delete a construction site"))
        # self.select_button.configure(text=texts.get("Choose", "Choose"))
        
        
        self.tab1_label_search.configure(text=texts.get("Search", "Search"))
        self.plus_to_table.configure(text = texts.get("Add", "Add"))
        self.minus_to_table.configure(text = texts.get("Decrease", "Decrease"))
        self.zamena_to_table.configure(text = texts.get("Replace", "Replace"))
        self.apply.configure(text = texts.get("Apply", "Apply"))
        
        # self.tab2_label_Add.configure(text=texts.get("Add", "Add"))

        selected_language = language
        self.save_language_to_file(selected_language)

    def show_img_for_barcode(self, barcode):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT VZ_Nr FROM lager_bestand WHERE Bar_Code = %s", (barcode,))
        data= cursor.fetchone()
        
        if data is not None:
            vznr = data[0]
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .png

            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует

                self.image_label = CTk.CTkLabel(self.home_frame2, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=0, pady=0, sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}

    def show_img_for_bedeutung(self, vz):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT VZ_Nr FROM lager_bestand WHERE VZ_Nr = %s", (vz,))
        data= cursor.fetchone()
        
        if data is not None:
            vznr = data[0]
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .png

            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует

                self.image_label = CTk.CTkLabel(self.home_frame2, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=0, pady=0, sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}

    def show_img_for_vz(self, vz):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT VZ_Nr FROM Lager_Bestand WHERE VZ_Nr = %s", (vz,))
        data = cursor.fetchone()

        if data is not None:
            vznr = data[0]
            image_path = f"VZ_DB/{vznr}.jpg"  # Предполагаем, что все изображения имеют расширение .png

            try:
                image = PIL.Image.open(image_path)
                ctk_image = CTk.CTkImage(image, size=(200,200))
                # Создайте виджет для отображения изображения
                if hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует

                self.image_label = CTk.CTkLabel(self.home_frame2, image=ctk_image, text="")
                self.image_label.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}")

    def check_values(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()

        # Получаем все строки из базы данных
        cursor.execute("SELECT * FROM Lager_Bestand")
        results = cursor.fetchall()

        for result in results:
            bestand_lager = result[0]  # Замените индексы на те, которые соответствуют вашей структуре таблицы
            aktueller_bestand = result[1]  # Замените индексы на те, которые соответствуют вашей структуре таблицы

            # Сравниваем значения и обновляем, если необходимо
            if aktueller_bestand > bestand_lager:
                # Обновляем aktueller_bestand на значение bestand_lager
                cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bestand_lager = %s", (bestand_lager, bestand_lager))
    
    def kol2(self):
        self.barcode = self.bar_code.get()
        self.vz = self.vz_nr.get()
        bedeutung = self.bedeutung.get()
        if bedeutung:
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            # Получаем данные из базы данных (замените на ваш SQL-запрос)
            cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = %s OR VZ_Nr = %s OR LOWER(bedeutung) ILIKE LOWER(%s)", (self.barcode, self.vz,  f"%{bedeutung}%"))
            data = cursor.fetchall()
        else:
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            # Получаем данные из базы данных (замените на ваш SQL-запрос)
            cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = %s OR VZ_Nr = %s", (self.barcode, self.vz))
            data = cursor.fetchall()
    
        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)

        if data:
            for item in data:
                # Добавляем новые строки с данными в таблицу
                self.show_img_for_barcode(self.bar_code.get())
                self.show_img_for_vz(self.vz_nr.get())
                if len(data) == 1:
                    # Выполняем определенное действие только для одного товара
                    self.show_img_for_bedeutung(item[1])
                elif self.error_label:
                    self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было
                elif hasattr(self, "image_label"):
                    self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
                self.table.insert("", "end", values=item)
        elif self.barcode == "" and self.vz == "" and bedeutung == "":
            self.result_show("Забыл ввести данные")
        else:
            self.result_show("Данных не найдено")
        self.bar_code.delete(0, 'end')
        self.vz_nr.delete(0, 'end')
        self.bedeutung.delete(0, 'end')
         
    def check_bedeutung(self,event):
        # Функция вызывается при изменении баркода
        if self.bedeutung.get(): 
            # Если баркод не пустой, очищаем поле Vz Nr
            self.vz_nr.delete(0, 'end')
            self.bar_code.delete(0, 'end')

    def check_vz_nr(self, event):
        # Функция вызывается при изменении баркода
        if self.bar_code.get():
            # Если баркод не пустой, очищаем поле Vz Nr
            self.vz_nr.delete(0, 'end')
            self.bedeutung.delete(0, 'end')
        
    def check_barcode(self, event):
        # Функция вызывается при изменении Vz Nr
        if self.vz_nr.get():
            # Если Vz Nr не пустой, очищаем поле баркода
            self.bar_code.delete(0, 'end')
            self.bedeutung.delete(0, 'end')

    def show_werkzeug_table(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("SELECT Bar_Code, Bedeutung,Größe, Bestand_Lager, Aktueller_bestand FROM werkzeug_lager")
        data = cursor.fetchall()
        for row in self.werkzeug_table.get_children():
            self.werkzeug_table.delete(row)
       
        for item in data:
            self.werkzeug_table.insert("", "end", values=item)

    def show_material_table(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        
        # Получаем все записи из таблицы "Lager_Bestand"
        cursor.execute("SELECT Bar_Code, Bedeutung,Größe, Bestand_Lager, Aktueller_bestand FROM material_lager")
        data = cursor.fetchall()
        
        # Очищаем текущие строки в таблице
        for row in self.material_table.get_children():
            self.material_table.delete(row)
        # if hasattr(self, "image_label"):
        #         self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        # if self.error_label:
        #     self.error_label.destroy()
        # Вставляем данные в таблицу
        for item in data:
            self.material_table.insert("", "end", values=item)

    def show_all_data(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        
        # Получаем все записи из таблицы "Lager_Bestand"
        # Выполните SQL-запрос с сортировкой по столбцу vz_nr
        cursor.execute("SELECT * FROM lager_bestand ORDER BY CAST(SUBSTRING(vz_nr FROM '^[0-9]+') AS INTEGER), CAST(SUBSTRING(vz_nr FROM '[0-9]+$') AS INTEGER)")

        data= cursor.fetchall()
        # Очищаем текущие строки в таблице
        for row in self.table.get_children():
            self.table.delete(row)
        if hasattr(self, "image_label"):
                self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        if self.error_label:
            self.error_label.destroy()
        # Вставляем данные в таблицу
        for item in data:
            self.table.insert("", "end", values=item)
        

        for row in self.table_for_editing.get_children():
            self.table_for_editing.delete(row)
        if hasattr(self, "image_label"):
                self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        if self.error_label:
            self.error_label.destroy()
        # Вставляем данные в таблицу
        for item in data:
            self.table_for_editing.insert("", "end", values=item)

    def select_frame_by_name(self, name):
        # Ставим цвет для активной кнопки
        self.sign.configure(fg_color=("red") if name == "home" else "transparent")
        
        self.material_frame.configure(fg_color=("red") if name == "Traffic safety" else "transparent")
        self.bau_frame.configure(fg_color=("red") if name == "Traffic monitoring" else "transparent")
        self.log_frame.configure(fg_color=("red") if name == "Logs" else "transparent")

        # Показываем включенный фрейм
        if name == "home":
            self.f1.grid(row=0, column=1, sticky="nsew")
        else:
            self.f1.grid_forget()
        if name == "Traffic safety":
            self.f2.grid(row=0, column=1, sticky="nsew")
        else:
            self.f2.grid_forget()
        if name == "Traffic monitoring":
            self.f3.grid(row=0, column=1, sticky="nsew")
        else:
            self.f3.grid_forget()
        if name == "Logs":
            self.f4.grid(row=0, column=1, sticky="nsew")
            self.show_logs()
        else:
            self.f4.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def material_button_event(self):
        self.select_frame_by_name("Traffic safety")

    def bau_button_event(self):
        self.select_frame_by_name("Traffic monitoring")

    def log_button_event(self):
        self.select_frame_by_name("Logs")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

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

                self.image_label = CTk.CTkLabel(self.tabview.tab("View"), image=ctk_image, text="")
                self.image_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 0), sticky="ne")
            except FileNotFoundError:
                self.result_show("Изображение не найдено")
            except Exception as e:
                print(f"Ошибка открытия изображения: {e}") # показывает какая ошибка в консоль! {e}

    def result_show(self, message):
        if self.error_label:
            self.error_label.destroy()  # Удаляем предыдущее сообщение об ошибке, если оно уже было
        if hasattr(self, "image_label"):
                self.image_label.destroy()  # Удаляем предыдущий виджет, если он существует
        self.error_label = CTk.CTkLabel(self.home_frame2, font=('<Arial>', 20)  , bg_color="transparent", text=message, text_color="gray")
        self.error_label.grid( row=0, column=0, padx=0, pady=0, sticky="ne")
        
    def exit (self):
        self.destroy()  # Сворачиваем окно
        new_window = Autorisation.App()
        new_window.mainloop()  # Запускаем главный цикл нового окна
   
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
    
    def on_log_select(self, event):
        # Получаем выделенную запись
        selected_item = self.log_table.selection()
        self.status_bau_do.set("")
        self.kostenstelle_vvo_do.delete(0,'end')
        self.kostenstelle_vvo_do.configure(placeholder_text = "Kostenstelle VVO")
        self.kostenstelle_plannung_nr_do.delete(0,'end')
        self.kostenstelle_plannung_nr_do.configure(placeholder_text = "Kostenstelle planung")
        self.bauvorhaben_do.delete(0,'end')
        self.bauvorhaben_do.configure(placeholder_text = "Bauvorhaben")
        self.ansprechpartner_do.delete(0,'end')
        self.ansprechpartner_do.configure(placeholder_text = "Ansprechpartner")
        self.ort_do.delete(0,'end')
        self.ort_do.configure(placeholder_text = "Ort")
        self.strasse_do.delete(0,'end')
        self.strasse_do.configure(placeholder_text = "Strasse")
        self.ausfurung_von_do.delete(0,'end')
        self.ausfurung_bis_do.delete(0,'end')
        self.umbau_datum_do.delete(0,'end')
        self.check_umbau_do.deselect()
        self.uber_do.deselect()

        self.status_bau_posle.set("")
        self.kostenstelle_vvo_posle.delete(0,'end')
        self.kostenstelle_vvo_posle.configure(placeholder_text = "Kostenstelle VVO")
        self.kostenstelle_plannung_nr_posle.delete(0,'end')
        self.kostenstelle_plannung_nr_posle.configure(placeholder_text = "Kostenstelle planung")
        self.bauvorhaben_posle.delete(0,'end')
        self.bauvorhaben_posle.configure(placeholder_text = "Bauvorhaben")
        self.ansprechpartner_posle.delete(0,'end')
        self.ansprechpartner_posle.configure(placeholder_text = "Ansprechpartner")
        self.ort_posle.delete(0,'end')
        self.ort_posle.configure(placeholder_text = "Ort")
        self.strasse_posle.delete(0,'end')
        self.strasse_posle.configure(placeholder_text = "Strasse")
        self.ausfurung_von_posle.delete(0,'end')
        self.ausfurung_bis_posle.delete(0,'end')
        self.umbau_datum_posle.delete(0,'end')
        self.check_umbau_posle.deselect()
        self.uber_posle.deselect()
        
        if selected_item:
            item_values = self.log_table.item(selected_item, "values")[0]
            print(item_values)
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM app_logs WHERE log_id = %s", (item_values,))
            data = cursor.fetchone()
            print(data)
            if data[6] != None:
                self.status_bau_do.set(data[6])
            if data[8] != None:
                self.kostenstelle_vvo_do.insert(0, data[8])
            if data[10] != None:
                self.kostenstelle_plannung_nr_do.insert(0, data[10])
            if data[12] != None:
                self.bauvorhaben_do.insert(0, data[12])
            if data[14] != None:
                self.ansprechpartner_do.insert(0, data[14])
            if data[16] != None:
                self.ort_do.insert(0, data[16])
            if data[18] != None:
                self.strasse_do.insert(0, data[18])
            if data[20] != None:
                self.ausfurung_von_do.set_date(data[20])
            if data[22] != None:
                self.ausfurung_bis_do.set_date(data[22])
            if data[24] != None:
                if data[24] == "1":
                    self.check_umbau_do.select()
                else:
                    self.check_umbau_do.deselect()
            if data[26] != None:
                self.umbau_datum_do.set_date(data[26])
            if data[28] != None:
                if data[28] == "1":
                    self.uber_do.select()
                else:
                    self.uber_do.deselect()
            
            if data[7] != None:
                self.status_bau_posle.set(data[7])
            if data[9] != None:
                self.kostenstelle_vvo_posle.insert(0, data[9])
            if data[11] != None:
                self.kostenstelle_plannung_nr_posle.insert(0, data[11])
            if data[13] != None:
                self.bauvorhaben_posle.insert(0, data[13])
            if data[15] != None:
                self.ansprechpartner_posle.insert(0, data[15])
            if data[17] != None:
                self.ort_posle.insert(0, data[17])
            if data[19] != None:
                self.strasse_posle.insert(0, data[19])
            if data[21] != None:
                self.ausfurung_von_posle.set_date(data[21])
            if data[23] != None:
                self.ausfurung_bis_posle.set_date(data[23])
            if data[25] != None:
                if data[25] == "1":
                    self.check_umbau_posle.select()
                else:
                    self.check_umbau_posle.deselect()
            if data[27] != None:
                self.umbau_datum_posle.set_date(data[27])
            if data[29] != None:
                if data[29] == "1":
                    self.uber_posle.select()
                else:
                    self.uber_posle.deselect()
  

    def create_log_frames(self):
        self.status_bau_do = customtkinter.CTkOptionMenu(self.log_left, values=["Aktiv","Inaktiv", "Abgeschlossen"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau_do.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")
        
        self.kostenstelle_vvo_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo_do.grid(column= 0, row=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.kostenstelle_plannung_nr_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Kostenstelle planung:", width= 250, corner_radius = 3)
        self.kostenstelle_plannung_nr_do.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bauvorhaben_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben_do.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ansprechpartner_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner_do.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort_do.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse_do = customtkinter.CTkEntry(self.log_left, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse_do.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label_do = customtkinter.CTkLabel(self.log_left, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label_do.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von_do = DateEntry(self.log_left, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von_do.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label_do = customtkinter.CTkLabel(self.log_left, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label_do.grid(row=10, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis_do = DateEntry(self.log_left, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis_do.grid(column= 0, row=10, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.umbau_datum_label_do = customtkinter.CTkLabel(self.log_left, text="Umbau:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.umbau_datum_label_do.grid(column=0, row=11, padx=10, pady=(0,10), sticky = "nw")

        check_var_do = customtkinter.StringVar(value="off")
        self.check_umbau_do = customtkinter.CTkCheckBox(self.log_left,variable=check_var_do, text="",width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red", onvalue="1", offvalue="0")
        self.check_umbau_do.grid(column=0, row=11, padx=(10, 100), pady=(0,10), sticky = "ne")

        self.umbau_datum_do = DateEntry(self.log_left, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.umbau_datum_do.grid(column= 0, row=11, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.uber_do = customtkinter.CTkSwitch(self.log_left, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber_do.grid(column = 0, row = 12, padx=(10, 10), pady=(0, 10), sticky="nw")


        next_image = customtkinter.CTkLabel(self.log_center, image=self.image_next, text="")
        next_image.pack(padx=10, pady=10, expand=True)

        self.status_bau_posle = customtkinter.CTkOptionMenu(self.log_right, values=["Aktiv","Inaktiv", "Abgeschlossen"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau_posle.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")
        
        self.kostenstelle_vvo_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo_posle.grid(column= 0, row=2, padx=(10, 10), pady=(10, 10), sticky="nw")

        

        # self.kostenstelle_plannung_var = StringVar()

        # self.kostenstelle_plannung_button = customtkinter.CTkButton(self.log_left, text="VZP ordner auswählen", 
        #                                                             command=self.choose_folder, width=250,
        #                                                             fg_color=("gray70", "gray30"), corner_radius=2, 
        #                                                             text_color=("gray10", "gray90"), hover_color=("red"),
        #                                                             font=customtkinter.CTkFont(size=14, weight="bold"),
        #                                                             anchor="center")
        # self.kostenstelle_plannung_button.grid(column=0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.kostenstelle_plannung_nr_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Kostenstelle planung:", width= 250, corner_radius = 3)
        self.kostenstelle_plannung_nr_posle.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bauvorhaben_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben_posle.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ansprechpartner_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner_posle.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort_posle.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse_posle = customtkinter.CTkEntry(self.log_right, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse_posle.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label_posle = customtkinter.CTkLabel(self.log_right, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label_posle.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von_posle = DateEntry(self.log_right, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von_posle.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label_posle = customtkinter.CTkLabel(self.log_right, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label_posle.grid(row=10, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis_posle = DateEntry(self.log_right, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis_posle.grid(column= 0, row=10, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.umbau_datum_label_posle = customtkinter.CTkLabel(self.log_right, text="Umbau:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.umbau_datum_label_posle.grid(column=0, row=11, padx=10, pady=(0,10), sticky = "nw")

        check_var_posle = customtkinter.StringVar(value="off")
        self.check_umbau_posle = customtkinter.CTkCheckBox(self.log_right, variable=check_var_posle, text="",width = 0, checkbox_height = 20, checkbox_width = 20, corner_radius=1, border_width = 2, hover_color = "red", fg_color = "red", onvalue="1", offvalue="0")
        self.check_umbau_posle.grid(column=0, row=11, padx=(10, 100), pady=(0,10), sticky = "ne")

        self.umbau_datum_posle = DateEntry(self.log_right, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.umbau_datum_posle.grid(column= 0, row=11, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.uber_posle = customtkinter.CTkSwitch(self.log_right, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber_posle.grid(column = 0, row = 12, padx=(10, 10), pady=(0, 10), sticky="nw")


    def show_logs(self):
        self.check_connection_with_thread()
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS app_logs (log_id SERIAL PRIMARY KEY, log_time TIMESTAMP, log_user VARCHAR(255), log_action VARCHAR(255));")
        
        try:
            cursor.execute("SELECT log_id, log_time, log_user, log_action, kostenstelle, bauvorhaben FROM app_logs ORDER BY log_time DESC")
            log_entries = cursor.fetchall()

            # Очищаем таблицу перед заполнением новыми данными
            self.clear_log_table()

            for entry in log_entries:
                log_id, log_time, log_user, log_action, log_kostenstelle, log_bauvorhaben = entry
                log_time_str = log_time.strftime("%H:%M %d.%m.%Y")
                self.log_table.insert("", "end", values=(log_id, log_time_str, log_user, log_action, log_kostenstelle, log_bauvorhaben))

        except Exception as e:
            print(f"Ошибка при чтении логов из базы данных: {e}")

    def clear_log_table(self):
        # Очищаем таблицу перед заполнением новыми данными
        for row in self.log_table.get_children():
            self.log_table.delete(row)
    def clear_logs(self):
        self.log_view.configure(state="normal")
        
        try:
            self.check_connection_with_thread()
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM app_logs")  # Этот запрос удаляет все записи из таблицы
            
            # Очистите содержимое виджета текста
            self.log_view.delete("1.0", "end")
            
            self.logger.info("Логи очищены")
        except Exception as e:
            print(f"Ошибка при удалении логов из базы данных: {e}")

        self.log_view.configure(state="disabled")

    def info(self):
        import info_top_level
        info_window = info_top_level.App()
        info_window.grab_set()  # захватываем фокус
        info_window.wait_window()  # ждем закрытия дочернего окна
        info_window.grab_release()  # освобождаем фокус после его закрытия

    def check_connection(self):
        try:
            if self.conn is None or self.conn.closed != 0:
                # Если соединения нет или оно закрыто, создаем новое соединение
                self.conn = regbase.create_conn()
                print("соединение повторно создано")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def check_connection_periodically(self):
        threading.Thread(target=self.reload_regbase).start()
        print("Время пошло")
        self.after(300000, self.check_connection_periodically)  # Запуск следующей проверки через 5 минут
    
    def reload_regbase(self):
        self.conn = regbase.create_conn()
        print("произошло подключение")

    def check_connection_with_thread(self):
        threading.Thread(target=self.check_connection).start()

if __name__ == '__main__':
    
    app = BestandLager()
    conn = regbase.create_conn()
    app.mainloop()