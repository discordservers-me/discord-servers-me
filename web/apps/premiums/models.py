from django.db import models

# Create your models here.


class PremiumTier(models.Model):
    tier = models.IntegerField(default=0)

    def __str__(self):
        return str(self.tier)


class PremiumFeature(models.Model):
    icon = models.CharField(max_length=50, blank=True)
    icon_color = models.CharField(max_length=50, blank=True)
    background_color = models.CharField(max_length=50, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    tier = models.ForeignKey(PremiumTier, on_delete=models.CASCADE, related_name='features')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description
