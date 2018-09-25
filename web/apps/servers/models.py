from django.db import models
from os.path import splitext
from django.utils import timezone
# Create your models here.


class ServerTag(models.Model):
    name = models.CharField(max_length=16)
    material_icon = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DiscordServer(models.Model):

    PREMIUM_HIGHTLIGHT_CHOICES = (
        (0, 'No Highlight'),
        (1, 'Yellow - Premium Tier 1 + 2'),
        (2, 'Pink - Premium Tier 1 + 2'),
        (3, 'Red - Premium Tier 2'),
    )

    server_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    member_count = models.IntegerField(blank=True, null=True)
    icon_url = models.URLField(blank=True)
    icon = models.ImageField(upload_to='server_icons', blank=True, null=True)

    premium_tier = models.IntegerField(default=0)
    premium_highlight = models.IntegerField(default=0, choices=PREMIUM_HIGHTLIGHT_CHOICES)
    premium_1_from = models.DateTimeField(blank=True, null=True)
    premium_1_until = models.DateTimeField(blank=True, null=True)
    premium_2_from = models.DateTimeField(blank=True, null=True)
    premium_2_until = models.DateTimeField(blank=True, null=True)

    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    shown = models.BooleanField(default=False)
    bumped_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    invite_link = models.URLField(blank=True)
    website = models.URLField(blank=True)

    tags = models.ManyToManyField(ServerTag, related_name='servers', blank=True)

    def __str__(self):
        return self.name

    def emoji_count(self):
        return self.emojis.count()

    def manager_ids(self):
        return self.managers.values_list('manager_id', flat=True)

    def icon_512(self):
        link, ext = splitext(self.icon_url)
        return f'{link}.png?size=512'

    def icon_256(self):
        link, ext = splitext(self.icon_url)
        return f'{link}.png?size=256'

    def icon_128(self):
        link, ext = splitext(self.icon_url)
        return f'{link}.png?size=128'

    def tier_1_expired(self):
        if self.premium_1_until:
            now = timezone.now()
            expired = (now - self.premium_1_until).total_seconds()
            if expired > 0:
                return True
            else:
                return False
        else:
            return True

    def tier_2_expired(self):
        if self.premium_2_until:
            now = timezone.now()
            expired = (now - self.premium_2_until).total_seconds()
            if expired > 0:
                return True
            else:
                return False
        else:
            return True

    def check_premium(self):
        """Returns the Tier after checking and down tier of the server if needed"""
        if self.tier_2_expired():
            if self.tier_1_expired():
                self.premium_tier = 0
                self.premium_1_from = None
                self.premium_1_until = None
                self.premium_2_from = None
                self.premium_2_until = None
                self.premium_highlight = 0
                self.save()
                return 0
            else:
                self.premium_tier = 1
                self.premium_2_from = None
                self.premium_2_until = None
                if self.premium_highlight == 3:
                    self.premium_highlight = 2
                self.save()
                return 1
        else:
            return 2

    def premium_css(self):
        if self.premium_highlight == 1:
            return 'premium-highlight-1'
        elif self.premium_highlight == 2:
            return 'premium-highlight-2'
        elif self.premium_highlight == 3:
            return 'premium-highlight-3'
        else:
            return 'no-highlight'

    def appear_chance(self):
        if self.premium_tier == 1:
            return 0.3636
        elif self.premium_tier == 2:
            return 0.6364
        else:
            return 0.0

    def is_bumped(self):
        now = timezone.now()
        gap = 60 * 30  # 30 minutes
        if (now - self.bumped_at).total_seconds() < gap:
            return True
        else:
            return False


class ServerManager(models.Model):
    manager_id = models.CharField(max_length=20)
    server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE, related_name='managers')

    def __str__(self):
        return self.manager_id


class DiscordEmoji(models.Model):
    server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE, related_name='emojis')
    emoji_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    url = models.URLField(blank=True)
    require_colons = models.BooleanField(default=True)
    animated = models.BooleanField(default=False)

    def get_alias(self):
        if self.require_colons:
            return f':{self.name}:'
        else:
            return self.name
