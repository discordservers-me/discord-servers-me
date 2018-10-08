import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.config.settings')
django.setup()
from django.conf import settings  # noqa
from bot import tasks  # noqa
from bot.bot import DiscordServersShardedClient  # noqa

bot = DiscordServersShardedClient(shard_ids=list(range(3, 6)), shard_count=6, max_messages=101)

bot.run(settings.BOT_TOKEN)
