from django.contrib import admin
from .models import GiveawayInformation
# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

# Apply summernote to all TextField in model.


class AdminGiveawayInformation(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('description',)
    list_display = (
        'title',
        'ended',
        'updated_at',
        'created_at',

    )


admin.site.register(GiveawayInformation, AdminGiveawayInformation)
