from flask_mail import Message
from scisforum import mail

def send_message(email, message):
    msg = Message(email,
                  sender='imtech2k18@gmail.com',
                  recipients=['imtech2k18@gmail.com'])
    msg.body = message
    mail.send(msg)
