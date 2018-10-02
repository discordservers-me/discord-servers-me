from django.db import models


# Create your models here.

    # PartnerModel = instance.__class__
    # new_id = PartnerModel.objects.order_by("id").last().id + 1
    # return "partners/%s" % filename


class PartnersInformation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)
    url = models.CharField(max_length=256)
    image = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title
