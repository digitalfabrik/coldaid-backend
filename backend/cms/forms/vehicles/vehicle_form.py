import logging

from django import forms

from ...models import Vehicle

logger = logging.getLogger(__name__)


class VehicleCreateForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """

    class Meta:
        model = Vehicle
        fields = ['region', 'type', 'licencePlate', 'seats', 'backSeats', 'equipment']
