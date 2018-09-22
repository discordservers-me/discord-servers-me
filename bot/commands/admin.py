import json
import discord
from discord.ext import commands

from django.db.models import F

import settings


class Admin:
    """Command package for admin only"""

    def __init__(self, bot):
        self.bot = bot

    def add_space(self, no_of_spaces):
        spaces = ''
        while no_of_spaces >= 0:
            spaces += ' '
            no_of_spaces -= 1
        return spaces


def setup(bot):
    bot.add_cog(Admin(bot))
