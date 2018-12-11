import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.config.settings')
django.setup()
from django.conf import settings  # noqa
from bot import tasks  # noqa
from bot.bot import DiscordServersShardedClient  # noqa

bot = DiscordServersShardedClient(shard_ids=list(range(6, 8)), shard_count=10, max_messages=101)

# if not settings.DEBUG:
#     bot.loop.create_task(tasks.bump_premium_servers(bot))
#     bot.loop.create_task(tasks.check_changed_manager(bot))
#     bot.loop.create_task(tasks.update_servers_info(bot))

bot.run(settings.BOT_TOKEN)
