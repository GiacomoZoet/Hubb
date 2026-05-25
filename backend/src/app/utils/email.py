import os
import resend
from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def _base_html(title, heading, body_content, cta_label, cta_url, expiry_note):
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0fafa;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f0fafa;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.08);">

        <!-- Header -->
        <tr>
          <td style="background:#0d8e84;padding:32px 40px;text-align:center;">
            <span style="font-size:32px;font-weight:900;color:#ffffff;letter-spacing:-1px;">hubb</span>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:40px 40px 24px;">
            <h1 style="margin:0 0 12px;font-size:22px;color:#111827;">{heading}</h1>
            <p style="margin:0 0 28px;font-size:15px;color:#4b5563;line-height:1.6;">{body_content}</p>
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="border-radius:8px;background:#0d8e84;">
                  <a href="{cta_url}" style="display:inline-block;padding:14px 32px;font-size:15px;font-weight:700;color:#ffffff;text-decoration:none;">{cta_label}</a>
                </td>
              </tr>
            </table>
            <p style="margin:24px 0 0;font-size:13px;color:#9ca3af;">{expiry_note}</p>
            <p style="margin:12px 0 0;font-size:12px;color:#d1d5db;word-break:break-all;">
              If the button doesn't work, copy this link:<br>
              <a href="{cta_url}" style="color:#0d8e84;">{cta_url}</a>
            </p>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f9fafb;padding:20px 40px;border-top:1px solid #e5e7eb;text-align:center;">
            <p style="margin:0;font-size:12px;color:#9ca3af;">
              You received this email because an account was created or a request was made on hubb.<br>
              If this wasn't you, you can safely ignore this email.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def send_confirmation_email(email):
    resend.api_key = os.getenv('RESEND_API_KEY')
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt='email-confirm')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    link = f'{frontend_url}/confirm/{token}'

    html = _base_html(
        title='Confirm your hubb account',
        heading='Confirm your email address',
        body_content='Thanks for signing up! Click the button below to confirm your email address and activate your hubb account.',
        cta_label='Confirm my account',
        cta_url=link,
        expiry_note='This link expires in 24 hours.',
    )

    resend.Emails.send({
        'from': 'noreply@giacomozoet.dev',
        'to': email,
        'subject': 'Confirm your hubb account',
        'html': html,
        'text': f'Confirm your hubb account\n\nClick the link below to confirm your email address. The link expires in 24 hours.\n\n{link}',
    })


def send_reset_email(email):
    resend.api_key = os.getenv('RESEND_API_KEY')
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(email, salt='password-reset')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    link = f'{frontend_url}/reset-password/{token}'

    html = _base_html(
        title='Reset your hubb password',
        heading='Reset your password',
        body_content='We received a request to reset the password for your hubb account. Click the button below to choose a new password.',
        cta_label='Reset my password',
        cta_url=link,
        expiry_note='This link expires in 1 hour. If you did not request a password reset, no action is needed.',
    )

    resend.Emails.send({
        'from': 'noreply@giacomozoet.dev',
        'to': email,
        'subject': 'Reset your hubb password',
        'html': html,
        'text': f'Reset your hubb password\n\nClick the link below to reset your password. The link expires in 1 hour.\n\n{link}',
    })
