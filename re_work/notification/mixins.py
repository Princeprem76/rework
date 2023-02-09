import huey.contrib.djhuey as huey
from push_notifications.exceptions import GCMError
from push_notifications.models import GCMDevice


@huey.db_task(retries=1, retry_delay=5)
def send_push_notification(message, users, product_id, type):
    devices = GCMDevice.objects.filter(user__in=users)
    print(devices)
    extra = {"type": type, "product_id": product_id}
    try:
        devices.send_message(message, extra=extra)
    except GCMError:
        pass