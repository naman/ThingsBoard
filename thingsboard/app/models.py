from django.db import models


class Things(models.Model):

    """Internet of Things"""

    name = models.CharField("Name", max_length=120)
    description = models.CharField("Description", max_length=120)
    mac_address = models.CharField("MAC Address", max_length=120, null=True)
    state = models.CharField("State", max_length=120)
    # location =

# def __str__(self):  # __unicode__ on Python 2
    # return self.name
