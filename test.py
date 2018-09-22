# from pytz import timezone
# from datetime import timedelta, datetime
import asyncio
# from pprint import pprint
# import random
# from math import floor
import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.config.settings')
django.setup()
from web.apps.servers.models import DiscordServer
from random import choices, randint
loop = 100
server_names = ['WHOO', 'HOOOP', 'Server randomness', 'Stuff happend', 'Bla bla server', 'Cool Server']
short_desc = 'Lorem ipsum dono bla bla ay ay blo Lorem ipsum dono bla bla ay ay blo Lorem ipsum dono bla bla ay ay blo'


def test_func():
    print(None in [1, 2, 3])


if __name__ == "__main__":
    test_func()
