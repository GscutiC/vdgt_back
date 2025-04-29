from flask_mail import Message
from flask import current_app
from flask_mail import Mail

mail = Mail()

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error al enviar correo: {e}")