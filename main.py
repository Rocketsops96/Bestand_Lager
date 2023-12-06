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
        self.title("Bestand Lager")
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
            

            self.bau_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Building", font=("Arial", 14, "bold"),
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
        self.tabview.tab("View").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Editing").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Material").grid_columnconfigure(0, weight=1)
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
        
        self.tab1_label_search = customtkinter.CTkLabel(self.home_frame1, text="Search", 
                                                              font=customtkinter.CTkFont(size=15, weight="bold"))
        self.tab1_label_search.grid(row=0, column=0, padx=20)

        self.bar_code = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
        self.bar_code.grid(column= 0, row=1, padx=(10, 10), pady=(5, 10), sticky="nw",)
        
        self.vz_nr = customtkinter.CTkEntry(self.home_frame1, placeholder_text="Vz Nr.:", width= 250, corner_radius = 3)
        self.vz_nr.grid(column= 0, row=2, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.btn_frame = customtkinter.CTkFrame(self.home_frame1, fg_color = "transparent")
        self.btn_frame.grid(column= 0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

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


        self.bar_code_home_frame3 = customtkinter.CTkEntry(self.home_frame3, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
        self.bar_code_home_frame3.grid(column= 1, row=0,  pady=(20, 0),padx = 10, sticky="nsew")
        

        self.sum_home_frame3 = customtkinter.CTkEntry(self.home_frame3, placeholder_text="Введите количество", width= 250, corner_radius = 3)
        self.sum_home_frame3.grid(column= 1, row=1, pady=(10, 0),padx = 10, sticky="nsew")

        self.apply = customtkinter.CTkButton(master=self.home_frame3, corner_radius=5, height=40, width=250, border_spacing=5, text="Apply",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                    anchor="center", command=self.reduction_main_table)
        self.apply.grid(column = 1,row=2, padx=10, pady=20, sticky="nw")



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
############## ############## ############## ############## #Настройка фрейма №2 ############## ############## ############## ############## ##############    
       
        self.tabview_baustellen = customtkinter.CTkTabview(self.f2)
        self.tabview_baustellen.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.tabview_baustellen.add("Bearbeitung")
        self.tabview_baustellen.add("Erstellen")
        self.tabview_baustellen.add("Inaktiv")
        
        self.tabview_baustellen.tab("Erstellen").grid_columnconfigure(0, weight=1)

        self.tabview_baustellen.tab("Bearbeitung").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Bearbeitung").grid_rowconfigure(1, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_columnconfigure(0, weight=1)
        self.tabview_baustellen.tab("Inaktiv").grid_rowconfigure(1, weight=1)

        self.tabview_baustellen.configure(segmented_button_selected_color="red")


        self.bau_frame1 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Erstellen"),fg_color="transparent")
        self.bau_frame1.grid(row=0, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame1.grid_columnconfigure(0, weight=0)
      
        self.bau_frame2 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2.grid(row=0, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame2.grid_columnconfigure(0, weight=1)
        self.bau_frame2_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Bearbeitung"),fg_color="transparent")
        self.bau_frame2_2.grid(row=1, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame2_2.grid_columnconfigure(0, weight=1)
        
        
        self.bau_frame3 = customtkinter.CTkFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3.grid(row=0, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame3.grid_columnconfigure(0, weight=1)
        self.bau_frame3_2 = customtkinter.CTkScrollableFrame(self.tabview_baustellen.tab("Inaktiv"),fg_color="transparent")
        self.bau_frame3_2.grid(row=1, column=0, padx=(10,10),pady=(10,10), sticky="nsew")
        self.bau_frame3_2.grid_columnconfigure(0, weight=1)
       
        
       
        self.status_bau = customtkinter.CTkOptionMenu(self.bau_frame1, values=["Aktiv","Inaktiv"],
                                                               fg_color="gray10", button_color="red",width= 220)
        self.status_bau.grid(row=0, column=0, padx=20, pady=(20, 0), sticky= "nw")
        
        self.name_bau = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Name:", width= 250, corner_radius = 3)
        self.name_bau.grid(column= 0, row=1, padx=(10, 10), pady=(10, 10), sticky="nw")

        self.kostenstelle_vvo = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Kostenstelle VVO:", width= 250, corner_radius = 3)
        self.kostenstelle_vvo.grid(column= 0, row=2, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.bauvorhaben = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Bauvorhaben:", width= 250, corner_radius = 3)
        self.bauvorhaben.grid(column= 0, row=3, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ort = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Ort:", width= 250, corner_radius = 3)
        self.ort.grid(column= 0, row=4, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.strasse = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Strasse:", width= 250, corner_radius = 3)
        self.strasse.grid(column= 0, row=5, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.vzp = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="VZP:", width= 250, corner_radius = 3)
        self.vzp.grid(column= 0, row=6, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.ausfurung_von_label = customtkinter.CTkLabel(self.bau_frame1, text="Ausfurung von:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_von_label.grid(row=7, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.ausfurung_von = DateEntry(self.bau_frame1, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_von.grid(column= 0, row=7, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ausfurung_bis_label = customtkinter.CTkLabel(self.bau_frame1, text="Ausfurung bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.ausfurung_bis_label.grid(row=8, column=0, padx=10, pady=(0,10), sticky = "nw")
  
        self.ausfurung_bis = DateEntry(self.bau_frame1, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.ausfurung_bis.grid(column= 0, row=8, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.vrao_ab_label = customtkinter.CTkLabel(self.bau_frame1, text="VA. ab:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.vrao_ab_label.grid(row=9, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.vrao_ab = DateEntry(self.bau_frame1, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.vrao_ab.grid(column= 0, row=9, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.vrao_bis_label = customtkinter.CTkLabel(self.bau_frame1, text="VA. bis:", 
                                                            font=customtkinter.CTkFont(size=14, weight="bold"), text_color=("white"))
        self.vrao_bis_label.grid(row=10, column=0, padx=10, pady=(0,10), sticky = "nw")

        self.vrao_bis = DateEntry(self.bau_frame1, width=12, background='grey',
                           foreground='white', borderwidth=2,date_pattern='dd.MM.yyyy')
        self.vrao_bis.grid(column= 0, row=10, padx=(10, 10), pady=(0, 10), sticky="ne")

        self.ansprechpartner = customtkinter.CTkEntry(self.bau_frame1, placeholder_text="Ansprechpartner:", width= 250, corner_radius = 3)
        self.ansprechpartner.grid(column= 0, row=11, padx=(10, 10), pady=(0, 10), sticky="nw")

        self.uber = customtkinter.CTkSwitch(self.bau_frame1, text="Uberwachung", font=customtkinter.CTkFont(size=14, weight="bold"), button_color= ("white"), progress_color = ("red"), button_hover_color = ("red"))
        self.uber.grid(column = 0, row = 12, padx=(10, 10), pady=(0, 10), sticky="nw")
        
        self.map_data = customtkinter.CTkButton(master=self.bau_frame1, corner_radius=5, height=30, width=250, border_spacing=5, text="Map",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.map)
        self.map_data.grid(column = 0,row=13, padx=(10,0), pady=(0, 10), sticky="nw")

        self.select_plan_pdf = customtkinter.CTkButton(master=self.bau_frame1, corner_radius=5, height=30, width=250, border_spacing=5, text="Open VZP...",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.select_pdf)
        self.select_plan_pdf.grid(column = 0,row=14, padx=(10,0), pady=(0, 10), sticky="nw")

        self.selcteded_pdf_files = customtkinter.CTkLabel(self.bau_frame1, text="", 
                                                            font=customtkinter.CTkFont(size=11), text_color=("gray30"))
        self.selcteded_pdf_files.grid(row=14, column=1, padx=10, pady=(0,10), sticky = "e")

        self.create_bau = customtkinter.CTkButton(master=self.bau_frame1, corner_radius=5, height=30, width=250, border_spacing=5, text="Upload",
                                                fg_color=("gray70", "gray30"), text_color=("gray10", "gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=14, weight="bold"),
                                                    anchor="center", command=self.upload_images)
        self.create_bau.grid(column = 0,row=15, padx=(10,0), pady=(0, 10), sticky="nw")


############################



        
        
############## ############## ############## ############## #Настройка фрейма №3 ############## ############## ############## ############## ##############        
        
        # self.cursor = self.conn.cursor()
        
        # self.bau_list_frame = customtkinter.CTkFrame(self.f3, fg_color="transparent")
        # self.bau_list_frame.grid(row=0, column=0, padx=(10,10),pady=(5,0), sticky="nw")
        # self.bau_list_frame.grid_columnconfigure(0, weight=1)

        # self.bau_button_frame = customtkinter.CTkFrame(self.f3, fg_color="transparent")
        # self.bau_button_frame.grid(row=1, column=0, padx=(10,10), sticky="nw")
        # self.bau_button_frame.grid_columnconfigure(1, weight=1)

        # self.bau_item_frame = customtkinter.CTkFrame(self.f3)
        # self.bau_item_frame.grid(row=0, column=2, padx=(10,10), sticky="ne")
        # self.bau_item_frame.grid_columnconfigure(2, weight=1)
        
        
        # self.tables = self.get_table_list()

        # # Создайте список для отображения таблиц
        # self.table_listbox = CTkListbox(self.bau_list_frame,  height=10, corner_radius = 2)
        # self.table_listbox.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        # # Заполните список таблицами
        # for table in self.tables:
        #     self.table_listbox.insert(CTk.END, table)

        # # Создайте кнопку для выбора таблицы
        # self.select_button = CTk.CTkButton(self.bau_list_frame, corner_radius=2, height=30, width=250, border_spacing=5,
        #                                         fg_color=("gray30"), text_color=("gray90"),
        #                                         hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
        #                                         anchor="center", text="Выбрать", command=self.select_table_button)
        # self.select_button.grid(row=1, column=0,  pady=10, sticky="nsew")

        # # Создайте кнопку для создания новой таблицы
        # if self.role == "1":
        #     self.create_button = CTk.CTkButton(self.bau_list_frame, corner_radius=2, height=30, width=250, border_spacing=5,
        #                                         fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
        #                                         font=customtkinter.CTkFont(size=15, weight="bold"),
        #                                         anchor="center", text="Создать", command=self.create_table)
        #     self.create_button.grid(row=2, column=0, sticky="nsew")

        # # Создайте кнопку для удаления таблицы
        #     self.delete_button = CTk.CTkButton(self.bau_list_frame, corner_radius=2, height=30, width=250, border_spacing=5,
        #                                         fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
        #                                         font=customtkinter.CTkFont(size=15, weight="bold"),
        #                                         anchor="center", text="Удалить", command=self.delete_table)
        #     self.delete_button.grid(row=3, column=0, pady=10, sticky="nsew")

        
        # self.selcted_bau_table_label = customtkinter.CTkLabel(self.bau_button_frame, text="", 
        #                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.selcted_bau_table_label.grid(row=0, column=0, padx=20, pady=20)

        # self.bar_code_f2 = customtkinter.CTkEntry(self.bau_button_frame, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
        # self.bar_code_f2.grid(column= 0, row=1,  pady=(10, 10), sticky="nsew",)
        

        # self.sum = customtkinter.CTkEntry(self.bau_button_frame, placeholder_text="Введите количество", width= 250, corner_radius = 3)
        # self.sum.grid(column= 0, row=2, pady=(0, 0), sticky="nsew",)

        # self.add_button = CTk.CTkButton(self.bau_button_frame, corner_radius=2, height=30, width=250, border_spacing=5,
        #                                         fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
        #                                         font=customtkinter.CTkFont(size=15, weight="bold"),
        #                                         anchor="center", text="Отправить", command=self.add_button_bau)
        # self.add_button.grid(row=3, column=0, pady=10, sticky="nsew")





        
        # self.item_table = ttk.Treeview(self.bau_item_frame, columns=("","VZ Nr.", "Bedeutung","Bestand"), style="Treeview", height=24)
        # self.item_table.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nsew")
    
        # self.item_table.column("#0", width=0, stretch=False)
        # self.item_table.column("#1", width=150)
        # self.item_table.column("#2", width=250)
        # self.item_table.column("#3", width=150)
        # self.item_table.column("#4", width=0, stretch=False)
    
        # # Добавляем заголовки столбцов
        
        # self.item_table.heading("#1", text="VZ Nr.")
        # self.item_table.heading("#2", text="Bedeutung")
        # self.item_table.heading("#3", text="Bestand")

        # self.after(100, lambda: self.bar_code_f2.focus_set())
        # self.after(100, lambda: self.bar_code_home_frame3.focus_set())
        # self.add_button.bind('<Return>', lambda event=None: self.add_button_bau())
    
############## ############## ############## ############## #Настройка фрейма №4 ############## ############## ############## ############## ############## 
        self.log_view = customtkinter.CTkTextbox(master=self.f4, width=400, corner_radius=3)
        self.log_view.grid(row=0, column=0, padx=(5,5), pady=(5,0), sticky="nsew")
        self.clear_log_button = customtkinter.CTkButton(self.f4,  corner_radius=2, height=30, width=250, border_spacing=5,
                                                fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
                                                font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center", text="Clear logs", command=self.clear_logs)
        self.clear_log_button.grid(row=1, column=0, pady=5, sticky="nsew")








############## ############## ############## ############## #Настройка фрейма №5 ############## ############## ############## ############## ##############         




    
        
        self.bar_code.bind("<KeyRelease>", self.check_vz_nr)
        self.vz_nr.bind("<KeyRelease>", self.check_barcode)
        self.table.bind("<<TreeviewSelect>>", self.on_item_select)
        self.bar_code.bind('<Return>', lambda event=None: self.kol2())
        self.vz_nr.bind('<Return>', lambda event=None: self.kol2())
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
        self.display_existing_products()
        self.create_labels()

    def create_labels(self):
        label = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE", width= 150, fg_color="#0f5925")
        label.pack(side='left', padx=(10,5), anchor="nw")
        label2 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="NAME",width= 150, fg_color="#0f5925")
        label2.pack(side='left', padx=5, anchor="nw")
        label3 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN",width= 150, fg_color="#0f5925")
        label3.pack(side='left', padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFURUNG VON",width= 150, fg_color="#0f5925")
        label4.pack(side='left', padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFURUNG BIS",width= 150, fg_color="#0f5925")
        label5.pack(side='left', padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text="VRAO AB",width= 150, fg_color="#0f5925")
        label6.pack(side='left', padx=5, anchor="nw")
        label7 = customtkinter.CTkLabel(self.bau_frame2, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"VRAO BIS",width= 150, fg_color="#0f5925")
        label7.pack(side='left', padx=5, anchor="nw")

        
        inaktiv_label = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="KOSTENSTELLE", width= 150, fg_color="#0f5925")
        inaktiv_label.pack(side='left', padx=5, anchor="nw")
        inaktiv_label2 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="NAME",width= 150, fg_color="#0f5925")
        inaktiv_label2.pack(side='left', padx=5, anchor="nw")
        inaktiv_label3 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="BAUVORHABEN",width= 150, fg_color="#0f5925")
        inaktiv_label3.pack(side='left', padx=5, anchor="nw")
        inaktiv_label4 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFURUNG VON",width= 150, fg_color="#0f5925")
        inaktiv_label4.pack(side='left', padx=5, anchor="nw")
        inaktiv_label5 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="AUSFURUNG BIS",width= 150, fg_color="#0f5925")
        inaktiv_label5.pack(side='left', padx=5, anchor="nw")
        inaktiv_label6 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text="VRAO AB",width= 150, fg_color="#0f5925")
        inaktiv_label6.pack(side='left', padx=5, anchor="nw")
        inaktiv_label7 = customtkinter.CTkLabel(self.bau_frame3, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"VRAO BIS",width= 150, fg_color="#0f5925")
        inaktiv_label7.pack(side='left', padx=5, anchor="nw")

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
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab, vrao_bis, ansprechpartner, status FROM bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'vrao_ab': product_tuple[8],
                            'vrao_bis': product_tuple[9], 'ansprechpartner': product_tuple[10],'status': product_tuple[11] }
            product_dicts.append(product_dict)
        return product_dicts

    def get_products_from_database(self, status = 'Aktiv'):
        # Открываете курсор для выполнения SQL-запроса
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab, vrao_bis, ansprechpartner, status FROM Bau WHERE status = %s ORDER BY TO_DATE(ausfurung_von, 'DD.MM.YYYY')", (status,))
        products = cursor.fetchall()
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'kostenstelle': product_tuple[2], 'bauvorhaben': product_tuple[3], 
                            'ort': product_tuple[4], 'strasse': product_tuple[5], 'ausfurung_von': product_tuple[6], 'ausfurung_bis': product_tuple[7], 'vrao_ab': product_tuple[8],
                            'vrao_bis': product_tuple[9], 'ansprechpartner': product_tuple[10],'status': product_tuple[11] }
            product_dicts.append(product_dict)

        return product_dicts
    
    def create_inaktiv_frame(self, inaktiv_product):
        self.inaktiv_frame = customtkinter.CTkFrame(self.bau_frame3_2)
        self.inaktiv_frame.pack(fill='x', pady=5, anchor="nw")
        # Создаем поле с данными о товаре
        label = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['kostenstelle']}", width= 150)
        label.pack(side='left', padx=5, anchor="nw")
        label2 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['name']}",width= 150)
        label2.pack(side='left', padx=5, anchor="nw")
        label3 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['bauvorhaben']}",width= 150)
        label3.pack(side='left', padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_von']}",width= 150)
        label4.pack(side='left', padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['ausfurung_bis']}",width= 150)
        label5.pack(side='left', padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['vrao_ab']}",width= 150)
        label6.pack(side='left', padx=5, anchor="nw")
        label7 = customtkinter.CTkLabel(self.inaktiv_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{inaktiv_product['vrao_bis']}",width= 150)
        label7.pack(side='left', padx=5, anchor="nw")

        image_photo = customtkinter.CTkImage(light_image=Image.open("images/photo.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        photo_button = customtkinter.CTkButton(self.inaktiv_frame,image=image_photo, text="", command=lambda p=inaktiv_product['kostenstelle']: self.download_photo(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left', padx=5, anchor="nw")

        image_set_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"),
                                  dark_image=Image.open("images/capo.png"),
                                  size=(20, 20))
        set_capo = customtkinter.CTkButton(self.inaktiv_frame, image=image_set_capo, text="", command=lambda p=inaktiv_product['id']: self.set_capo_top_level(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left', padx=5, anchor="nw")
        
        image_stunden = customtkinter.CTkImage(light_image=Image.open("images/clock.png"),
                                  dark_image=Image.open("images/clock.png"),
                                  size=(20, 20))
        stunden = customtkinter.CTkButton(self.inaktiv_frame, image=image_stunden, text="", command=lambda p=inaktiv_product['id']: self.stunden_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left', padx=5, anchor="nw")

        image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        material = customtkinter.CTkButton(self.inaktiv_frame, image=image_material, text="", command=lambda p=inaktiv_product['id']: self.material_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left', padx=5, anchor="nw")

        image_return = customtkinter.CTkImage(light_image=Image.open("images/return.png"),
                                  dark_image=Image.open("images/return.png"),
                                  size=(20, 20))
        activate_button = customtkinter.CTkButton(self.inaktiv_frame, image=image_return, text="", command=lambda p=inaktiv_product['id']: self.activate_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        activate_button.pack(side='left', padx=5, anchor="nw")
        
    def create_product_frame(self, product):
        self.product_frame = customtkinter.CTkFrame(self.bau_frame2_2)
        self.product_frame.pack(fill='x', pady=2, anchor="nw")
        
        # Создаем поле с данными о товаре
        label = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['kostenstelle']}", width= 150)
        label.pack(side='left', padx=5, anchor="nw")
        label2 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['name']}",width= 150)
        label2.pack(side='left', padx=5, anchor="nw")
        label3 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['bauvorhaben']}",width= 150)
        label3.pack(side='left', padx=5, anchor="nw")
        label4 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_von']}",width= 150)
        label4.pack(side='left', padx=5, anchor="nw")
        label5 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['ausfurung_bis']}",width= 150)
        label5.pack(side='left', padx=5, anchor="nw")
        label6 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['vrao_ab']}",width= 150)
        label6.pack(side='left', padx=5, anchor="nw")
        label7 = customtkinter.CTkLabel(self.product_frame, font=customtkinter.CTkFont(size=15, weight="bold") , text=f"{product['vrao_bis']}",width= 150)
        label7.pack(side='left', padx=5, anchor="nw")

        image_reduction = customtkinter.CTkImage(light_image=Image.open("images/reduction.png"),
                                  dark_image=Image.open("images/reduction.png"),
                                  size=(20, 20))
        reduction_btn = customtkinter.CTkButton(self.product_frame,image=image_reduction, text="", command=lambda p=product['id']: self.open_reduction_menu(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        reduction_btn.pack(side='left', padx=5, anchor="nw")

        photo_image = customtkinter.CTkImage(light_image=Image.open("images/photo.png"),
                                  dark_image=Image.open("images/photo.png"),
                                  size=(20, 20))
        photo_button = customtkinter.CTkButton(self.product_frame,image=photo_image, text="", command=lambda p=product['id']: self.download_photo(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        photo_button.pack(side='left', padx=5, anchor="nw")

        image_set_capo = customtkinter.CTkImage(light_image=Image.open("images/capo.png"),
                                  dark_image=Image.open("images/capo.png"),
                                  size=(20, 20))
        set_capo = customtkinter.CTkButton(self.product_frame, image=image_set_capo, text="", command=lambda p=product['id']: self.set_capo_top_level(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red") )
        set_capo.pack(side='left', padx=5, anchor="nw")
        
        image_stunden = customtkinter.CTkImage(light_image=Image.open("images/clock.png"),
                                  dark_image=Image.open("images/clock.png"),
                                  size=(20, 20))
        stunden = customtkinter.CTkButton(self.product_frame, image=image_stunden, text="", command=lambda p=product['id']: self.stunden_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        stunden.pack(side='left', padx=5, anchor="nw")

        image_material = customtkinter.CTkImage(light_image=Image.open("images/material.png"),
                                  dark_image=Image.open("images/material.png"),
                                  size=(20, 20))
        material = customtkinter.CTkButton(self.product_frame, image=image_material, text="", command=lambda p=product['id']: self.material_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                 font=customtkinter.CTkFont(size=15, weight="bold"), anchor="center",fg_color="#2d2e2e",hover_color=("red"))
        material.pack(side='left', padx=5, anchor="nw")

        image_delete = customtkinter.CTkImage(light_image=Image.open("images/delete.png"),
                                  dark_image=Image.open("images/delete.png"),
                                  size=(20, 20))
        deactive_button = customtkinter.CTkButton(self.product_frame, image=image_delete, text="", command=lambda p=product['id']: self.deactive_bau(p),corner_radius=2, height=20, width=50, border_spacing=5,
                                                fg_color=("#2d2e2e"), text_color=("gray90"),
                                                hover_color=("red"), font=customtkinter.CTkFont(size=15, weight="bold"),
                                                anchor="center" )
        deactive_button.pack(side='left', padx=5, anchor="nw")

        current_date = datetime.now().date()
        # Преобразуем строку даты из базы данных в объект datetime
        product_date = datetime.strptime(product['ausfurung_von'], '%d.%m.%Y').date()
        # Вычисляем разницу в днях между текущей датой и датой в товаре
        days_until_due = (product_date - current_date).days
        
        # Если остается 7 дней или менее до даты, устанавливаем красный цвет
        if 1 <= days_until_due <= 7:
            label.configure(fg_color="#8a0707")
            label2.configure(fg_color="#8a0707")
            label3.configure(fg_color="#8a0707")
            label4.configure(fg_color="#8a0707")
            label5.configure(fg_color="#8a0707")
            label6.configure(fg_color="#8a0707")
            label7.configure(fg_color="#8a0707")
        
        elif days_until_due == 0:
            label.configure(fg_color="#56149c")
            label2.configure(fg_color="#56149c")
            label3.configure(fg_color="#56149c")
            label4.configure(fg_color="#56149c")
            label5.configure(fg_color="#56149c")
            label6.configure(fg_color="#56149c")
            label7.configure(fg_color="#56149c")
        
        elif 8 <= days_until_due <= 14:
            label.configure(fg_color="#e6e220", text_color = "black")
            label2.configure(fg_color="#e6e220", text_color = "black")
            label3.configure(fg_color="#e6e220", text_color = "black")
            label4.configure(fg_color="#e6e220", text_color = "black")
            label5.configure(fg_color="#e6e220", text_color = "black")
            label6.configure(fg_color="#e6e220", text_color = "black")
            label7.configure(fg_color="#e6e220", text_color = "black")
        elif product_date < current_date:
            # Если время прошло, устанавливаем синий цвет
            label.configure(fg_color="#0b558a")
            label2.configure(fg_color="#0b558a")
            label3.configure(fg_color="#0b558a")
            label4.configure(fg_color="#0b558a")
            label5.configure(fg_color="#0b558a")
            label6.configure(fg_color="#0b558a")
            label7.configure(fg_color="#0b558a")

    def open_reduction_menu(self,product_id):
        import reduction_bau_menu
        reduction_menu = reduction_bau_menu.App(self, product_id)  # создаем окно, если его нет или оно уничтожено
        reduction_menu.grab_set()  # захватываем фокус
        reduction_menu.wait_window()  # ждем закрытия дочернего окна
        reduction_menu.grab_release()  # освобождаем фокус после его закрытия
        self.update_product_list()

    def material_bau(self):
        pass

    def stunden_bau(self,product_id):
        pass

    def set_capo_top_level(self,product_id):
        self.toplevel_window = Set_Capo(self, product_id)  # создаем окно, если его нет или оно уничтожено
        self.toplevel_window.grab_set()  # захватываем фокус
        self.toplevel_window.wait_window()  # ждем закрытия дочернего окна
        self.toplevel_window.grab_release()  # освобождаем фокус после его закрытия

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
        for widget in self.bau_frame2_2.winfo_children():
            widget.destroy()

        for widget in self.bau_frame3_2.winfo_children():
            widget.destroy()

        self.display_existing_products()

    def download_photo(self, product_kostenstelle):
        thread = threading.Thread(target=self.download_photo_in_thread, args=(product_kostenstelle,))
        thread.start()

    def download_photo_in_thread(self, product_kostenstelle):
        folder_path = filedialog.askdirectory(title="Select Folder to Save Images")
        cursor = self.conn.cursor()
        cursor.execute("SELECT photo_data, bau FROM sicherung WHERE bau = %s", (product_kostenstelle,))
        row = cursor.fetchone()
        data1 = row[1]
        print(data1)
        if folder_path:
            # Создаем папку для сохранения изображений
            folder_name = f"{data1}"
            folder_path = os.path.join(folder_path, folder_name)

            # Проверяем, существует ли папка, и создаем, если нет
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Извлечение строки
            if row is not None:
                # Проверяем, что данные не являются None
                if row[0] is not None:
                    # Преобразование объекта memoryview в строку
                    image_data_array = bytes(row[0]).decode('utf-8').split(',')

                    # Декодирование и сохранение каждого изображения
                    for i, image_data in enumerate(image_data_array):
                        try:
                            # Декодирование из формата base64
                            image_data_decoded = base64.b64decode(image_data)

                            # Создание объекта изображения
                            image = Image.open(BytesIO(image_data_decoded))
                            if hasattr(image, '_getexif'):  # проверка на наличие данных ориентации
                                exif = image._getexif()
                                if exif is not None:
                                    orientation = exif.get(0x0112)
                                    if orientation is not None:
                                        if orientation == 3:
                                            image = image.rotate(180, expand=True)
                                        elif orientation == 6:
                                            image = image.rotate(270, expand=True)
                                        elif orientation == 8:
                                            image = image.rotate(90, expand=True)

                            # Путь для сохранения изображения
                            image_path = os.path.join(folder_path, f"{data1}_{i+1}.jpeg")

                            # Проверка наличия файла перед сохранением
                            if not os.path.exists(image_path):
                                # Сохранение изображения
                                image.save(image_path, "JPEG", quality=20)
                            else:
                                print(f"File {image_path} already exists, skipping.")
                        except Exception as e:
                            print(f"Error processing image {i+1}: {e}")
                else:
                    print(f"No data found for id = {self.product_kostenstelle}")
            threading.Thread(target=self.show_notification, args=("Уведомление", "Изображения успешно загружены!")).start()
    
    def show_notification(self, title, message):
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)

    def map(self):
        map_window = test_map.App()  # создаем окно, если его нет или оно уничтожено
        map_window.grab_set()  # захватываем фокус
        map_window.wait_window()  # ждем закрытия дочернего окна
        map_window.grab_release()  # освобождаем фокус после его закрытия
        

    def upload_images(self):
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
        
        cursor.execute("SELECT kostenstelle_vvo FROM Bau WHERE kostenstelle_vvo = %s", (kostenstelle_vvo,))
        existing_record = cursor.fetchone()
        if existing_record:
            threading.Thread(target=self.show_notification, args=("Ошибка", "Стройка с таким номером уже существует!")).start()
            threading.Thread(target=lambda: self.flash_error_color(self.kostenstelle_vvo), args=()).start()
            return  # Прерываем выполнение функции, так как запись уже существует
        
        cursor.execute(f"CREATE TABLE IF NOT EXISTS Bau (id SERIAL PRIMARY KEY,name_bau text, kostenstelle_vvo text,bauvorhaben text,ort text, strasse text,ausfurung_von text,ausfurung_bis text,vrao_ab text, vrao_bis text, ansprechpartner text, status text, image_data BYTEA, pdf_data BYTEA, meta_data text, uberwachung text,vzp)")

        meta_data = None
        
        cursor.execute(f"INSERT INTO Bau (name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab, vrao_bis, ansprechpartner, status, pdf_data, meta_data , uberwachung,vzp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(name, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab,vrao_bis, ansprechpartner, status, self.pdf_data, meta_data, uberwacht,vzp))
        self.update_product_list()

        self.name_bau.delete(0, 'end')
        self.kostenstelle_vvo.delete(0, 'end')
        self.bauvorhaben.delete(0, 'end')
        self.strasse.delete(0, 'end')
        self.ort.delete(0, 'end')
        self.ansprechpartner.delete(0, 'end')
        self.vzp.delete(0, 'end')
        self.pdf_data = None
        threading.Thread(target=self.show_notification, args=("Уведомление", "Стройка создана!")).start()
        user = self.login # имя кто сделал действие для лога
        action = f"Создал таблицу под названием {name}" # перменная для создания названия действия лога
        self.user_action(user, action)
    
    def flash_error_color(self, widget):
        for _ in range(5):  # Меняем цвет 5 раз
            widget.configure(border_color="grey")
            time.sleep(0.2)
            widget.configure(border_color="red")
            time.sleep(0.2)  # Задержка в 200 миллисекунд
   
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

        # Кодируем PDF-файлы в base64 и добавляем их в список pdf_files_base64
        pdf_files_base64 = []
        for pdf_file_path in pdf_file_paths:
            pdf_files_base64.append(encode_pdf_to_base64(pdf_file_path))

            # Преобразование списка в строку с разделителем запятой
        self.pdf_data = ','.join(pdf_files_base64)
        threading.Thread(target=self.show_notification, args=("Уведомление", "Планы успешно загружены!")).start()
  
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
        cursor = self.conn.cursor()
        try:
            if selected_reduction == "Current":
                if selected_action == "Add":
                    cursor.execute("SELECT aktueller_bestand FROM Lager_Bestand WHERE bar_Code = %s", (bar_code,))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data + int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s", (new_value, bar_code))
                    self.show_all_data()

                elif selected_action == "Decrease":
                    cursor.execute("SELECT aktueller_bestand FROM Lager_Bestand WHERE bar_Code = %s", (bar_code,))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data  - int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s", (new_value, bar_code))
                    self.show_all_data()

                elif selected_action == "Replace":
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s WHERE bar_Code = %s", (sum_value, bar_code))
                    self.show_all_data()

            if selected_reduction == "Total on account":
                if selected_action == "Add":
                    cursor.execute("SELECT bestand_lager FROM Lager_Bestand WHERE bar_Code = %s", (bar_code,))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data + int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s", (new_value, bar_code))
                    self.show_all_data()

                elif selected_action == "Decrease":
                    cursor.execute("SELECT bestand_lager FROM Lager_Bestand WHERE bar_Code = %s", (bar_code,))
                    data = cursor.fetchall()
                    new_data = data[0][0]  # Получаем значение из кортежа
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data  - int(sum_value)  # Преобразуем sum_value в целое число
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s", (new_value, bar_code))
                    self.show_all_data()

                elif selected_action == "Replace":
                    cursor.execute("UPDATE Lager_Bestand SET bestand_lager = %s WHERE bar_Code = %s", (sum_value, bar_code))
                    self.show_all_data()

            if selected_reduction == "Defect":
                if selected_action == "Add":
                    cursor.execute("SELECT * FROM Lager_Bestand WHERE bar_Code = %s", (bar_code,))
                    data = cursor.fetchone()
                    new_data = data[5]
                    new_data2 = data[4]
                    if new_data is None: 
                        new_data = 0
                    new_value = new_data - int(sum_value) 
                    new_value2 = new_data2 - int(sum_value)
                    cursor.execute("UPDATE Lager_Bestand SET aktueller_bestand = %s, bestand_lager = %s  WHERE bar_Code = %s", (new_value, new_value2, bar_code))
                    if data:
                        # Если данные были найдены, извлекаем нужные значения
                        (bar_code, vz_nr, bedeutung, größe, bestand_lager, aktueller_bestand) = data
                        cursor.execute("SELECT * FROM Defekt WHERE bar_code = %s", (bar_code,))
                        existing_defekt_data = cursor.fetchone()
                        # Выполняем запрос на вставку данных в Defekt
                        if existing_defekt_data:
                            rest_data = existing_defekt_data[4] + int(sum_value)
                            cursor.execute("UPDATE Defekt SET bestand = %s WHERE bar_code = %s",(rest_data, bar_code))
                        else:
                            cursor.execute("INSERT INTO Defekt (bar_code, vz_nr, bedeutung, größe, bestand) VALUES (%s, %s, %s, %s, %s)", (bar_code, vz_nr, bedeutung, größe, sum_value))
        except Exception as e:
            # Обработка ошибок, например, вывод сообщения
            print(f"Ошибка: {e}")
            self.show_all_data()
        self.bar_code_home_frame3.delete(0, 'end')
        self.sum_home_frame3.delete(0, 'end')
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
    
    # def add_button_bau(self):
    #     print(self.selected_table)
    #     self.barcode_f2 = self.bar_code_f2.get()
    #     self.sum_value = self.sum.get()  # Сохраняем значение суммы как атрибут объекта
        
    #     # Создаем контекстные менеджеры для соединений, и здесь не нужно закрывать соединение с базой
    #     cursor = self.conn.cursor()
    #     print("0,5")
    #     # Выполняем операцию SELECT в базе данных "bd.db"
    #     cursor.execute("SELECT * FROM lager_bestand WHERE bar_code = %s",(self.barcode_f2,))
    #     data = cursor.fetchone()
    #     print(data)
    #     bar = data[0]
    #     vz = data[1]
    #     bed = data[4]
    #     akt = data[5]
    #     print("1")
    #     try:
    #         # Проверяем наличие товара в таблице
    #         cursor.execute(f"SELECT * FROM {self.selected_table} WHERE Bar_Code = %s",(bar,))
    #         existing_product = cursor.fetchone()
    #         print(self.selected_table)
    #         print("2")
    #         if existing_product:
    #             # Если товар уже существует, обновляем Bestand
    #             cursor.execute(f"UPDATE {self.selected_table} SET bestand = %s WHERE bar_code = %s",(self.sum_value,bar))
    #             print("3")
    #         else:
    #             # Если товар не существует, добавляем новую запись
    #             cursor.execute(f"INSERT INTO {self.selected_table} (bar_code, vz_nr, bedeutung, bestand) VALUES (%s, %s, %s, %s)",(bar,vz,bed,self.sum_value))
    #             # Очищаем таблицу программы перед добавлением новых данных
    #             print("4")
    #         for row in self.item_table.get_children():
    #             self.item_table.delete(row)
    #             print("5")
    #         # Загружаем все данные из выбранной таблицы и выводим их в таблицу программы
    #         cursor.execute(f"SELECT vz_Nr, bedeutung, bestand FROM {self.selected_table}")
    #         data = cursor.fetchall()
    #         print("6")
    #         for item in data:
    #             self.item_table.insert("", "end", values=item)
    #         self.bar_code_f2.delete(0, 'end')
    #         self.sum.delete(0, 'end') 
    #         self.after(50, lambda: self.bar_code_f2.focus_set())
            
            
    #     except Exception as e:
    #         print("Ошибка add_button_bau:", e)

    # def delete_table(self):
    #     selected_table = self.table_listbox.get(self.table_listbox.curselection())
    #     if selected_table:
    #         # Открываем диалоговое окно с вопросом
    #         confirmation = tkinter.messagebox.askyesno("Подтверждение", f"Вы уверены что хотите удалить таблицу '{selected_table}'?")
            
    #         if confirmation:
    #             # Удалите таблицу из базы данных
    #             self.cursor.execute(f"DROP TABLE IF EXISTS {selected_table};")
    #             self.conn.commit()

    #             # Обновите список таблиц
    #             self.tables = self.get_table_list()
    #             self.table_listbox.delete(0, CTk.END)  # Очистите список
    #             for table in self.tables:
    #                 self.table_listbox.insert(CTk.END, table)
    #     user = self.login # имя кто сделал действие для лога
    #     action = f"удалил таблицу под названием {selected_table}" # перменная для создания названия действия лога
    #     self.user_action(user, action)

    # def create_table(self):
    #     # Запросите имя новой таблицы с помощью диалогового окна

    #     dialog = customtkinter.CTkInputDialog(text="Введите название стройки или номер", title="Baustelle", button_fg_color = "gray30",
    #                                                                                     button_hover_color = "red")
    #     dialog.geometry("300x200")
    #     text = dialog.get_input()  # waits for input

    #     if text:
    #         # Создайте новую таблицу в базе данных
    #         self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {text} (Bar_Code TEXT, VZ_Nr TEXT, Bedeutung TEXT, Bestand TEXT);")
    #         self.conn.commit()

    #         if self.table_listbox.size() > 0:
    #             self.table_listbox.delete(0, CTk.END)
    #         # Обновляем список таблиц, вызывая функцию get_table_list()
    #         self.tables = self.get_table_list()
    #         for table in self.tables:
    #             self.table_listbox.insert(CTk.END, table)
    #     user = self.login # имя кто сделал действие для лога
    #     action = f"создал таблицу под названием {text}" # перменная для создания названия действия лога
    #     self.user_action(user, action)
   
    # def get_table_list(self):
    #     # Получите список таблиц из базы данных
    #     self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog') AND table_name NOT IN ('users','lager_bestand', 'app_logs', 'defekt', 'material_lager');")
    #     table_list = self.cursor.fetchall()
    #     return [table[0] for table in table_list]

    # def select_table_button(self):
    #     selected_table = self.table_listbox.get(self.table_listbox.curselection())
    #     if selected_table:
    #         self.selected_table = selected_table  # Сохраняем имя выбранной таблицы
    #         if self.selcted_bau_table_label:
    #             self.selcted_bau_table_label.destroy()
    #             self.selcted_bau_table_label = customtkinter.CTkLabel(self.bau_button_frame, text=f"Вы выбрали: {selected_table}", 
    #                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
    #             self.selcted_bau_table_label.grid(row=0, column=0, padx=20, pady=20)
    #     # Очищаем таблицу программы перед добавлением новых данных
    #     for row in self.item_table.get_children():
    #         self.item_table.delete(row)
        
    #     # Загружаем данные из выбранной таблицы и выводим их в таблицу программы
    #         cursor = self.conn.cursor()
    #         cursor.execute(f"SELECT VZ_Nr, Bedeutung, Bestand FROM {selected_table}")
    #         data = cursor.fetchall()
    #         for item in data:
    #             self.item_table.insert("", "end", values=item)

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
            self.bau_frame.configure(text=texts.get("Building", "Building"))
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
                self.table.insert("", "end", values=item)
        elif self.barcode == "" and self.vz == "":
            print("Сработало")
            self.result_show("Забыл ввести данные")
        else:
            self.result_show("Данных не найдено")
        self.bar_code.delete(0, 'end')
        self.vz_nr.delete(0, 'end')


    def check_vz_nr(self, event):
        # Функция вызывается при изменении баркода
        if self.bar_code.get():
            # Если баркод не пустой, очищаем поле Vz Nr
            self.vz_nr.delete(0, 'end')
        
    def check_barcode(self, event):

        # Функция вызывается при изменении Vz Nr
        if self.vz_nr.get():
            # Если Vz Nr не пустой, очищаем поле баркода
            self.bar_code.delete(0, 'end')

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
            self.bau_frame.configure(fg_color=("red") if name == "Building" else "transparent")
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
        if name == "Building":
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
        self.select_frame_by_name("Building")

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