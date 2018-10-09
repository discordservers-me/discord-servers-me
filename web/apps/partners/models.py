from django.db import models


# Create your models here.
def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s.%s" % (filebase, extension)

    # PartnerModel = instance.__class__
    # new_id = PartnerModel.objects.order_by("id").last().id + 1
    # return "partners/%s" % filename


class PartnersInformation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000, blank=True)
    url = models.CharField(max_length=256)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return self.title
