import tkinter as tk
from customtkinter import CTkFrame, CTkLabel, CTkButton
import psycopg2
import regbase

class ProductApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.create_widgets()

    def create_widgets(self):
        self.product_frame = CTkFrame(self.root)
        self.product_frame.pack(fill='both', expand=True)

  
        # Отображение существующих товаров
        self.display_existing_products()

    def display_existing_products(self):
        # Получаем товары из базы данных
        products = self.get_products_from_database()

        # Создаем фреймы для каждого товара
        for product in products:
            self.create_product_frame(product)

    def get_products_from_database(self):
        # Открываете курсор для выполнения SQL-запроса
        with self.conn.cursor() as cursor:
            # Выполняете SQL-запрос для получения товаров
            cursor.execute("SELECT * FROM bau")
            # Получаете результат запроса
            products = cursor.fetchall()

        # Преобразовываем кортежи в словари
        product_dicts = []
        for product_tuple in products:
            product_dict = {'id': product_tuple[0], 'name': product_tuple[1], 'price': product_tuple[2]}
            product_dicts.append(product_dict)

        # Возвращаем список словарей товаров
        return product_dicts
    
   

    def create_product_frame(self, product):
        product_frame = CTkFrame(self.product_frame)
        product_frame.pack(fill='x', pady=5)

        # Создаем поле с данными о товаре
        label = CTkLabel(product_frame, text=f"{product['name']} - {product['price']}")
        label.pack(side='left', padx=5)

        # Кнопка для выполнения действия с товаром
        action_button = CTkButton(product_frame, text="Действие", command=lambda p=product: self.perform_action(p))
        action_button.pack(side='left', padx=5)

   

    def perform_action(self, product):
        # Здесь вы можете определить пользовательское действие для выбранного товара
        print(f"Выполнено действие для товара: {product['name']}")

if __name__ == "__main__":
    # Подключение к базе данных
    conn = regbase.create_conn()
    root = tk.Tk()
    app = ProductApp(root, conn)
    root.mainloop()

    # Не забудьте закрыть соединение с базой данных при выходе из программы
    conn.close()
