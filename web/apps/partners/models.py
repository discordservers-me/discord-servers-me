from django.db import models

# Create your models here.


class PartnersInformation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)

    def __str__(self):
        return self.title
