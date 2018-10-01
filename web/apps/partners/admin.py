from django.contrib import admin

# Register your models here.
from .models import PartnersInformation
# Register your models here.


class AdminPartnersInformation(admin.ModelAdmin):
    list_display = (
        'title',
        'description'
    )
    list_editable = (
        'title',
        'description'
    )


admin.site.register(PartnersInformation, AdminPartnersInformation)
