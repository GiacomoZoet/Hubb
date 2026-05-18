import os
import resend
from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def send_confirmation_email(email):
    resend.api_key = os.getenv('RESEND_API_KEY')
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt='email-confirm')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    link = f'{frontend_url}/confirm/{token}'

    resend.Emails.send({
        'from': 'noreply@giacomozoet.dev',
        'to': email,
        'subject': 'Confirm your hubb account',
        'text': f'Click the link below to confirm your email address. The link expires in 24 hours.\n\n{link}'
    })


def send_reset_email(email):
    resend.api_key = os.getenv('RESEND_API_KEY')
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt='password-reset')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    link = f'{frontend_url}/reset-password/{token}'

    resend.Emails.send({
        'from': 'noreply@giacomozoet.dev',
        'to': email,
        'subject': 'Reset your hubb password',
        'text': f'Click the link below to reset your password. The link expires in 1 hour.\n\n{link}'
    })
