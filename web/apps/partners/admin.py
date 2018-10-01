from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PartnersInformation
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

# Apply summernote to all TextField in model.


class AdminPartnersInformation(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('description',)
    list_display = (
        'title'
    )


admin.site.register(PartnersInformation, AdminPartnersInformation)
