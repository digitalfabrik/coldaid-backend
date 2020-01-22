"""
Form for creating a request object and request translation object
"""
import logging

from django import forms

from ...models import Request


logger = logging.getLogger(__name__)


class RequestForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """

    class Meta:
        model = Request
        fields = ['address', 'postcode', 'city', 'country', 'latitude', 'longitude']

    def __init__(self, data=None, instance=None, disabled=False):
        logger.info('RequestForm instantiated with data %s and instance %s', data, instance)

        # instantiate ModelForm
        super(RequestForm, self).__init__(data=data, instance=instance)

        # If form is disabled because the user has no permissions to edit the page, disable all form fields
        if disabled:
            for _, field in self.fields.items():
                field.disabled = True

    # pylint: disable=arguments-differ
    def save(self, region=None):
        logger.info('RequestForm saved with cleaned data %s and changed data %s', self.cleaned_data, self.changed_data)

        request = super(RequestForm, self).save(commit=False)

        if not self.instance.id:
            # only update these values when request is created
            request.region = region

        request.save()
        return request
