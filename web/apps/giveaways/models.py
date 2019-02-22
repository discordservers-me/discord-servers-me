from django.db import models


class GiveawayInformation(models.Model):
    title = models.CharField(max_length=200, blank=True, help_text='A title that does not show in the page. Only in the Admin interface.')
    description = models.TextField(max_length=5000, blank=True, help_text='Edit as you want, or use Code View to edit in HTML.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended = models.BooleanField(default=False, help_text='Check this to mark the Giveaway as ended. It will not show in the page.')

    def __str__(self):
        return self.title
