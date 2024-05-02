import time

from config import celery_app


@celery_app.task
def send_email():
    print("Sending email...")
    time.sleep(5)
    print("Email is sent...")
