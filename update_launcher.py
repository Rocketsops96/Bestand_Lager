import subprocess
import sys
import time


def run_update_script():
    # Запуск процесса обновления
    print("Запуск процесса обновления...")
    update_script_path = "update.py"  # Замените на фактический путь к вашему update.py
    subprocess.run([sys.executable, update_script_path])
    time.sleep(25)
    run_updated_app()

def run_updated_app():
    # Запуск новой версии приложения
    app_script_path = "VVO.exe"  # Замените на фактический путь к вашему BestandLager.py
    subprocess.run([sys.executable, app_script_path])
    print("Обновление завершено. Запуск новой версии приложения...")
run_update_script()




