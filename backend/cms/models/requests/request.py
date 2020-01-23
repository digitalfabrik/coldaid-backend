"""Model for Requests

"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now
from ..regions.region import Region
from ..vehicles.vehicle import Vehicle


# pylint: disable=too-few-public-methods
class RequestManager(models.Manager):
    def get_queryset(self):
        # only return true Requests, no accommodations
        return super(RequestManager, self).get_queryset()
        # .filter(accommodation__isnull=True)


class Request(models.Model):
    """Object for Request

    Args:
        models : Database model inherit from the standard django models
    """
    MALE = 'm'
    FEMALE = 'w'
    OTHER = 'x'
    GENDER_CHOICES = (
        ('m', 'male'),
        ('w', 'female'),
        ('x', 'other'),
    )
    GROUPSIZE = [("0", "-")]  # , *(zip(range(1, 10), (range(1, 10)))), ("11", ">10")]
    for i in range(1, 10):
        GROUPSIZE.append([str(i), str(i)])
    GROUPSIZE.append(("11", ">10"))
    # Infos about person in need (pin)
    pinname = models.CharField(max_length=250, default="")
    wheelchair = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHER)
    medicalNeeds = models.BooleanField(default=False)
    luggage = models.BooleanField(default=False)
    children = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    group = models.CharField(max_length=5, choices=GROUPSIZE, default="0", unique=False)

    # Infos about helping person
    helpername = models.CharField(max_length=250, default="")
    phone = models.CharField(max_length=20, default="0049")
    # Infos about location
    region = models.ForeignKey(Region, related_name='requests', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10, validators=[
        RegexValidator(regex='^.{5}$', message='Length has to be 5', code='nomatch')])
    city = models.CharField(max_length=250, default="Berlin")
    country = models.CharField(max_length=250, default="Berlin")
    latitude = models.FloatField()
    longitude = models.FloatField()
    # other meta infos
    # date=models.DateTimeField(default=now)
    archived = models.BooleanField(default=False)
    objects = RequestManager()
    assignedBus = models.ForeignKey(Vehicle, related_name='assignedRequests', on_delete=models.SET_NULL, null=True,
                                    blank=True)

    @staticmethod
    def vehicles():
        return Vehicle.objects.all()


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

