import smtplib
from email.mime.text import MIMEText

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

# Пример использования функции отправки письма
send_email("Test", "test text", "d.dobin@vvo-gmbh.de")
