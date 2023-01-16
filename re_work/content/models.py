from django.db import models

# Create your models here.
from re_work.core.models import TimeStampAbstractModel
from re_work.product.models import Product
from re_work.user.models import User


class Comments(TimeStampAbstractModel):
    user = models.ForeignKey(User, related_name="Commenter", on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField()
    parents = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)


class CommonContent(TimeStampAbstractModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    comment = models.ForeignKey(Comments, related_name="Comments", on_delete=models.CASCADE, null=True, blank=True)


class VideoContent(CommonContent, models.Model):
    duration = models.TimeField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)


class FileContent(CommonContent, models.Model):
    files = models.URLField(null=True, blank=True)


class PreProductionContent(models.Model):
    file_contents = models.ManyToManyField(FileContent, related_name="file_content")
    location = models.ManyToManyField(CommonContent, related_name="location")
    props = models.ManyToManyField(CommonContent, related_name="props")
    model = models.ManyToManyField(CommonContent, related_name="model")
    has_video = models.BooleanField(default=True)
    has_location = models.BooleanField(default=True)
    has_props = models.BooleanField(default=True)
    has_file = models.BooleanField(default=True)
    has_model = models.BooleanField(default=True)
    complete_video = models.BooleanField(default=False)
    complete_location = models.BooleanField(default=False)
    complete_props = models.BooleanField(default=False)
    complete_file = models.BooleanField(default=False)
    complete_model = models.BooleanField(default=False)


class ProductionContent(models.Model):
    video_completion = models.DateTimeField(null=True, blank=True)
    complete_video = models.BooleanField(default=False)


class PostProductionContent(models.Model):
    editing = models.ManyToManyField(CommonContent, related_name="editing")
    internal = models.ManyToManyField(CommonContent, related_name="internal_feedback")
    delivery = models.DateTimeField(blank=True, null=True)
    has_editing = models.BooleanField(default=True)
    has_internal = models.BooleanField(default=True)
    has_delivery = models.BooleanField(default=True)
    complete_editing = models.BooleanField(default=False)
    complete_internal = models.BooleanField(default=False)
    complete_delivery = models.BooleanField(default=False)


class Section(models.Model):
    product = models.ForeignKey(Product, related_name="products_name", on_delete=models.SET_NULL, null=True, blank=True)
    video_content = models.ManyToManyField(VideoContent, related_name="Video_Content")
    pre_contents = models.ManyToManyField(PreProductionContent, related_name="pre_production_content")
    production_contents = models.ManyToManyField(ProductionContent, related_name="production_content")
    post_contents = models.ManyToManyField(PostProductionContent, related_name="post_production_content")
