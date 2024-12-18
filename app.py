import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import requests

load_dotenv()

# Configuration
# URL = "http://10.0.7.7/plogin"
URL = "http://idp.hse.ie"
CHECK_INTERVAL = 60  # in seconds
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")

def send_email(subject, body):
    """ Function to send email	"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()        
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_website():
    """ Function to check website status """
    try:
        response = requests.get(URL, timeout=10) # timeout is set to 10 seconds
        if response.status_code == 200:
            print(f"Website is up: {datetime.now()}")
            return True, None
        else:
            print(f"Website is down: {datetime.now()}")
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False, str(e)

def main():
    """ Main function """
    website_up = None # None means we don't know the status yet

    while True:
        is_up, error = check_website()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_up and website_up is False:
            send_email("Website is back up", f"The website {URL} is back up as of {current_time}.")
        elif not is_up and website_up is not False:
            send_email("Website is down", f"The website {URL} is down as of {current_time}. Error: {error}")

        website_up = is_up
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
