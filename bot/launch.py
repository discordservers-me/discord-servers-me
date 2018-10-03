import discord
from pytz import timezone
from django.utils import timezone as django_timezone
import asyncio
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.config.settings')
django.setup()
from web.apps.servers.models import DiscordServer, DiscordEmoji, ServerManager  # noqa
from django.conf import settings  # noqa

guilds_count = DiscordServer.objects.count()

if settings.DEBUG is True:
    prefix = '&*'
else:
    prefix = '&*'

bot = discord.AutoShardedClient(shard_ids=[0, 1, 2, 3, 4], shard_count=5)


@bot.event
async def on_shard_ready(shard_id):
    print(f'Shard {shard_id} loaded.')


@bot.event
async def on_ready():
    print('------')
    print(f'Logged in as: {bot.user.name} (ID: {bot.user.id})')
    print('------')
    exec_guilds = ['287295168053510145', '491296531513868304', '484568851963576320', '495415063591518238', '488026470183206942', '396070717025943562', '489119700366655488', '414061238440427531', '496705067555094558', '495967011067789312',
                   '447211140083089418', '488027329009025025', '471433697548304405', '244193575074660353', '488369913971343416', '352661965807681537', '495704661022474240', '460386326521577483', '495446155518541834', '493955231424446484', '493492672217219094',
                   '494997999299330058', '403691615115411479', '495442859332468747', '432531048270659584', '469628190483283988', '495083249408671754', '469630074061062154', '495717622097117214', '446141543666024449', '484569825205551115',
                   '468234677795160069', '485527631752855553', '495248223217254401', '451371865911328770', '485782160809263124', '480541126470664194', '494809644313739277', '483118377238396929', '495713024271712268', '488501310618861603', '487699416053055489',
                   '493482359543300106', '453182328181620747', '491345846328360960', '496379601384112143', '495747160361664523', '490940712012218374', '196060689415143424', '457681582220771330', '462458737924374548', '473777143617421312', '402831074239053824',
                   '479021791877267476', '482715312630923284', '464752109909311499', '395327343067004928', '485688585966583810', '495706971157037059', '491039338659053568', '414516311406804992', '474394946376433672', '492730281430745089']
    for g_id in exec_guilds:
        guild = bot.get_guild(g_id)
        emojis = guild.emojis
        server_obj = DiscordServer.objects.get(server_id=g_id)
        server_emoji_ids = []
        # check if emoji exists in db, create if not
        for emoji in emojis:
            emoji_id = str(emoji.id)
            server_emoji_ids.append(emoji_id)
            server_emoji, emoji_created = DiscordEmoji.objects.update_or_create(
                server=server_obj,
                emoji_id=emoji_id,
                defaults={
                    'name': emoji.name,
                    'url': emoji.url,
                    'require_colons': emoji.require_colons,
                    'animated': emoji.animated
                }
            )
            if emoji_created:
                print(f'Emoji {server_emoji.name} stored.')

        # then check if emojis in db exist in server emoji list, delete if not
        db_emojis = DiscordEmoji.objects.filter(server__server_id=g_id)
        for db_emoji in db_emojis:
            if db_emoji.emoji_id not in server_emoji_ids:
                print(f'Emoji ({db_emoji.name}) deleted.')
                db_emoji.delete()
    # if not settings.DEBUG:
    #     # change this for the 'Playing xxx' status
    #     presence = f'Prefix: r!'
    #     await bot.change_presence(game=discord.Game(name=presence))


@bot.event
async def on_guild_join(guild):
    update_or_create_server(guild)
    print(f'Joined guild: {guild.name}')


@bot.event
async def on_guild_remove(guild):
    server_id = guild.id

    try:
        server_obj = DiscordServer.objects.get(server_id=server_id)
        # delete the guild (server) from database, and all related database
        # like emojis
        server_obj.delete()
        print(f'Removed from guild: {guild.name}. Data deleted.')
    except DiscordServer.DoesNotExist:
        print(f'This server (ID: {server_id}) does not exist in Database.')


@bot.event
async def on_guild_update(guild_before, guild_after):
    update_or_create_server(guild_after)
    print(f'Guild [{guild_after.name}] updated')


# @bot.event
# async def on_member_join(member):
#     update_or_create_server(member.guild)
#     print(f'Guild [{member.guild.name}]\'s member count increased.')


# @bot.event
# async def on_member_remove(member):
#     update_or_create_server(member.guild)
#     print(f'Guild [{member.guild.name}]\'s member count decreased.')


@bot.event
async def on_server_emojis_update(before, after):
    # try to get the server object from database
    # return if not exist (can't sync without server object)
    try:
        if before:
            server_obj = DiscordServer.objects.get(server_id=str(before[0].guild_id))
        else:
            server_obj = DiscordServer.objects.get(server_id=str(after[0].guild_id))
    except DiscordServer.DoesNotExist:
        print('DiscordServer does not exist.')
        return

    # logic to decide if an emoji is added or deleted
    deleted = []
    added = []
    for e in before:
        if e not in after:
            deleted.append(e)

    for e in after:
        if e not in before:
            added.append(e)

    if deleted:
        for e in deleted:
            try:
                db_emoji = DiscordEmoji.objects.get(emoji_id=e.id)
                print(f'Emoji {db_emoji.emoji} deleted.')
                db_emoji.delete()
            except DiscordEmoji.DoesNotExist:
                # not exists, no more actions needed
                pass

    elif added:
        for e in added:
            server_emoji, created = DiscordEmoji.objects.update_or_create(
                server=server_obj,
                emoji_id=e.id,
                defaults={
                    'emoji': e.name,
                    'emoji_url': e.url,
                    'require_colons': e.require_colons,
                    'animated': e.animated
                }
            )
            if created:
                print(f'Emoji {server_emoji.emoji} stored.')
    # updated existing emoji (change name)
    else:
        before_as_name = []
        after_as_name = []
        for e in before:
            before_as_name.append(e.name)

        for e in after:
            after_as_name.append(e.name)

        after_update = list(set(after_as_name) - set(before_as_name))[0]
        before_update = list(set(before_as_name) - set(after_as_name))[0]
        try:
            updated_emoji = DiscordEmoji.objects.get(server=server_obj, emoji=before_update)
        except DiscordEmoji.DoesNotExist:
            print('DiscordEmoji does not exist.')
            return
        updated_emoji.emoji = after_update
        updated_emoji.save()
        print(f'Updated emoji "{updated_emoji.emoji}" from "{before_update}"')


def update_or_create_server(guild):
    member_count = guild.member_count
    server_id = str(guild.id)
    server_name = guild.name
    server_creation_date = guild.created_at.replace(tzinfo=timezone('UTC'))
    icon_url = guild.icon_url
    # owner_id = str(guild.owner_id)
    # print(owner_id, type(owner_id))

    # update (if found with server_id) or create the server
    # into database with the above information
    server_obj, server_created = DiscordServer.objects.update_or_create(
        server_id=server_id,
        defaults={
            'name': server_name,
            'creation_date': server_creation_date,
            'icon_url': icon_url,
            'member_count': member_count,
        }
    )

    # ONE-TIME RUN, when joining the server
    # updating the server managers will be done in a scheduled task
    # to avoid consuming resources
    if server_created:
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

        db_managers = ServerManager.objects.filter(server=server_obj)
        for db_manager in db_managers:
            if db_manager.manager_id not in manager_ids:
                print(f'Manager with ID {db_manager.manager_id} deleted (Server: {server_obj.name}).')
                db_manager.delete()

    # ONE-TIME RUN, when joining the server
    if server_created:
        emojis = guild.emojis
        server_emoji_ids = []
        # check if emoji exists in db, create if not
        for emoji in emojis:
            emoji_id = str(emoji.id)
            server_emoji, emoji_created = DiscordEmoji.objects.update_or_create(
                server=server_obj,
                emoji_id=emoji_id,
                defaults={
                    'name': emoji.name,
                    'url': emoji.url,
                    'require_colons': emoji.require_colons,
                    'animated': emoji.animated
                }
            )
            if emoji_created:
                print(f'Emoji {server_emoji.name} stored.')
            server_emoji_ids.append(emoji_id)

        # then check if emojis in db exist in server emoji list, delete if not
        db_emojis = DiscordEmoji.objects.filter(server__server_id=server_id)
        for db_emoji in db_emojis:
            if db_emoji.emoji_id not in server_emoji_ids:
                print(f'Emoji ({db_emoji.name}) deleted.')
                db_emoji.delete()


async def bump_premium_servers():
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
                print(f'Server with ID [{server_id}] does not exist in database.')
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
                    print(f'Manager with ID {db_manager.manager_id} deleted (Server: {server_obj.name}).')
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
        print(f'Guild Update Done.')


if not settings.DEBUG:
    bot.loop.create_task(bump_premium_servers())
    bot.loop.create_task(check_changed_manager(bot))
    bot.loop.create_task(update_servers_info(bot))
    # pass


if settings.DEBUG:
    bot.loop.create_task(bump_premium_servers())
    bot.loop.create_task(check_changed_manager(bot))
    bot.loop.create_task(update_servers_info(bot))

bot.run(settings.BOT_TOKEN)
