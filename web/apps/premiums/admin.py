from django.contrib import admin
from .models import PremiumTier, PremiumFeature
# Register your models here.


class AdminPremiumFeature(admin.ModelAdmin):
    list_display = (
        'tier',
        # 'icon',
        # 'icon_color',
        # 'background_color',
        'ordering',
        'short_description',
        'description',
        'updated_at'
    )
    list_editable = (
        # 'icon',
        # 'icon_color',
        # 'background_color',
        'ordering',
        'short_description',
        'description'
    )


admin.site.register(PremiumTier)
admin.site.register(PremiumFeature, AdminPremiumFeature)
