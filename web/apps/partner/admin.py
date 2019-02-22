from django.contrib import admin
from .models import PartnerInformation

# Register your models here.


class AdminPartnerInformation(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'url'
    )


admin.site.register(PartnerInformation, AdminPartnerInformation)
