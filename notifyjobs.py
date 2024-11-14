import requests
import smtplib
import time
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "jobpostings69420lol@gmail.com"
RECEIVER_EMAIL = "benson195440@gmail.com"
PASSWORD = "lrzn ezip kwxx hgzq"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SUBJECT = "New Job Posting!"
MESSAGE = "Default Message"
GITHUB_URL = "https://github.com/SimplifyJobs/New-Grad-Positions"
SECONDS_TO_SLEEP = 120


def get_recent_job(s):
    match = re.search(r"<td><strong>(.*?)</strong></td>", s, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None


def fetch_html(url=GITHUB_URL):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None


def notify(
    sender=SENDER_EMAIL,
    receiver=RECEIVER_EMAIL,
    password=PASSWORD,
    subject=SUBJECT,
    message=MESSAGE,
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")


def run(seconds_to_sleep=SECONDS_TO_SLEEP):
    previous_job = None
    run_number = 1
    while True:
        html = fetch_html()
        job = get_recent_job(html)
        if job != previous_job:
            notify(message=f"{job} just posted a new job.")
            previous_job = job
            print(f"Run #{run_number}: {job}")
        else:
            print(f"Run #{run_number}: ---------")
        run_number += 1
        time.sleep(seconds_to_sleep)


run()
