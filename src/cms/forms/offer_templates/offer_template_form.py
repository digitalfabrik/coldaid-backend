"""
Form for creating an offer_template object
"""
from django import forms

from ...models import OfferTemplate
from ...utils.slug_utils import generate_unique_slug


class OfferTemplateForm(forms.ModelForm):
    """
    DjangoForm Class, that can be rendered to create deliverable HTML

    Args:
        forms : Defines the form as an Model form related to a database object
    """

    class Meta:
        model = OfferTemplate
        fields = [
            'name',
            'slug',
            'thumbnail',
            'url',
            'post_data',
            'use_postal_code'
        ]

    def __init__(self, *args, **kwargs):
        super(OfferTemplateForm, self).__init__(*args, **kwargs)

    def clean_slug(self):
        return generate_unique_slug(self, 'offer-template')

    def clean_post_data(self):
        cleaned_post_data = self.cleaned_data['post_data']
        if not cleaned_post_data:
            cleaned_post_data = dict()
        return cleaned_post_data
