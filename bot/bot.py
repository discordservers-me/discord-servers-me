import discord
from pytz import timezone
from bot import tasks  # noqa
from web.apps.servers.models import DiscordServer, DiscordEmoji, ServerManager  # noqa
from django.conf import settings  # noqa


class DiscordServersShardedClient(discord.AutoShardedClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.DEBUG:
            self.loop.create_task(tasks.check_changed_manager(self))
            self.loop.create_task(tasks.update_servers_info(self))

    async def on_shard_ready(self, shard_id):
        print(f'Shard {shard_id} loaded.')

    async def on_ready(self):
        print('------')
        print(f'Logged in as: {self.user.name} (ID: {self.user.id})')
        print(f'Shards managing {len(self.guilds)} guilds.')
        print('------')
        await self.fetch_zero_emoji_servers_with_emojis()

    async def on_guild_join(self, guild):
        self.update_or_create_server(guild)
        print(f'Joined guild: {guild.name}')

    async def on_guild_remove(self, guild):
        server_id = guild.id

        try:
            server_obj = DiscordServer.objects.get(server_id=server_id)
            # delete the guild (server) from database, and all related database
            # like emojis
            server_obj.delete()
            print(f'Removed from guild: {guild.name}. Data deleted.')
        except DiscordServer.DoesNotExist:
            print(f'This server (ID: {server_id}) does not exist in Database.')

    async def on_guild_update(self, guild_before, guild_after):
        self.update_or_create_server(guild_after)
        print(f'Guild [{guild_after.name}] updated')

    async def on_server_emojis_update(self, before, after):
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

    def update_or_create_server(self, guild):
        member_count = guild.member_count
        server_id = str(guild.id)
        server_name = guild.name
        server_creation_date = guild.created_at.replace(tzinfo=timezone('UTC'))
        icon_url = guild.icon_url

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

    async def fetch_zero_emoji_servers_with_emojis(self):
        await self.wait_until_ready()
        exec_guilds = []
        zeg = DiscordServer.objects.all()
        for g in zeg:
            if g.emoji_count() == 0:
                exec_guilds.append(g)

        print('Updating 0-emoji-count servers...')
        for g_obj in exec_guilds:
            guild = self.get_guild(int(g_obj.server_id))

            if guild is None:
                continue
            emojis = guild.emojis
            server_emoji_ids = []
            # check if emoji exists in db, create if not
            for emoji in emojis:
                emoji_id = str(emoji.id)
                server_emoji_ids.append(emoji_id)
                server_emoji, emoji_created = DiscordEmoji.objects.update_or_create(
                    server=g_obj,
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
            db_emojis = DiscordEmoji.objects.filter(server__server_id=g_obj.server_id)
            for db_emoji in db_emojis:
                if db_emoji.emoji_id not in server_emoji_ids:
                    print(f'Emoji ({db_emoji.name}) deleted.')
                    db_emoji.delete()
        print('0-emoji-count Servers Update Done.')
