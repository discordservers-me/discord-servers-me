from django.contrib import admin
from .models import AboutContent
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class AdminAboutInformation(SummernoteModelAdmin):
    summernote_fields = ('description')
    list_display = ['title']


admin.site.register(AboutContent, AdminAboutInformation)
