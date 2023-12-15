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






customtkinter.set_appearance_mode("dark")

class BestandLager(CTk.CTk):
    def __init__(self,login, role, conn): # После теста добавить аргумент login и role  не забыть убрать комментарий ниже!!!!
        super().__init__()
         # Настройки логирования
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Создайте объект логгера для вашего класса или модуля
        self.logger = logging.getLogger(__name__)
        self.role = role # Для полного функционала изменить 1 на role
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
        if self.role == "1":
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
        else:
            pass
        
        
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
        if self.role == "1":
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
        self.select_frame_by_name("home")



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
        if self.role == "1":
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

        self.tabview_baustellen.tab("Bearbeitung").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Bearbeitung").grid_rowconfigure(2, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_rowconfigure(1, weight=1)

        self.tabview_baustellen.configure(segmented_button_selected_color="red")

        self.bau_frame1 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame1.grid(row=0, column=0, padx=(10,10),pady=(0,10), sticky="nsew")
        self.bau_frame1.grid_columnconfigure(0, weight=1)
        
        self.bau_frame2 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2.grid(row=1, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame2.grid_columnconfigure(0, weight=1)
        
        self.bau_frame2_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2_2.grid(row=2, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame2_2.grid_columnconfigure(0, weight=1)
        
        
        self.bau_frame3 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3.grid(row=0, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame3.grid_columnconfigure(0, weight=1)
        self.bau_frame3_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3_2.grid(row=1, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame3_2.grid_columnconfigure(0, weight=1)
       

############################



        
        
############## ############## ############## ############## #Настройка фрейма №3 ############## ############## ############## ############## ##############        
        
        
############## ############## ############## ############## #Настройка фрейма №4 ############## ############## ############## ############## ############## 
        self.log_view = customtkinter.CTkTextbox(master=self.f4, width=400, corner_radius=3)
        self.log_view.grid(row=0, column=0, padx=(5,5), pady=(5,0), sticky="nsew")
        self.clear_log_button = customtkinter.CTkButton(self.f4,  corner_radius=2, height=30, width=250, border_spacing=5,
                                                fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
                                                font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center", text="Clear logs", command=self.clear_logs)
        self.clear_log_button.grid(row=1, column=0, pady=5, sticky="nsew")








############## ############## ############## ############## #Настройка фрейма №5 ############## ############## ############## ############## ##############         




    
        self.bedeutung.bind("<KeyRelease>", self.check_bedeutung)
        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
        self.bedeutung.bind('<Return>', lambda event=None: self.kol2())
        # self.bar_code_f2.bind('<Return>', lambda event=None: self.add_button_bau())
        # self.sum.bind('<Return>', lambda event=None: self.add_button_bau())
        self.sum_home_frame3.bind('<Return>', lambda event=None: self.reduction_main_table())
        self.update_ui_language(self.language)
        self.update()

        
        self.login = login
        self.barcode = None
        self.error_label= None

        
        self.show_logs()
        self.show_all_data()
        self.show_material_table()
        self.show_werkzeug_table()
        self.display_existing_products()
        self.create_labels()

    def create_labels(self):
        diese_woche = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Diese Woche", width= 150, fg_color="#CE5145")
        diese_woche.pack(side='left', padx=(10,5), anchor="nw")
        nachste_woche = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Nächste Woche",width= 150, fg_color="#998711", text_color = "black")
        nachste_woche.pack(side='left', padx=5, anchor="nw")
        heute = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Heute",width= 150, fg_color="#8c0303")
        heute.pack(side='left', padx=5, anchor="nw")
        bei_der_arbeit = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="Wird Uberwacht",width= 150, fg_color="#66B032",text_color = "black")
        bei_der_arbeit.pack(side='left', padx=5, anchor="nw")
        h_verbot_color = customtkinter.CTkLabel(self.bau_frame1, font=customtkinter.CTkFont(size=15, weight="bold") , text="H.Verbot",width= 150, fg_color="#4424D6",text_color = "white")
        h_verbot_color.pack(side='left', padx=5, anchor="nw")

        
        label8 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="NAME", width= 150, fg_color="#0f5925")
        label8.pack(side='left', padx=(10,5), anchor="nw")
        label = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN", width= 150, fg_color="#0f5925")
        label.pack(side='left', padx=5, anchor="nw")
        label2 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE",width= 150, fg_color="#0f5925")
        label2.pack(side='left', padx=5, anchor="nw")
        label3 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="ANSPRECHPARTNER",width= 180, fg_color="#0f5925")
        label3.pack(side='left', padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="VZP",width= 100, fg_color="#0f5925")
        label4.pack(side='left', padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSF, H.VERBOT",width= 180, fg_color="#0f5925")
        label5.pack(side='left', padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFURUNG VOM",width= 150, fg_color="#0f5925")
        label6.pack(side='left', padx=5, anchor="nw")
        label7 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSF. BIS/VRAO ENDE",width= 180, fg_color="#0f5925")
        label7.pack(side='left', padx=5, anchor="nw")
        

        image_add = customtkinter.CTkImage(light_image=Image.open("images/add_btn.png"),
                                  dark_image=Image.open("images/add_btn.png"),
                                  size=(20, 20))
        add_btn = customtkinter.CTkButton(self.bau_frame2,image=image_add, text="", command=self.open_add_bau_menu_toplevel, corner_radius=2, height=20, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"),
                                                anchor="center" )
        add_btn.pack(side='left', padx=5, anchor="nw")
        
        inaktiv_label = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="NAME", width= 150, fg_color="#0f5925")
        inaktiv_label.pack(side='left', padx=(10,5), anchor="nw")
        inaktiv_label2 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN",width= 150, fg_color="#0f5925")
        inaktiv_label2.pack(side='left', padx=5, anchor="nw")
        inaktiv_label3 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE",width= 150, fg_color="#0f5925")
        inaktiv_label3.pack(side='left', padx=5, anchor="nw")
        inaktiv_label4 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="ANSPRECHPARTNER",width= 180, fg_color="#0f5925")
        inaktiv_label4.pack(side='left', padx=5, anchor="nw")
        inaktiv_label5 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="VZP",width= 100, fg_color="#0f5925")
        inaktiv_label5.pack(side='left', padx=5, anchor="nw")
        inaktiv_label7 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSFURUNG VOM",width= 150, fg_color="#0f5925")
        inaktiv_label7.pack(side='left', padx=5, anchor="nw")
        inaktiv_label8 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"AUSF. BIS/VRAO ENDE",width= 180, fg_color="#0f5925")
        inaktiv_label8.pack(side='left', padx=5, anchor="nw")

    def days_until_due(self, product):
        current_date = datetime.now().date()
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days
        return days_until_due

    def display_existing_products(self):
        products = self.get_products_from_database()
        # Разделяем товары на два списка: те, чья дата уже прошла, и те, чья дата еще предстоит
        past_due_products = [product for product in products if self.days_until_due(product) < 0]
        future_products = [product for product in products if self.days_until_due(product) >= 0]
        # Сортируем товары, у которых дата еще предстоит
        sorted_future_products = sorted(future_products, key=self.days_until_due)
        for product in sorted_future_products:
            self.create_product_frame(product)
        # Создаем фреймы для товаров, у которых дата уже прошла
        for product in past_due_products:
            self.create_product_frame(product)

        inaktiv_products = self.get_inaktiv_from_database()
        for inaktiv_product in inaktiv_products:
            self.create_inaktiv_frame(inaktiv_product)

    def get_inaktiv_from_database(self, status = 'Inaktiv'):
        # Открываете курсор для выполнения SQL-запроса
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
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status, set_capo, kostenstelle_plannung FROM Bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'ansprechpartner': product_tuple[8],
                            'status': product_tuple[9], 'set_capo': product_tuple[10],'kostenstelle_plannung': product_tuple[11] }
            product_dicts.append(product_dict)

        return product_dicts
    
    def create_inaktiv_frame(self, inaktiv_product):
        self.inaktiv_frame = customtkinter.CTkFrame(self.bau_frame3_2)
        self.inaktiv_frame.pack(fill='x', pady=5, anchor="nw")
        # Создаем поле с данными о товаре
        label1_text = inaktiv_product['name'][:15] + "..." if len(inaktiv_product['name']) > 15 else inaktiv_product['name']
        label1 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label1_text, width= 150)
        label1.pack(side='left', padx=5, anchor="nw")
        CTkToolTip(label1, message=f"{inaktiv_product['name']}")

        label2 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['bauvorhaben']}", width= 150)
        label2.pack(side='left', padx=5, anchor="nw")
        kostenstelle_btn = customtkinter.CTkButton(self.inaktiv_frame, text=f"{inaktiv_product['kostenstelle']}", command=lambda p=inaktiv_product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=1, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=5, padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ansprechpartner']}",width= 180)
        label4.pack(side='left', padx=5, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.inaktiv_frame, text="VZP", command=lambda p=inaktiv_product['kostenstelle_plannung']: self.open_vzp_folder(p),corner_radius=2, height=28, width=100, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left',pady=5, padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_von']}",width= 150)
        label5.pack(side='left', padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_bis']}",width= 180)
        label6.pack(side='left', padx=5, anchor="nw")


        image_reduction = customtkinter.CTkImage(light_image=Image.open("images/reduction.png"),
                                  dark_image=Image.open("images/reduction.png"),
                                  size=(20, 20))
        reduction_btn = customtkinter.CTkButton(self.inaktiv_frame,image=image_reduction, text="", command=lambda p=inaktiv_product['id']: self.open_reduction_menu(p),corner_radius=2, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left',pady=5, padx=5, anchor="nw")

        photo_image = customtkinter.CTkImage(light_image=Image.open("images/photo.png"),
                                  dark_image=Image.open("images/photo.png"),
                                  size=(20, 20))
        photo_button = customtkinter.CTkButton(self.inaktiv_frame,image=photo_image, text="", command=lambda p=inaktiv_product['kostenstelle']: self.open_photo_menu(p),corner_radius=2, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left',pady=5, padx=5, anchor="nw")

        image_set_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"),
                                  dark_image=Image.open("images/capo.png"),
                                  size=(20, 20))
        set_capo = customtkinter.CTkButton(self.inaktiv_frame, image=image_set_capo, text="", command=lambda p=inaktiv_product['id']: self.set_capo_top_level(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left',pady=5, padx=5, anchor="nw")
        
        image_stunden = customtkinter.CTkImage(light_image=Image.open("images/clock.png"),
                                  dark_image=Image.open("images/clock.png"),
                                  size=(20, 20))
        stunden = customtkinter.CTkButton(self.inaktiv_frame, image=image_stunden, text="", command=lambda p=inaktiv_product['kostenstelle']: self.stunden_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left',pady=5, padx=5, anchor="nw")

        image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        material = customtkinter.CTkButton(self.inaktiv_frame, image=image_material, text="", command=lambda p=inaktiv_product['kostenstelle']: self.material_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left',pady=5, padx=5, anchor="nw")

        image_return = customtkinter.CTkImage(light_image=Image.open("images/return.png"),
                                  dark_image=Image.open("images/return.png"),
                                  size=(20, 20))
        activate_button = customtkinter.CTkButton(self.inaktiv_frame, image=image_return, text="", command=lambda p=inaktiv_product['id']: self.activate_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        activate_button.pack(side='left', padx=5, anchor="nw")
        
    def create_product_frame(self, product):
        self.product_frame = customtkinter.CTkFrame(self.bau_frame2_2, fg_color="transparent")
        self.product_frame.pack(fill='x', pady=2, anchor="nw")

        current_date = datetime.now().date()    #18.12.23
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        days_until_due = (product_date - current_date).days

        new_date = product_date - timedelta(days=6) #12.12.2023
        h_verbot=new_date.strftime('%d.%m.%Y')      #12.12.2023

            # Создаем поле с данными о товаре
        label2_text = product['name'][:15] + "..." if len(product['name']) > 15 else product['name']
        label2 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=label2_text, width= 150)
        label2.pack(side='left',pady=5, padx=5, anchor="nw")
        CTkToolTip(label2, message=f"{product['name']}")
        label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['bauvorhaben']}", width= 150)
        label.pack(side='left',pady=5, padx=5, anchor="nw")
        kostenstelle_btn = customtkinter.CTkButton(self.product_frame, text=f"{product['kostenstelle']}", command=lambda p=product['kostenstelle']: self.open_kostenstelle_folder(p),corner_radius=1, height=28, width=150, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        kostenstelle_btn.pack(side='left',pady=5, padx=5, anchor="nw")
        label3 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ansprechpartner']}",width= 180)
        label3.pack(side='left',pady=5, padx=5, anchor="nw")
        vzp_btn = customtkinter.CTkButton(self.product_frame, text="VZP", command=lambda p=product['kostenstelle_plannung']: self.open_vzp_folder(p),corner_radius=2, height=28, width=100, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        vzp_btn.pack(side='left',pady=5, padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold"), text=h_verbot, width=180)
        label4.pack(side='left',pady=5, padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_von']}",width= 150)
        label5.pack(side='left',pady=5, padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_bis']}",width= 180)
        label6.pack(side='left',pady=5, padx=5, anchor="nw")


        image_reduction = customtkinter.CTkImage(light_image=Image.open("images/reduction.png"),
                                  dark_image=Image.open("images/reduction.png"),
                                  size=(20, 20))
        reduction_btn = customtkinter.CTkButton(self.product_frame,image=image_reduction, text="", command=lambda p=product['id']: self.open_reduction_menu(p),corner_radius=2, height=15, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left',pady=5, padx=5, anchor="nw")

        photo_image = customtkinter.CTkImage(light_image=Image.open("images/photo.png"),
                                  dark_image=Image.open("images/photo.png"),
                                  size=(20, 20))
        photo_button = customtkinter.CTkButton(self.product_frame,image=photo_image, text="", command=lambda p=product['kostenstelle']: self.open_photo_menu(p),corner_radius=2, height=20, width=50,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left',pady=5, padx=5, anchor="nw")

        image_set_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"),
                                  dark_image=Image.open("images/capo.png"),
                                  size=(20, 20))
        set_capo = customtkinter.CTkButton(self.product_frame, image=image_set_capo, text="", command=lambda p=product['id']: self.set_capo_top_level(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left',pady=5, padx=5, anchor="nw")
        
        image_stunden = customtkinter.CTkImage(light_image=Image.open("images/clock.png"),
                                  dark_image=Image.open("images/clock.png"),
                                  size=(20, 20))
        stunden = customtkinter.CTkButton(self.product_frame, image=image_stunden, text="", command=lambda p=product['kostenstelle']: self.stunden_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left',pady=5, padx=5, anchor="nw")

        image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        material = customtkinter.CTkButton(self.product_frame, image=image_material, text="", command=lambda p=product['kostenstelle']: self.material_bau(p),corner_radius=2, height=20, width=50, 
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left',pady=5, padx=5, anchor="nw")

        image_delete = customtkinter.CTkImage(light_image=Image.open("images/delete.png"),
                                  dark_image=Image.open("images/delete.png"),
                                  size=(20, 20))
        deactive_button = customtkinter.CTkButton(self.product_frame, image=image_delete, text="", command=lambda p=product['id']: self.deactive_bau(p),corner_radius=2, height=20, width=50, 
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        deactive_button.pack(side='left',pady=5, padx=5, anchor="nw")
        
        
        #Если остается 7 дней или менее до даты, устанавливаем красный цвет
        if 1 <= days_until_due <= 7:
            label.configure(fg_color="#CE5145",text_color = "black")
            label2.configure(fg_color="#CE5145",text_color = "black")
            kostenstelle_btn.configure(fg_color="#CE5145",text_color = "black")
            label3.configure(fg_color="#CE5145",text_color = "black")
            label4.configure(fg_color="#CE5145",text_color = "black")
            label5.configure(fg_color="#CE5145",text_color = "black")
            label6.configure(fg_color="#CE5145",text_color = "black")
            vzp_btn.configure(fg_color="#CE5145",text_color = "black")

        
        elif days_until_due == 0:
            label.configure(fg_color="#8c0303")
            label2.configure(fg_color="#8c0303")
            kostenstelle_btn.configure(fg_color="#8c0303")
            label3.configure(fg_color="#8c0303")
            label4.configure(fg_color="#8c0303")
            label5.configure(fg_color="#8c0303")
            label6.configure(fg_color="#8c0303")
            vzp_btn.configure(fg_color="#8c0303")
        
        elif 8 <= days_until_due <= 14:
            label.configure(fg_color="#998711", text_color = "black")
            label2.configure(fg_color="#998711", text_color = "black")
            kostenstelle_btn.configure(fg_color="#998711", text_color = "black")
            label3.configure(fg_color="#998711", text_color = "black")
            label4.configure(fg_color="#998711", text_color = "black")
            label5.configure(fg_color="#998711", text_color = "black")
            label6.configure(fg_color="#998711", text_color = "black")
            vzp_btn.configure(fg_color="#998711", text_color = "black")

        elif product_date < current_date:
            # Если время прошло, устанавливаем синий цвет
            label.configure(fg_color="#66B032",text_color = "black")
            label2.configure(fg_color="#66B032",text_color = "black")
            kostenstelle_btn.configure(fg_color="#66B032",text_color = "black")
            label3.configure(fg_color="#66B032",text_color = "black")
            label4.configure(fg_color="#66B032",text_color = "black")
            label5.configure(fg_color="#66B032",text_color = "black")
            label6.configure(fg_color="#66B032",text_color = "black")
            vzp_btn.configure(fg_color="#66B032",text_color = "black")
    
        if not product['set_capo'] =="":
            set_capo.configure(fg_color="#bec1c4")

        if 0 <= (new_date - current_date).days <= 6:
            label4.configure(fg_color = "#4424D6", text_color = "white")
            # self.flag = True
            # threading.Thread(target=lambda: self.flash_error_color(self.product_frame), args=()).start()


    def open_kostenstelle_folder(self, product_id):
        # base_path = r"test_folder\02 Verkehrssicherung"
        base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        items = os.listdir(os.path.normpath(base_path))
        matching_folders = [folder for folder in items if product_id.lower() in folder.lower()]
        if matching_folders:
            target_folder = os.path.join(base_path, matching_folders[0])
            os.startfile(target_folder)
   
    def open_vzp_folder(self, product_id):
        base_path = r"\\FILESRV1\Abteilungen\VVO\2024\01 Verkehrsplanung"
        # base_path = r"test_folder\01 Verkehrsplanung"
        nested_folders = ["09 Verkehrszeichenpläne", "02 PDF"]
        items = os.listdir(os.path.normpath(base_path))
        matching_folders = [folder for folder in items if product_id.lower() in folder.lower()]

        if matching_folders:
            target_folder = os.path.join(base_path, matching_folders[0])
            for nested_folder in nested_folders:
                target_folder = os.path.join(target_folder, nested_folder)

            os.startfile(target_folder)
        else:
            print(f"No folders matching the keyword '{product_id}' found.")

    def open_reduction_menu(self,product_id):
        import reduction_bau_menu
        reduction_menu = reduction_bau_menu.App(self, product_id)  # создаем окно, если его нет или оно уничтожено
        reduction_menu.grab_set()  # захватываем фокус
        reduction_menu.wait_window()  # ждем закрытия дочернего окна
        reduction_menu.grab_release()  # освобождаем фокус после его закрытия
        user = self.login # имя кто сделал действие для лога
        cursor = self.conn.cursor()
        cursor.execute("SELECT kostenstelle_vvo FROM bau WHERE id = %s ",(product_id,))
        name = cursor.fetchone()
        action = f"Изменил стройку под названием: {name}" # перменная для создания названия действия лога
        self.user_action(user, action)
        self.update_product_list()

    def stunden_bau(self, product_kostenstelle):
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

                cursor = self.conn.cursor()
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status FROM bau WHERE kostenstelle_vvo = %s", (product_kostenstelle, ))
                data = cursor.fetchone()
                data_dict = {
                'C5': data[2],
                'C9': data[3],
                'C11': f"{data[5]}, {data[4]}",
                'I5': f"{data[6]} - {data[7]}",
                'I9': f"{data[6]} - {data[7]}",
                'I11': data[8],
            }
                
                # Вставляем данные в документ
                insert_data_into_excel(document_path, data_dict)

                # Открываем файл
                os.startfile(document_path)
            else:
                print(f"No folders starting with prefix '{prefix_to_match}' found inside folder '{target_folder}'.")
        else:
            print(f"No folders matching the keyword '{product_kostenstelle}' found.")

    def material_bau(self, product_kostenstelle):
        base_path = r"\\FILESRV1\Abteilungen\VVO\2024\02 Verkehrssicherung"
        # base_path = r"test_folder\02 Verkehrssicherung"
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
                # Путь к файлу "Stundenbericht Verkehrssicherung.xlsx"
                document_path = os.path.join(target_folder, nested_folder, "Materialliste.docx")

                cursor = self.conn.cursor()
                cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, ansprechpartner, status FROM bau WHERE kostenstelle_vvo = %s",(product_kostenstelle, ))
                data = cursor.fetchone()
                data_table1 = [
                    ["", data[2], "", "", f"{data[6]} - {data[7]}"],
                    ["", "", "", "", ""],
                    ["", data[3], "","",f"{data[6]} - {data[7]}"],
                    ["", f"{data[5]}, {data[4]}","","", data[8]],
                ]

                # Вставляем данные в файл Excel
                insert_data_into_tables(document_path,document_path, data_table1)

                # Открываем файл
                os.startfile(document_path)
            else:
                print(f"No folders matching the keyword '{product_kostenstelle}' found.")

    def set_capo_top_level(self,product_id):
        self.toplevel_window = Set_Capo(self, product_id)  # создаем окно, если его нет или оно уничтожено
        self.toplevel_window.grab_set()  # захватываем фокус
        self.toplevel_window.wait_window()  # ждем закрытия дочернего окна
        self.toplevel_window.grab_release()  # освобождаем фокус после его закрытия
        user = self.login # имя кто сделал действие для лога
        cursor = self.conn.cursor()
        cursor.execute("SELECT set_capo FROM bau WHERE id = %s ",(product_id,))
        name = cursor.fetchone()
        action = f"Beauftragte Personen für die Baustelle: {name}" # перменная для создания названия действия лога
        self.user_action(user, action)
        self.update_product_list()
    
    def open_add_bau_menu_toplevel(self):
        from add_bau_menu import Bau
        self.toplevel_window = Bau()  # создаем окно, если его нет или оно уничтожено
        self.toplevel_window.grab_set()  # захватываем фокус
        self.toplevel_window.wait_window()  # ждем закрытия дочернего окна
        self.toplevel_window.grab_release()  # освобождаем фокус после его закрытия
        self.update_product_list()
        cursor = self.conn.cursor()
        cursor.execute("SELECT name_bau FROM Bau ORDER BY id DESC LIMIT 1;")
        name = cursor.fetchone()
        user = self.login # имя кто сделал действие для лога
        action = f"Erstellt eine bedrohte Baustelle:: {name}" # перменная для создания названия действия лога
        self.user_action(user, action)
        
    def deactive_bau(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bau SET status = 'Inaktiv' WHERE id = %s", (product_id,))
        self.update_product_list()

    def activate_bau(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE bau SET status = 'Aktiv' WHERE id = %s", (product_id,))
        self.update_product_list()

    def update_product_list(self):
        # Очистите фреймы для активных и неактивных продуктов
        self.flag = False
        
        def update():
            for widget in self.bau_frame2_2.winfo_children():
                widget.destroy()

            for widget in self.bau_frame3_2.winfo_children():
                widget.destroy()

            self.display_existing_products()
        self.after(1000, update)
    
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
    
    # def flash_error_color(self, widget):
    #     def flash():
    #         if self.flag:
    #             widget.configure(fg_color="transparent")
    #             self.after(500, lambda: widget.configure(fg_color="#8a0707"))
    #             self.after(1000, flash)

    #     flash()

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

        print("сработало")

    def update_ui_language(self, language):      
        # Получите словарь с текстами для выбранного языка
        texts = localizations.language_texts.get(language, {})
        
        # Обновите тексты для виджетов, кнопок, лейблов и других элементов
        self.sign.configure(text=texts.get("Road signs", "Road signs"))
        if self.role == "1":
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
        
        cursor = self.conn.cursor()
        # Получаем данные из базы данных (замените на ваш SQL-запрос)
        cursor.execute("SELECT * FROM Lager_Bestand WHERE Bar_Code = %s OR VZ_Nr = %s OR LOWER(bedeutung) ILIKE LOWER(%s)", (self.barcode, self.vz,  f"%{bedeutung}%"))
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
        cursor = self.conn.cursor()
        cursor.execute("SELECT Bar_Code, Bedeutung,Größe, Bestand_Lager, Aktueller_bestand FROM werkzeug_lager")
        data = cursor.fetchall()
        for row in self.werkzeug_table.get_children():
            self.werkzeug_table.delete(row)
       
        for item in data:
            self.werkzeug_table.insert("", "end", values=item)

    def show_material_table(self):
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
        if self.role == "1":
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
   
    def show_logs(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS app_logs (log_id SERIAL PRIMARY KEY,log_time TIMESTAMP,log_user VARCHAR(255),log_action VARCHAR(255));")
    
        self.log_view.configure(state="normal")
        try:
            cursor.execute("SELECT log_time, log_user,log_action FROM app_logs ORDER BY log_time DESC")
            log_entries = cursor.fetchall()

            self.log_view.delete("1.0", "end")  # Очистить содержимое

            for entry in log_entries:
                log_time, log_user, log_action = entry
                log_text = f"{log_time} - Пользователь {log_user} выполнил действие: {log_action}\n"
                self.log_view.insert("end", log_text)

        except Exception as e:
            print(f"Ошибка при чтении логов из базы данных: {e}")

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

    def user_action(self, user, action):
        # Запись действия пользователя в лог
        
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO app_logs (log_time, log_user, log_action) VALUES (NOW(), %s, %s);",(user,action))
        self.logger.info(f"Пользователь {user} выполнил действие: {action}")
        self.show_logs()

    def clear_logs(self):
        self.log_view.configure(state="normal")
        
        try:
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

        

if __name__ == '__main__':
    
    app = BestandLager()
    conn = regbase.create_conn()
    app.mainloop()