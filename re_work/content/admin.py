from django.contrib import admin

# Register your models here.
from re_work.content.models import Comments, PreProductionContent, ProductionContent, PostProductionContent, Section, \
    CommonContent, VideoContent, FileContent

admin.site.register(
    [Comments, PreProductionContent, ProductionContent, PostProductionContent, Section, CommonContent, VideoContent,
     FileContent])
