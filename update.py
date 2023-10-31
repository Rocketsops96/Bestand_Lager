import os
import shutil
import requests
import zipfile
from io import BytesIO
import wget
# URL для загрузки новой версии вашего проекта с GitHub


# Путь к временной папке для загрузки и распаковки новой версии
temp_dir = 'new'

# Создайте временную папку (если она не существует)
os.makedirs(temp_dir, exist_ok=True)

url = 'https://github.com/Rocketsops96/Bestand_Lager/archive/main.zip'
wget.download(url, out=os.path.join(temp_dir, 'Bestand_Lager-main.zip'))

# Путь к временной папке для загрузки и распаковки новой версии
temp_dir = 'new'

# Создайте временную папку (если она не существует)
os.makedirs(temp_dir, exist_ok=True)

# Загрузите новую версию с GitHub и сохраните как zip-файл
response = requests.get(url)
if response.status_code == 200:
    with open(os.path.join(temp_dir, 'Bestand_Lager-main.zip'), 'wb') as zip_file:
        zip_file.write(response.content)

    # Распакуйте zip-файл во временную папку
    with zipfile.ZipFile(os.path.join(temp_dir, 'Bestand_Lager-main.zip'), 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Замените файлы в корневой папке новой версией
    for item in os.listdir(os.path.join(temp_dir, 'Bestand_Lager-main')):
        source = os.path.join(temp_dir, 'Bestand_Lager-main', item)
        destination = os.path.join(os.getcwd(), item)
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    # Удалите временную папку
    shutil.rmtree(temp_dir)

    print("Обновление завершено.")
else:
    print("Не удалось загрузить новую версию с GitHub.")
