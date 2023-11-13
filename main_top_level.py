# import customtkinter
# import customtkinter as CTk
# import sqlite3
# from tkinter import *
# from tkinter import ttk
# import Autorisation
# import PIL.Image
# from CTkListbox import *
# from tkinter.simpledialog import askstring
# import tkinter.messagebox
# from CTkTable import *
# import export_to_exel
# import os
# import localizations
# import logging
# import main

# customtkinter.set_appearance_mode("dark")

# class Top_Level_Window(CTk.CTk):
#     def __init__(self,action_handler, *args, **kwargs): # После теста добавить аргумент login и role  не забыть убрать комментарий ниже!!!!
#         super().__init__(*args, **kwargs)
#         self.action_handler = action_handler
#         # Установите геометрию окна
#         self.geometry("500x500+500+300")
#         self.iconbitmap(default=r"vvo.ico")
#         self.title("Bestand Lager")
#         self.resizable(False, False)  # Запрещаем или разрешаем изменение размера окна
#         self.grab_set()
#         self.grid_rowconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=1)
    

#         self.bar_code = customtkinter.CTkEntry(self, placeholder_text="Bar Code:", width= 250, corner_radius = 3)
#         self.bar_code.pack( padx=(10, 10), pady=(30, 10))

#         self.sum = customtkinter.CTkEntry(self, placeholder_text="Введите количество", width= 250, corner_radius = 3)
#         self.sum.pack(pady=(0, 0))


#         self.submit_button = customtkinter.CTkButton(master=self, corner_radius=2, height=30, width= 200, 
#                                                 fg_color=("gray30"), text_color=("gray90"),hover_color=("red"), 
#                                                 font=customtkinter.CTkFont(size=15, weight="bold"),
#                                                 anchor="center", text='Log in', command=self.action_handler)
#         self.submit_button.pack( padx=(10, 10), pady=(30, 10))
        


#         self.after(100, lambda: self.bar_code.focus_set())
#         self.submit_button.bind('<Return>', lambda event=None: self.submit())

#     def add_to_table():
#         print("Сработало")
    
#     def submit (self):
#         if self.action_handler:
#             self.action_handler()  # Вызываем сохраненную функцию-обработчик из основного окна


# # if __name__ == '__main__':
# #     app = Top_Level_Window()
# #     app.mainloop()