from django.db import models
from re_work.core.models import TimeStampAbstractModel
from re_work.user.models import User


class Notifications(TimeStampAbstractModel):
    created_by = models.ForeignKey(User, related_name="Creator", on_delete=models.CASCADE)
    notification_text = models.TextField()
    push_date_time = models.DateTimeField()
