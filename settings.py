from decouple import config


DEBUG = config('DEBUG', default=False, cast=bool)
BOT_TOKEN = config('BOT_TOKEN')
BOT_ID = config('BOT_ID')
BOT_SECRET = config('BOT_SECRET')
BUMP_DURATION = config('BUMP_DURATION', cast=int)
