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
        'from': 'onboarding@resend.dev',
        'to': email,
        'subject': 'Confirm your hubb account',
        'text': f'Click the link below to confirm your email address. The link expires in 24 hours.\n\n{link}'
    })
