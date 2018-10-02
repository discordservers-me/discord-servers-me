from django.contrib import admin
from .models import PartnersInformation

# Register your models here.


class AdminPartnersInformation(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'url'
    )


admin.site.register(PartnersInformation, AdminPartnersInformation)
