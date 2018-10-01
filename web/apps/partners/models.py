from django.db import models

# Create your models here.

class PartnersInformation(models.Model):
    title = models.CharField(max_length=200, help_text='A title that does not show in the page. Only in the Admin interface.')
    description = models.TextField(max_length=5000, blank=True, help_text='Edit as you want, or use Code View to edit in HTML.')

    def __str__(self):
        return self.title
