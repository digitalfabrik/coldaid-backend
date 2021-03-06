"""
Form for creating or saving event objects and their corresponding event translation objects
"""
import logging

from datetime import time

from django import forms
from django.utils.translation import ugettext as _

from ...models import Event

logger = logging.getLogger(__name__)


class EventForm(forms.ModelForm):
    is_all_day = forms.BooleanField(required=False)
    is_recurring = forms.BooleanField(required=False)

    class Meta:
        model = Event
        fields = [
            'start_date',
            'start_time',
            'end_date',
            'end_time',
            'picture'
        ]
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

    def __init__(self, data=None, instance=None, disabled=False):
        logger.info('EventForm instantiated with data %s and instance %s', data, instance)

        # Instantiate ModelForm
        super(EventForm, self).__init__(data=data, instance=instance)

        if self.instance.id:
            # Initialize BooleanFields based on Event properties
            self.fields['is_all_day'].initial = self.instance.is_all_day
            self.fields['is_recurring'].initial = self.instance.is_recurring

        # If form is disabled because the user has no permissions to edit the page, disable all form fields
        self.disabled = disabled
        if disabled:
            for _, field in self.fields.items():
                field.disabled = True

    #pylint: disable=arguments-differ
    def save(self, region=None, recurrence_rule=None, location=None):
        logger.info('EventForm saved with cleaned data %s and changed data %s', self.cleaned_data, self.changed_data)

        # Disable instant commit on saving because missing information would cause errors
        event = super(EventForm, self).save(commit=False)

        if not self.instance.id:
            # Set initial values on event creation
            event.region = region

        if event.recurrence_rule and not recurrence_rule:
            # Delete old recurrence rule from database in order to not spam the database with unused objects
            event.recurrence_rule.delete()
        event.recurrence_rule = recurrence_rule

        event.location = location

        event.save()
        return event

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        logger.info('EventForm cleaned [1/2] with cleaned data %s', cleaned_data)

        # make self.data mutable to allow values to be changed manually
        self.data = self.data.copy()

        if cleaned_data.get('is_all_day'):
            cleaned_data['start_time'] = time.min
            self.data['start_time'] = time.min
            # Strip seconds and microseconds because our time fields only has hours and minutes
            cleaned_data['end_time'] = time.max.replace(second=0, microsecond=0)
            self.data['end_time'] = time.max.replace(second=0, microsecond=0)
        else:
            # If at least one of the time fields are missing, show an error
            if not cleaned_data.get('start_time'):
                self.add_error('start_time', forms.ValidationError(_('If the event is not all-day, the start time is required'), code='required'))
            if not cleaned_data.get('end_time'):
                self.add_error('end_time', forms.ValidationError(_('If the event is not all-day, the end time is required'), code='required'))
            elif cleaned_data['start_time'] == time.min and cleaned_data['end_time'] == time.max.replace(second=0, microsecond=0):
                self.data['is_all_day'] = True

        if cleaned_data.get('end_date') and cleaned_data.get('start_date'):
            if cleaned_data.get('end_date') < cleaned_data.get('start_date'):
                # If both dates are given, check if they are valid
                self.add_error('end_date', forms.ValidationError(_('The end of the event can\'t be before the start of the event'), code='invalid'))
            elif cleaned_data.get('end_date') == cleaned_data.get('start_date'):
                # If both dates are identical, check the times
                if cleaned_data.get('end_time') and cleaned_data.get('start_time'):
                    # If both times are given, check if they are valid
                    if cleaned_data.get('end_time') < cleaned_data.get('start_time'):
                        self.add_error('end_time', forms.ValidationError(_('The end of the event can\'t be before the start of the event'), code='invalid'))

        logger.info('EventForm cleaned [2/2] with cleaned data %s', cleaned_data)

        return cleaned_data
