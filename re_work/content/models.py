import datetime

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
    comment = models.ManyToManyField(Comments, related_name="Content_Comment")
    comment_off = models.BooleanField(default=False)
    comment_time = models.DateTimeField(null=True, blank=True)

    def turn_off_comment(self):
        if self.comment_time is not None:
            if self.comment_time <= datetime.datetime.now():
                self.comment_off = True
            else:
                self.comment_off = False
        else:
            self.comment_off = True
        self.save()
        return self.comment_off


class VideoContent(CommonContent, models.Model):
    duration = models.CharField(max_length=50, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    has_approved = models.BooleanField(default=False)


class FileContent(CommonContent, models.Model):
    files = models.URLField(null=True, blank=True)
    has_approved = models.BooleanField(default=False)


class PreProductionContent(models.Model):
    file_contents = models.ManyToManyField(FileContent, related_name="file_content")
    location = models.ManyToManyField(CommonContent, related_name="location")
    props = models.ManyToManyField(CommonContent, related_name="props")
    model = models.ManyToManyField(CommonContent, related_name="model")
    has_location = models.BooleanField(default=True)
    has_props = models.BooleanField(default=True)
    has_file = models.BooleanField(default=True)
    has_model = models.BooleanField(default=True)
    complete_location = models.BooleanField(default=False)
    complete_props = models.BooleanField(default=False)
    complete_file = models.BooleanField(default=False)
    complete_model = models.BooleanField(default=False)

    def total_contents(self):
        count = 0
        if self.has_file:
            count += 1
        if self.has_props:
            count += 1
        if self.has_model:
            count += 1
        if self.has_location:
            count += 1
        return count

    def total_complete(self):
        count = 0
        if self.complete_file:
            count += 1
        if self.complete_props:
            count += 1
        if self.complete_model:
            count += 1
        if self.complete_location:
            count += 1
        return count


class ProductionContent(models.Model):
    video_completion = models.DateTimeField(null=True, blank=True)
    complete_video = models.BooleanField(default=False)

    def total_complete(self):
        count = 0
        if self.complete_video:
            count += 1
        return count


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

    def total_contents(self):
        count = 0
        if self.has_internal:
            count += 1
        if self.has_delivery:
            count += 1
        if self.has_editing:
            count += 1
        return count

    def total_complete(self):
        count = 0
        if self.complete_internal:
            count += 1
        if self.complete_delivery:
            count += 1
        if self.complete_editing:
            count += 1
        return count


class Section(models.Model):
    product = models.ForeignKey(Product, related_name="products_name", on_delete=models.SET_NULL, null=True, blank=True)
    video_content = models.ManyToManyField(VideoContent, related_name="Video_Content")
    pre_contents = models.ManyToManyField(PreProductionContent, related_name="pre_production_content")
    production_contents = models.ManyToManyField(ProductionContent, related_name="production_content")
    post_contents = models.ManyToManyField(PostProductionContent, related_name="post_production_content")

    def total_contents(self):
        count = self.pre_contents.all().first().total_contents() + self.post_contents.all().first().total_contents() + 1
        return count

    def total_complete(self):
        count = self.pre_contents.all().first().total_complete() + self.production_contents.all().first().total_complete() + self.post_contents.all().first().total_complete()
        return count
