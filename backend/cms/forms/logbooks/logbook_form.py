import logging

from django import forms

from ...models import Logbook


logger = logging.getLogger(__name__)


class LogbookCreateForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """

    class Meta:
        model = Logbook
        fields = ['vehicle', 'driver', 'coDriver', 'startDate', 'startMileage', 'press']

class LogbookFinishForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """

    class Meta:
        model = Logbook
        fields = ['endMileage', 'comments']
