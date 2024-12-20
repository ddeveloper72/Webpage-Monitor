import os
from pathlib import Path
import time
from datetime import datetime
from dotenv import load_dotenv

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

dotenv_path = Path(".env")
load_dotenv()

# Configuration
DEVELOPMENT = os.getenv("DEVELOPMENT")
CHECK_INTERVAL = 30  # in seconds
webhook_url = os.getenv("SLACK_WEBHOOK_URL")


def check_website():
    """Function to check website status"""
    try:
        response = requests.get(URL, timeout=10)  # timeout is set to 10 seconds
        if response.status_code == 200:
            print(f"Website is up: {datetime.now()}")
            return True, None
        else:
            print(f"Website is down: {datetime.now()}")
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False, str(e)


def send_slack_alert(slack_webhook_url, message):
    """Function to send a Slack alert"""
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "NCP-PPT Monitor Alert",
                    "emoji": True,
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": message}},
        ]
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(
            slack_webhook_url, json=payload, headers=headers, timeout=10, verify=False
        )
        if response.status_code != 200:
            print(f"Failed to send Slack alert: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert: {e}")


def main():
    """Main function"""
    website_up = None  # None means we don't know the status yet

    while True:
        is_up, error = check_website()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if is_up and website_up is False:
            send_slack_alert(
                webhook_url, f"*🚀 The website {URL} is back up as of {current_time}.*"
            )
        elif not is_up and website_up is not False:
            send_slack_alert(
                webhook_url,
                f"*The website {URL} is down as of {current_time}.* \n\n*Error:* {error}.",
            )

        website_up = is_up
        time.sleep(CHECK_INTERVAL)


if DEVELOPMENT:
    URL = os.environ.get("URL_DEVELOPMENT")
else:
    URL = os.environ.get("URL_PRODUCTION")

if __name__ == "__main__":
    main()
