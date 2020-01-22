"""Model for Requests

"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from ..regions.region import Region


# pylint: disable=too-few-public-methods
class RequestManager(models.Manager):
    def get_queryset(self):
        # only return true Requests, no accommodations
        return super(RequestManager, self).get_queryset()
        #.filter(accommodation__isnull=True)


class Request(models.Model):
    """Object for Request

    Args:
        models : Database model inherit from the standard django models
    """

    region = models.ForeignKey(Region, related_name='requests', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    archived = models.BooleanField(default=False)

    objects = RequestManager()

    @classmethod
    def get_list_view(cls):
        """Provides List of all Requests in german

        Returns:
            [Request]: List of all german Requests
        """

        requests = cls.objects.all().prefetch_related(
            'translations'
        )

        return requests

    class Meta:
        default_permissions = ()
        permissions = (
            ('manage_requests', 'Can manage Requests'),
        )

    @property
    def languages(self):
        request_translations = self.translations.prefetch_related('language').all()
        languages = []
        for request_translation in request_translations:
            languages.append(request_translation.language)
        return languages

    def get_translation(self, language_code):
        try:
            request_translation = self.translations.get(language__code=language_code)
        except ObjectDoesNotExist:
            request_translation = None
        return request_translation
