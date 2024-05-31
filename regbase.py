import psycopg2

host = '212.86.115.157'
user = "postgres"
password = 'DD1710dd'
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

