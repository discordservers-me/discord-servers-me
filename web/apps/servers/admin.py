from django.contrib import admin
from .models import DiscordServer, DiscordEmoji, ServerTag, ServerManager
# Register your models here.


class AdminDiscordServer(admin.ModelAdmin):
    list_display = (
        'name',
        'member_count',
        'premium_tier',
        'server_id',
        'icon_url',
        'bumped_at',
    )

    list_editable = (
        'member_count',
        'premium_tier',
        'bumped_at',
    )


class AdminDiscordEmoji(admin.ModelAdmin):
    list_display = (
        'name',
        'emoji_id',
        'url',
        'require_colons',
        'server'
    )


class AdminServerManager(admin.ModelAdmin):
    list_display = (
        'manager_id',
        'server',
    )


class AdminServerTag(admin.ModelAdmin):
    list_display = (
        '__str__',
        'name',
        'material_icon',
        'created_at',
    )

    list_editable = (
        'name',
        'material_icon',
    )


admin.site.register(DiscordServer, AdminDiscordServer)
admin.site.register(DiscordEmoji, AdminDiscordEmoji)
admin.site.register(ServerManager, AdminServerManager)
admin.site.register(ServerTag, AdminServerTag)
