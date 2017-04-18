# all forms here
from django.forms import ModelForm
from app.models import *


class ThingForm(ModelForm):
    class Meta:
        model = Thing
        exclude = ['states', 'connections', 'urls_visited']


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        exclude = ['createdon']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['createdon']


class URLForm(ModelForm):
    class Meta:
        model = URL
        exclude = ['visited']


class TypeForm(ModelForm):
    class Meta:
        model = Thing_Type
        exclude = ['createdon']


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        exclude = ['createdon']
