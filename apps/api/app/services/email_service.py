import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)


def send_email(
    to_email,
    subject,
    html_content
):

    msg = MIMEMultipart()

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(
        MIMEText(
            html_content,
            "html"
        )
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.send_message(msg)


def send_verification_email(
    to_email,
    token
):

    verification_link = (
        f"http://localhost:5173/"
        f"verify-email/{token}"
    )

    html = f"""
    <h2>Welcome to Resolvr AI</h2>

    <p>
    Click below to verify your account:
    </p>

    <a href="{verification_link}">
        Verify Email
    </a>
    """

    send_email(
        to_email,
        "Verify your Resolvr AI account",
        html
    )


def send_password_reset_email(
    to_email,
    token
):

    reset_link = (
        f"http://localhost:5173/"
        f"reset-password/{token}"
    )

    html = f"""
    <h2>Password Reset</h2>

    <p>
    Click below to reset your password:
    </p>

    <a href="{reset_link}">
        Reset Password
    </a>
    """

    send_email(
        to_email,
        "Reset your Resolvr AI password",
        html
    )