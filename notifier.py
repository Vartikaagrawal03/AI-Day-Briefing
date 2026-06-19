import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)


def send_email_briefing(briefing_text, recipient_email):
    """Send the briefing as an email to yourself"""

    sender_email = get_secret("GMAIL_SENDER")
    app_password = get_secret("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "📋 Your Daily Briefing"

    msg.attach(MIMEText(briefing_text, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("✅ Briefing email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    test_briefing = "This is a test briefing message."
    send_email_briefing(test_briefing, get_secret("GMAIL_SENDER"))