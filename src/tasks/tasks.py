import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from src.config import settings
from src.tasks.celery_config import celery_app
from src.tasks.email_templates import create_confirmation_template


@celery_app.task
def resize_image(
    image_path: str
):
    image_path = Path(image_path)
    image = Image.open(image_path)
    resized_image = image.resize((300, 150))
    with open(f"src/static/images/resized_{image_path.name}", "wb") as file:
        resized_image.save(file)


@celery_app.task
def send_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
