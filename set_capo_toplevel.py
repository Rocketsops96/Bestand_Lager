import customtkinter as CTk
from customtkinter import CTkCheckBox
import regbase

class Set_Capo(CTk.CTkToplevel):
    def __init__(self,parent,product_id, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        self.geometry("400x300")
        self.product_id= product_id

        self.label = CTk.CTkLabel(self, text="Team")
        self.label.pack(padx=20, pady=20)

        # Создаем 5 чекбоксов и размещаем их в окне
        self.checkbox1 = CTkCheckBox(self, text="G.Hudzen")
        self.checkbox1.pack(pady=5)

        self.checkbox2 = CTkCheckBox(self, text="D.Mirakaj")
        self.checkbox2.pack(pady=5)

        self.checkbox3 = CTkCheckBox(self, text="B.Gashi")
        self.checkbox3.pack(pady=5)

        self.checkbox4 = CTkCheckBox(self, text="A.Bobrishov")
        self.checkbox4.pack(pady=5)

        

        # Создаем кнопку "Ок"
        ok_button = CTk.CTkButton(self, text="Ок", command=self.ok_button_clicked)
        ok_button.pack(pady=10)
        
        self.set_initial_checkbox_state()

    def set_initial_checkbox_state(self):
        # Получаем текущие значения set_capo для данного товара из базы данных
        conn = regbase.create_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT set_capo FROM bau WHERE id = %s", (self.product_id,))
        result = cursor.fetchone()
        conn.close()

        # Если значения получены, устанавливаем состояние чекбоксов
        if result:
            print(result)
            set_capo_values = [value.strip() for value in result[0].split(',')]
            for checkbox in [self.checkbox1, self.checkbox2, self.checkbox3, self.checkbox4]:
                value = checkbox.cget("text")
                if value in set_capo_values:
                    checkbox.select()
                else:
                    checkbox.deselect()


    def ok_button_clicked(self):

        # Выполняем запрос в базу данных с данными из чекбоксов
        checkbox_values = [
            "G.Hudzen" if self.checkbox1.get() else None,
            "D.Mirakaj" if self.checkbox2.get() else None,
            "B.Gashi" if self.checkbox3.get() else None,
            "A.Bobrishov" if self.checkbox4.get() else None,
            
        ]
        set_capo_text = ", ".join(filter(None, checkbox_values))  # Собираем текст через запятую, удаляя пустые значения
        self.conn = regbase.create_conn()
        cursor = self.conn.cursor()
        
        cursor.execute("UPDATE bau SET set_capo = %s WHERE id = %s", (set_capo_text, self.product_id))
        # Здесь добавьте ваш код запроса в базу данных с использованием checkbox_values
        print("Checkbox values:", checkbox_values)
        # Закрываем окно после обработки
        self.destroy()
