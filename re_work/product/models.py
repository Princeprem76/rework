from django.db import models

# Create your models here.
from re_work.user.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="Clients_Product", blank=True, null=True)
    video_editor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="editor", blank=True, null=True)
    script_writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="script", blank=True, null=True)
    has_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product_name} ({self.client.name})"
