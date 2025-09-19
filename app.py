import os
import smtplib
import sqlite3 
from email.message import EmailMessage
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)


SENDER_EMAIL = "qplayzx@gmail.com"
SENDER_PASSWORD = "umir titg dsgw wjus"
RECIPIENT_EMAIL = "sensiblegdev@gmail.com"

@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not all([name, email, message]):
        return "Ошибка: Пожалуйста, заполните все поля.", 400

    try:
   
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO requests (name, email, message, timestamp)
            VALUES (?, ?, ?, ?)
        """, (name, email, message, datetime.utcnow()))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка при сохранении в БД: {e}")
        return f"Произошла ошибка на сервере при сохранении данных: {e}", 500
    

    msg = EmailMessage()
    msg['Subject'] = f"Новое сообщение с сайта CareLine AI от {name}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    formatted_message = message.replace('\n', '<br>')
    email_body = f"""
     Новое сообщение с контактной формы CareLine AI
         Имя: {name}
         Email для ответа: {email}
         Сообщение:
         {formatted_message}
    """
    msg.set_payload(email_body, charset='utf-8')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return "Спасибо! Ваше сообщение успешно отправлено."
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        return f"Произошла ошибка при отправке сообщения: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)


