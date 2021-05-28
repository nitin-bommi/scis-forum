from flask_mail import Message
from scisforum import mail

def send_message(email, message):
    msg = Message(email,
                  sender='scisforum@gmail.com',
                  recipients=['scisforum@gmail.com'])
    msg.body = message
    mail.send(msg)

def reply_message(email):
    msg = Message('Thank you',
                    sender='scisforum@gmail.com',
                    recipients=[email])
    msg.body = "Thank you for contacting us. We will get back to you soon."
    mail.send(msg)