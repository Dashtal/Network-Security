import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "bit.il.invoice@gmail.com"
PASSWORD = "rxvr sgdi cmec oalf"
VIRUS_URL = "http://localhost:3001/virus"
SUBJECT = "bit - הכסף שהעברת בביט לביבי נתניהו התקבל בהצלחה!"
BODY = f"""\
<html>
  <body dir="rtl">
    <p>שלום רב,<br/>הכסף שהעברת בביט לביבי נתניהו על סך 1,000 שקלים התקבל בהצלחה!<br>
       <a href="{VIRUS_URL}">לצפייה בחשבונית לחץ כאן</a>
    </p>
  </body>
</html>
"""


# ---------------------------------------------------------------------------------------------------------------

def send_email(email: str):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = email
    message["Subject"] = SUBJECT
    message.attach(MIMEText(BODY, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, email, message.as_string())
