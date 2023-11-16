import psycopg2

host = '45.82.70.15'
user = "postgres"
password = '72219703'
db_name = 'VVO_DB'

conn = None

def create_conn():
    global conn
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    conn.autocommit = True
    print('Connection with DB created!')
    return conn;

