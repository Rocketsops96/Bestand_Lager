import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder

# Укажите параметры для SSH-соединения
ssh_host = '45.82.70.15'
ssh_user = 'root'
ssh_password = 'D5v7O1n5M8'
ssh_port = 58374

# Укажите параметры для подключения к базе данных
db_host = '127.0.0.1'  # Хост базы данных
db_user = 'postgres'
db_password = '72219703'
db_name = 'VVO_DB'

def create_conn():
    conn = None
    try:
        # Устанавливаем SSH-соединение
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ssh_host, username=ssh_user, password=ssh_password, port=ssh_port)

        # Устанавливаем SSH-туннель к хосту базы данных
        tunnel = SSHTunnelForwarder(
            ssh_address_or_host=(ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(db_host, 5432)
        )
        tunnel.start()

        # Подключаемся к базе данных через SSH-туннель
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host='127.0.0.1',
            port=tunnel.local_bind_port
        )
        conn.autocommit = True
        print('Подключение к базе данных установлено через SSH!')

    except Exception as e:
        print(f"Ошибка при создании соединения: {e}")

    return conn

def main():
    conn = create_conn()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            print(cursor.fetchone())
        except Exception as e:
            print(f"Ошибка при выполнении SQL-запроса: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
