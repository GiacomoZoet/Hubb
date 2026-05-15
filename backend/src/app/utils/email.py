import os
from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app import mail


def send_confirmation_email(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt='email-confirm')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    link = f'{frontend_url}/confirm/{token}'

    msg = Message(
        subject='Confirm your hubb account',
        recipients=[email],
        body=f'Click the link below to confirm your email address. The link expires in 24 hours.\n\n{link}'
    )
    mail.send(msg)
