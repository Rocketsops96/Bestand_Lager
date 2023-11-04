import tkinter as tk
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("GIF Animation")
        self.geometry("50x50")

        # Загрузка анимации GIF и изменение размера кадров
        self.animation_image = Image.open("gif2.gif")
        self.animation_frames = []

        try:
            while True:
                frame = self.resize_image(self.animation_image, (50, 50))  # Замените (100, 100) на желаемые размеры
                frame = ImageTk.PhotoImage(frame)
                self.animation_frames.append(frame)
                self.animation_image.seek(self.animation_image.tell() + 1)
        except EOFError:
            pass

        # Создание лейбла для отображения анимации
        self.animation_label = tk.Label(self)
        self.animation_label.pack()

        # Запуск анимации
        self.current_frame = 0
        self.animate()

    def resize_image(self, image, size):
        # Изменение размера изображения
        return image.resize(size)

    def animate(self):
        # Отображение текущего кадра анимации и переход к следующему
        self.animation_label.config(image=self.animation_frames[self.current_frame])
        self.current_frame += 1

        # Если достигнут конец анимации, вернуться к началу
        if self.current_frame == len(self.animation_frames):
            self.current_frame = 1

        # Рекурсивный вызов метода для непрерывной анимации
        self.after(100, self.animate)

if __name__ == "__main__":
    app = App()
    app.mainloop()
