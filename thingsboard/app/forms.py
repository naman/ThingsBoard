# all forms here
from django.forms import ModelForm
from app.models import Thing


class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['location', 'admin_or_not']
