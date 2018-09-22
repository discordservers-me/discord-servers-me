from database.bot_models.models import Player


def check_user_in_db(user_id, user_name):
    """
    Check if the user is already in Database.
    If not, create one based on the discord_id and discord_name.
    Return the Player object.
    """
    player, created = Player.objects.get_or_create(discord_id=user_id, defaults={'discord_name': user_name})
    if player.discord_name != user_name:
        player.discord_name = user_name
        player.save()
    return player
