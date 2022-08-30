from django.db import models
from django.forms import widgets

class RadioSelectField(models.CharField):
    def formfield(self, **kwargs):
        if self.choices:
            defaults = {'widget': widgets.RadioSelect}
        defaults.update(kwargs)
        return super(RadioSelectField, self).formfield(**defaults)