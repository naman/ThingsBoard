from django.db import models


class Connections(models.Model):
    source_address = models.CharField("Source Address", max_length=120)
    destination_address = models.CharField(
        "Destination Address", max_length=120)
    type_of_connection = models.CharField("Connection Type", max_length=120)
    visited = models.DateTimeField(auto_now_add=True)


class Permissions(models.Model):
    name = models.CharField("Name", max_length=120)


class URL(models.Model):
    name = models.CharField("Name", max_length=120)
    visited = models.DateTimeField(auto_now_add=True)


class State(models.Model):
    name = models.CharField("Name", max_length=120)
    visited = models.DateTimeField(auto_now_add=True)


class Things(models.Model):

    """Internet of Things"""

    urls_visited = models.ForeignKey(URL)
    permissions = models.ForeignKey(Permissions)
    connections = models.ForeignKey(Connections)
    state = models.ForeignKey(State)

    name = models.CharField("Name", max_length=120)
    description = models.CharField("Description", max_length=120, null=True)
    mac_address = models.CharField("MAC Address", max_length=120)
    ip_address = models.CharField("IP address", max_length=120)
    location = models.CharField("Location", max_length=120, null=True)
    admin_or_not = models.BooleanField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.name
