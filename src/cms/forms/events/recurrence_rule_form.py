"""
Form for creating or saving event objects and their corresponding event translation objects
"""
import logging

from django import forms
from django.utils.translation import ugettext as _

from ...constants import weekdays, frequency
from ...models import RecurrenceRule

logger = logging.getLogger(__name__)


class RecurrenceRuleForm(forms.ModelForm):
    has_recurrence_end_date = forms.BooleanField(required=False)

    class Meta:
        model = RecurrenceRule
        fields = [
            'frequency',
            'interval',
            'weekdays_for_weekly',
            'weekday_for_monthly',
            'week_for_monthly',
            'recurrence_end_date',
        ]
        widgets = {
            'weekdays_for_weekly': forms.SelectMultiple(choices=weekdays.CHOICES),
            'recurrence_end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, data=None, instance=None, event_start_date=None, disabled=False):
        logger.info('RecurrenceRuleForm instantiated with data %s and instance %s', data, instance)

        # Instantiate ModelForm
        super(RecurrenceRuleForm, self).__init__(data=data, instance=instance)

        if self.instance.id:
            # Initialize BooleanField based on RecurrenceRule properties
            self.fields['has_recurrence_end_date'].initial = bool(self.instance.recurrence_end_date)

        # Set event start date to be used in clean()-method
        self.event_start_date = event_start_date

        # If form is disabled because the user has no permissions to edit the page, disable all form fields
        if disabled:
            for _, field in self.fields.items():
                field.disabled = True

    def clean(self):
        cleaned_data = super(RecurrenceRuleForm, self).clean()

        if not cleaned_data.get('frequency'):
            self.add_error('frequency', forms.ValidationError(_('No recurrence frequency selected'), code='required'))
        elif cleaned_data.get('frequency') == frequency.WEEKLY and not cleaned_data.get('weekdays_for_weekly'):
            self.add_error('weekdays_for_weekly', forms.ValidationError(_('No weekdays for weekly recurrence selected'), code='required'))
        elif cleaned_data.get('frequency') == frequency.MONTHLY:
            if not cleaned_data.get('weekday_for_monthly'):
                self.add_error('weekday_for_monthly', forms.ValidationError(_('No weekday for monthly recurrence selected'), code='required'))
            if not cleaned_data.get('week_for_monthly'):
                self.add_error('week_for_monthly', forms.ValidationError(_('No week for monthly recurrence selected'), code='required'))

        if cleaned_data.get('has_recurrence_end_date'):
            if not cleaned_data.get('recurrence_end_date'):
                self.add_error('recurrence_end_date', forms.ValidationError(_('If the recurrence ends, the recurrence end date is required'), code='required'))
            elif self.event_start_date and cleaned_data.get('recurrence_end_date') <= self.event_start_date:
                self.add_error(
                    'recurrence_end_date',
                    forms.ValidationError(_('The recurrence end date has to be after the event\'s start date'), code='invalid')
                )
        else:
            cleaned_data['recurrence_end_date'] = None

        return cleaned_data

    def has_changed(self):
        # Handle weekdays_for_weekly data separately from the other data because has_changed doesn't work
        # with CheckboxSelectMultiple widgets and ArrayFields out of the box
        try:
            # Have to remove the corresponding field name from self.changed_data
            self.changed_data.remove('weekdays_for_weekly')
        except ValueError:
            return super(RecurrenceRuleForm, self).has_changed()
        value = self.fields['weekdays_for_weekly'].widget.value_from_datadict(self.data, self.files, self.add_prefix('weekdays_for_weekly'))
        initial = self['weekdays_for_weekly'].initial
        if value:
            value = set(map(int, value))
        if initial:
            initial = set(initial)
        if value != initial:
            self.changed_data.append('weekdays_for_weekly')
        return bool(self.changed_data)
