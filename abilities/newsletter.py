import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

from .mensa import MensaScraper
import config

FINKENAU_ID = "164"

PERSONAL_MESSAGE = f"""
<br>
<p>Made with <3 by Alex</p>
"""

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
PORT = 587

class Newsletter:

    def __init__(self):
        weekday = time.strftime("%A")
        if weekday != "Friday" and weekday != "Saturday": # Leads to the send function directly returning
            self.meals = MensaScraper(day="morgen", location_id=FINKENAU_ID, style="html").get_meals()

    def send(self):
        if not self.meals:
            return
        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Mensa Speiseplan'
        msg['From'] = config.SENDER
        msg['To'] = config.RECEIVER
        msg.attach(MIMEText(self.meals + PERSONAL_MESSAGE, 'html'))


        # Create a secure SSL/TLS connection
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(config.SENDER, config.APP_PASSWORD)
            server.sendmail(config.SENDER, config.RECEIVER, msg.as_string())
