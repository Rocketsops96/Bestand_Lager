import os
import requests
import wget
import zipfile
import subprocess
import shutil  # Импортируйте модуль shutil

# Путь к временной папке для загрузки и распаковки новой версии
temp_dir = 'new'

# Создайте временную папку (если она не существует)
os.makedirs(temp_dir, exist_ok=True)

# URL для получения информации о версии на сервере
version_url = 'https://raw.githubusercontent.com/Rocketsops96/Bestand_Lager/main/version.txt'

# Получите версию с сервера
response = requests.get(version_url)
if response.status_code == 200:
    server_version = response.text.strip()  # Предполагаем, что версия в текстовом файле
    current_version = "1.0.0"  # Замените на актуальную версию

    if server_version > current_version:
        print("Доступно обновление. Загружаем...")

        # Загрузка новой версии программы
        new_version_url = 'https://github.com/Rocketsops96/Bestand_Lager/archive/main.zip'
        wget.download(new_version_url, out=os.path.join(temp_dir, 'new_version.zip'))

        # Распаковка новой версии
        with zipfile.ZipFile(os.path.join(temp_dir, 'new_version.zip'), 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Замена текущей версии новой версией
        for item in os.listdir(os.path.join(temp_dir, 'Bestand_Lager-main')):
            source = os.path.join(temp_dir, 'Bestand_Lager-main', item)
            destination = os.path.join(os.getcwd(), item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        # Удаление временной папки
        shutil.rmtree(temp_dir)

        print("Обновление завершено.")

        # Перезапуск программы (замените на свой способ запуска)
        subprocess.Popen(["python", "your_program.py"])

    else:
        print("У вас последняя версия.")
else:
    print("Не удалось получить информацию о версии с сервера.")
