import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
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

def send_email(subject, body, to_email, attachment_path=""):
   
    gmail_user = "mrdmitrey1996@gmail.com"  # Замените на ваш адрес Gmail
    app_password = "bzxthjyafehethmd"  # Замените на ваше приложение-пароль

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email

    try:
        # Подключение к серверу Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # Вход в учетную запись Gmail с использованием приложения-пароля
        server.login(gmail_user, app_password)

        # Отправка письма
        server.sendmail(gmail_user, to_email, msg.as_string())
        print("Письмо успешно отправлено!")

    except smtplib.SMTPException as e:
        print("Ошибка при отправке письма:", e)

    finally:
        # Закрытие соединения с сервером
        server.quit()

def check_bau():
    conn = create_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name_bau, kostenstelle_vvo, bauvorhaben, ort, strasse, ausfurung_von, ausfurung_bis, vrao_ab, vrao_bis, ansprechpartner FROM Bau ")
    data = cursor.fetchall()
    current_date = datetime.now().date()
    for row in data:
        ausfurung_von = row[6]
        ausfurung_date = datetime.strptime(ausfurung_von, '%d.%m.%Y').date()
        days_until_due = (ausfurung_date - current_date).days
        # Если остается 7 дней или менее до даты, выводим kostenstelle_vvo в консоль
        if 0 <= days_until_due <= 7:
            print("Kostenstelle_vvo:", row[2])
            bau=row[2]
            name_bau = row[1]
            send_email("ACHTUNG", f"Bis zum Baubeginn {bau} - {name_bau} verbleiben noch {days_until_due} Tage. Vergessen Sie nicht, ein Parkverbot festzulegen, falls vorhanden. \nHerzliche Grüße, Ihr VVO-Roboter", "d.dobin@vvo-gmbh.de")
check_bau()

