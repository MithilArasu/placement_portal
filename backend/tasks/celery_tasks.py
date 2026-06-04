
from celery import Celery

celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery.task
def send_drive_notification(drive_title):

    print(
        f"Notification sent for drive: {drive_title}"
    )

    return True