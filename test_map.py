import customtkinter
from tkintermapview import TkinterMapView
import regbase
import json


customtkinter.set_default_color_theme("blue")

# Включаем кэширование на 1 час


class App(customtkinter.CTkToplevel):

    APP_NAME = "VVO Map"
    WIDTH = 800
    HEIGHT = 500
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = regbase.create_conn()

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.state("zoomed")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["Google normal", "Google satellite"],fg_color="gray10", button_color="red", button_hover_color=("black"),
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=0, column=0, padx=5, pady=10)

        logins = ["A.Bobrishov", "B.Gashi", "D.Mirakaj", "G.Hudzen"]
        for i, login in enumerate(logins):
            button = customtkinter.CTkButton(self.frame_left, text=login, command=lambda l=login: self.focus_on_marker(l), corner_radius=0, height=40, border_spacing=10, font=("Arial", 14, "bold"),
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("red"),
                                                       anchor="w")
            button.grid(row=i + 1, column=0, padx=0, pady=5,sticky="nsew")
        # ============ frame_left ============


       


        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)
        
       
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nsew", padx=(0, 0), pady=(0, 0))
        
         # Привязываем метод к событию двойного щелчка мыши на карте

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Suchen",
                                                width=90,text_color=("gray10", "gray90"), hover_color=("black"),fg_color=("red"),
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        # self.map_widget.set_address("Ulm")
        self.change_map("Google normal")
        

        # Добавляем контекстное меню для карты
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        

        self.marker_list = []

        # После инициализации карты в функции __init__
        self.map_widget.bind("<Double-Button-1>", self.double_click_event)
        self.update_map_markers()
        self.focus_on_marker("B.Gashi")
    def update_map_markers(self):
        try:
            print("Updating map markers...")
            # Получаем данные из базы данных
            cursor = self.conn.cursor()
            cursor.execute("SELECT geo_data, login FROM capos")
            rows = cursor.fetchall()

            # Очищаем существующие маркеры
            for marker in self.marker_list:
                marker.delete()

            # Устанавливаем новые маркеры на карту
            for row in rows:
                geo_data_str = row[0]
                login = row[1]

                # Разбиваем строку координат
                try:
                    latitude, longitude = map(float, geo_data_str.split(', '))

                    # Устанавливаем маркер на карту
                    self.marker_list.append(self.map_widget.set_marker(latitude, longitude, text=login))

                except ValueError as e:
                    print(f"Ошибка при разборе строки Geo Data: {str(e)}")
                    print(f"Geo Data: {geo_data_str}")
                    print(f"Login: {login}")

            print("Map markers updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating map markers: {e}")

        # Устанавливаем таймер для следующего обновления маркеров через 6 секунд
        self.after(30000, self.update_map_markers)

    def double_click_event(self, event):
        current_position = self.map_widget.get_position()
        marker = self.map_widget.set_marker(current_position[0], current_position[1], text="new marker")
        self.marker_list.append(marker)

        # Добавляем новые координаты в траекторию
        if self.previous_position:
            self.map_widget.draw_line(self.previous_position, (current_position[0], current_position[1]))

        # Сохраняем текущие координаты как предыдущие
        self.previous_position = (current_position[0], current_position[1])

    def focus_on_marker(self, login):
        # Ищем маркер с соответствующим текстом
        matching_markers = [marker for marker in self.marker_list if marker.text == login]
        if matching_markers:
            marker = matching_markers[0]
            # Устанавливаем позицию на маркере
            self.map_widget.set_position(marker.position[0], marker.position[1], marker=True, text=login)
            self.map_widget.set_zoom(17)

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def add_marker_event(self, coords):
        print("Add marker:", coords)
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text="new marker")


    def change_map(self, new_map: str):
        
        if new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

