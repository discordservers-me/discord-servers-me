from django.contrib import admin
from .models import AboutContent

# Register your models here.


class AdminAboutInformation(admin.ModelAdmin):
    list_display = (
        'title'
    )


admin.site.register(AboutContent, AdminAboutInformation)
