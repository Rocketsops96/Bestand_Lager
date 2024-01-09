import os
import requests
import shutil
import zipfile
import sys
import ctypes
import time
import win32com.client  # Импортируем библиотеку pywin32

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def create_desktop_shortcut(target_path, shortcut_name):
    # Получаем путь к рабочему столу пользователя
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Создаем объект ярлыка
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(desktop_path, f"{shortcut_name}.lnk"))

    # Устанавливаем параметры ярлыка
    shortcut.Targetpath = target_path
    shortcut.save()
def delete_files_except_temp_and_update_exe():
    temp_dir = 'new'
    update_exe = 'update2.exe'
    
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            # Исключаем временную папку и update.exe из удаления
            if file_path not in [os.path.abspath(os.path.join(os.getcwd(), temp_dir)),
                                 os.path.abspath(os.path.join(os.getcwd(), update_exe))]:
                try:
                    # Проверяем, не является ли файл update.exe
                    if file.lower() != 'update.exe':
                        os.remove(file_path)
                    else:
                        print(f"Пропущено удаление файла {file_path}")
                except Exception as e:
                    print(f"Не удалось удалить файл {file_path}: {e}")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Исключаем временную папку из удаления
            if dir_path != os.path.abspath(os.path.join(os.getcwd(), temp_dir)):
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    print(f"Не удалось удалить папку {dir_path}: {e}")


def update_program():
    # Проверяем, запущен ли скрипт с правами администратора
    if not is_admin():
        # Если нет, повторно запускаем скрипт с запросом прав администратора
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

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

                # Удалите все файлы и папки в корневой папке, кроме временной папки и update.exe
                delete_files_except_temp_and_update_exe()

                # Загрузите новую версию с GitHub и сохраните как zip-файл
                response = requests.get(download_url)
                response.raise_for_status()

                with open(os.path.join(temp_dir, 'update_files.zip'), 'wb') as zip_file:
                    zip_file.write(response.content)

                # Распакуйте zip-файл в корневую папку
                with zipfile.ZipFile(os.path.join(temp_dir, 'update_files.zip'), 'r') as zip_ref:
                    # Извлеките содержимое, пропустив замену update.exe
                    for file_info in zip_ref.infolist():
                        file_path = os.path.join(os.getcwd(), file_info.filename)
                        if file_info.filename.lower() == 'update.exe' and os.path.exists(file_path):
                            print(f"Пропущена замена файла {file_info.filename}")
                        else:
                            zip_ref.extract(file_info, os.getcwd())
                 # Создаем ярлык для файла VVO.exe на рабочем столе
                create_desktop_shortcut(os.path.join(os.getcwd(), 'VVO.exe'), 'VVO')
                # Обновите версию
                with open(current_version_path, 'w') as current_version_file:
                    current_version_file.write(release_info['tag_name'])

                print("Обновление завершено.")
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
        time.sleep(5)  # Добавим небольшую задержку перед удалением
        shutil.rmtree(temp_dir)

    # Добавим задержку перед закрытием консоли
    input("Нажмите Enter для завершения...")

# Вызовите функцию обновления программы
update_program()
