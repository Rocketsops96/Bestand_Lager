import os
import shutil
import requests
import zipfile

def update_programm():
    # URL для GitHub API, указывающий на ваш репозиторий
    github_api_url = 'https://api.github.com/repos/Rocketsops96/Bestand_Lager/releases/latest'

    # Путь к временной папке для загрузки и распаковки новой версии
    temp_dir = 'new'

    # Создайте временную папку (если она не существует)
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Загрузите информацию о последнем релизе с GitHub API
        response = requests.get(github_api_url)
        response.raise_for_status()

        release_info = response.json()
        assets = release_info.get('assets', [])

        # Проверяем, есть ли какие-то ассеты (архивы) в релизе
        if assets:
            download_url = assets[0].get('browser_download_url', '')

            # Получите текущую версию
            current_version_path = 'version.txt'
            if os.path.exists(current_version_path):
                with open(current_version_path, 'r') as current_version_file:
                    current_version = current_version_file.read().strip()
            else:
                current_version = 'v0.0.0.0'

            # Если есть новая версия, загрузите и обновите проект
            if current_version != release_info['tag_name']:
                print("Обнаружено обновление. Начинается процесс обновления...")

                # Загрузите новую версию с GitHub и сохраните как zip-файл
                response = requests.get(download_url)
                response.raise_for_status()

                with open(os.path.join(temp_dir, 'update_files.zip'), 'wb') as zip_file:
                    zip_file.write(response.content)

                try:
                    # Распакуйте zip-файл во временную папку
                    with zipfile.ZipFile(os.path.join(temp_dir, 'update_files.zip'), 'r') as zip_ref:
                        # Создайте новую временную подпапку для распакованных файлов
                        temp_update_dir = os.path.join(temp_dir, 'Bestand_Lager-main')
                        zip_ref.extractall(temp_update_dir)

                        # Замените файлы в корневой папке новой версией
                        for item in os.listdir(temp_update_dir):
                            source = os.path.join(temp_update_dir, item)
                            destination = os.path.join(os.getcwd(), item)
                            if os.path.isdir(source):
                                shutil.copytree(source, destination, dirs_exist_ok=True)
                            else:
                                shutil.copy2(source, destination)

                        # Обновите версию
                        with open(current_version_path, 'w') as current_version_file:
                            current_version_file.write(release_info['tag_name'])

                        print("Обновление завершено.")
                except Exception as e:
                    print(f"Не удалось загрузить новую версию с GitHub: {e}")
            else:
                print("У вас уже установлена последняя версия.")
        else:
            print("Нет ассетов (архивов) в последнем релизе на GitHub.")
    except requests.RequestException as e:
        print(f"Ошибка при запросе к GitHub: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Удалите временную папку в конце, после копирования файлов
        shutil.rmtree(temp_dir)
        print("chfdmfsdjfsd")

# Вызовите функцию обновления программы
update_programm()
