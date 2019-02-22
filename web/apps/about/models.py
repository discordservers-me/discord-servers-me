from django.db import models


# Create your models here.

class AboutContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return self.title
