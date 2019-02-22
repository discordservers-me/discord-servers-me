from pytz import timezone
from django.utils import timezone as django_timezone
import asyncio
from web.apps.servers.models import DiscordServer, DiscordEmoji, ServerManager  # noqa
from django.conf import settings


async def bump_premium_servers(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(settings.BUMP_DURATION)
        now = django_timezone.now()
        tier1 = DiscordServer.objects.filter(premium_tier=1).order_by('bumped_at')[:4]
        tier2 = DiscordServer.objects.filter(premium_tier=2).order_by('bumped_at')[:7]
        servers = (list(tier1) + list(tier2))
        print(f'Bumping {len(servers)} premium servers...')
        for server in servers:
            premium_tier = server.check_premium()
            if premium_tier == 0:
                pass
            else:
                server.bumped_at = now
                server.save()
                print(f'Bumped server: {server.name}')
        print('Bumping Premium Servers Done.')


async def check_changed_manager(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(settings.UPDATE_MANAGERS_DURATION)
        guilds = bot.guilds
        print(f'Looping through {len(guilds)} guilds to check for changed managers...')
        for guild in guilds:

            server_id = str(guild.id)
            try:
                server_obj = DiscordServer.objects.get(server_id=server_id)
            except DiscordServer.DoesNotExist:
                print(f'Guild does not exist. (ID: {server_id})')
                continue

            # print(f'Looping through members in guild [{guild.name}]...')

            manager_ids = []
            for member in guild.members:
                if member.guild_permissions.manage_guild and not member.bot:
                    manager, manager_created = ServerManager.objects.get_or_create(
                        manager_id=member.id,
                        server=server_obj
                    )
                    if manager_created:
                        print(f'Manager added: {member.display_name} (ID: {member.id} | Server: {server_obj.name}).')
                    manager_ids.append(str(member.id))

            # print('Looping done.')

            db_managers = ServerManager.objects.filter(server=server_obj)
            for db_manager in db_managers:
                if db_manager.manager_id not in manager_ids:
                    print(f'Manager removed. (ID: {db_manager.manager_id} | Server: {server_obj.name}).')
                    db_manager.delete()
        print('Manager Change Done.')


async def update_servers_info(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(settings.UPDATE_SERVERS_INFO)
        guilds = bot.guilds
        print(f'Updating {len(guilds)} guilds...')
        for guild in guilds:

            member_count = guild.member_count
            server_id = str(guild.id)
            server_name = guild.name
            server_creation_date = guild.created_at.replace(tzinfo=timezone('UTC'))
            icon_url = guild.icon_url

            server_obj, server_created = DiscordServer.objects.update_or_create(
                server_id=server_id,
                defaults={
                    'name': server_name,
                    'creation_date': server_creation_date,
                    'icon_url': icon_url,
                    'member_count': member_count,
                }
            )
            if server_created:
                print(f'Guild added: {server_obj.name} (ID: {server_obj.server_id}).')
        print(f'Guild Update Done.')
