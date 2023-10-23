from PIL import Image
import os

def resize_image(input_path, output_path, new_size):
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            aspect_ratio = width / height

            # Определите, какое измерение (ширина или высота) является ограничивающим фактором
            if aspect_ratio > 1:
                new_width = new_size
                new_height = int(new_size / aspect_ratio)
            else:
                new_width = int(new_size * aspect_ratio)
                new_height = new_size

            # Создайте новое изображение с белыми полями
            new_img = Image.new("RGB", (new_size, new_size), (255, 255, 255))
            position = ((new_size - new_width) // 2, (new_size - new_height) // 2)
            new_img.paste(img.resize((new_width, new_height), Image.LANCZOS), position)

            # Измените путь для сохранения в другую папку
            output_directory = "resize"
            os.makedirs(output_directory, exist_ok=True)  # Создаем папку, если её нет
            output_path = os.path.join(output_directory, f"{os.path.basename(input_path)}")

            new_img.save(output_path)
        print(f"Изображение успешно изменено и сохранено в {output_path}")
    except Exception as e:
        print(f"Произошла ошибка при обработке изображения {input_path}: {e}")

def process_images_in_directory(input_directory, new_size):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(root, file)
                resize_image(input_path, f"resize/{os.path.basename(input_path)}", new_size)

if __name__ == "__main__":
    input_directory = "new"
    new_size = 200  # Желаемый размер 200x200 пикселей
    process_images_in_directory(input_directory, new_size)
