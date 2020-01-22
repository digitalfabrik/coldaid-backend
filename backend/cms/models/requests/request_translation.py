"""Model for Requests

"""
from django.conf import settings
from django.db import models
from django.utils import timezone

from .request import Request
from ..languages.language import Language
from ...constants import status


class RequestTranslation(models.Model):
    """Translation of an Requests

    Args:
        models : Database model inherit from the standard django models
    """

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, blank=True, allow_unicode=True)
    request = models.ForeignKey(
        Request,
        related_name='translations',
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=6, choices=status.CHOICES, default=status.DRAFT)
    short_description = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    version = models.PositiveIntegerField(default=0)
    minor_edit = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    @property
    def foreign_object(self):
        return self.request

    @property
    def permalink(self):
        return '/'.join([
            self.request.region.slug,
            self.language.code,
            'requests',
            self.slug
        ])

    class Meta:
        ordering = ['request', '-version']
        default_permissions = ()
