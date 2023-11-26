import tkinter as tk
from tkinter import ttk

class TableWithButtons(tk.Tk):
    def __init__(self, data):
        super().__init__()

        self.title("Table with Buttons")

        # Создаем Treeview
        self.tree = ttk.Treeview(self, columns=("Column 1", "Column 2"))
        self.tree.heading("#0", text="Row")
        self.tree.heading("#1", text="Column 1")
        self.tree.heading("#2", text="Column 2")

        # Вставляем данные
        for i, row in enumerate(data):
            self.tree.insert("", "end", iid=f"Row_{i+1}", text=f"Row {i+1}", values=(row[0], row[1]))

        # Создаем кнопки
        for i in range(len(data)):
            button_1 = tk.Button(self.tree, text=f"Button 1_{i+1}", command=lambda i=i: self.on_button_click(i, 1))
            button_2 = tk.Button(self.tree, text=f"Button 2_{i+1}", command=lambda i=i: self.on_button_click(i, 2))

            # Помещаем кнопки в Treeview
            self.tree.window_create(self.tree.item(f"Row_{i+1}")['open'], window=button_1, anchor="w")
            self.tree.set(f"Row_{i+1}", "#2", "")  # Пустая колонка для выравнивания

            self.tree.window_create(self.tree.item(f"Row_{i+1}")['open'], window=button_2, anchor="w")
            self.tree.set(f"Row_{i+1}", "#2", "")  # Пустая колонка для выравнивания

        # Отображаем Treeview
        self.tree.pack(padx=10, pady=10)

    def on_button_click(self, row_index, button_number):
        # Ваш код обработки нажатия на кнопку
        if button_number == 1:
            print(f"Button 1 clicked! Value of Column 1: {self.tree.item(f'Row_{row_index+1}', 'values')[0]}")
        elif button_number == 2:
            print(f"Button 2 clicked! Value of Column 2: {self.tree.item(f'Row_{row_index+1}', 'values')[1]}")

if __name__ == "__main__":
    # Пример данных для таблицы
    table_data = [
        ["A1", "B1"],
        ["A2", "B2"],
        ["A3", "B3"],
        # ... другие строки
    ]

    app = TableWithButtons(table_data)
    app.mainloop()
