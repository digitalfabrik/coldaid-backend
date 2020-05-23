"""Database model for requests

"""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import models
from cms.models.regions.region import Region
from cms.models.vehicles.vehicle import Vehicle


# pylint: disable=too-few-public-methods
#class RequestManager(models.Manager):
#    def get_queryset(self):
#        # only return true Requests, no accommodations
#        return super(RequestManager, self).get_queryset()
#        # .filter(accommodation__isnull=True)


class Request(models.Model):
    """Object for a request

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

    # Data about person in need (pin)
    pinname = models.CharField(max_length=250, default="", blank=True)
    wheelchair = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHER)
    medical_needs = models.BooleanField(default=False)
    luggage = models.IntegerField(default=0, choices=zip(range(10), range(10)), unique=False)
    iso_mat = models.BooleanField(default=False)
    blanket = models.BooleanField(default=False)
    jacket = models.BooleanField(default=False)
    sleeping_bag = models.BooleanField(default=False)
    children = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    group = models.CharField(max_length=5, choices=GROUPSIZE, default="0", unique=False)

    # Data about helper
    helpername = models.CharField(max_length=250, default="", blank=True)
    phone = models.CharField(max_length=20, default="0049")

    # Data about location
    region = models.ForeignKey(Region, related_name='requests', on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250)
    postcode = models.CharField(max_length=10, validators=[
        RegexValidator(regex='^.{5}$', message='Length has to be 5', code='nomatch')])
    city = models.CharField(max_length=250, default="Berlin")
    state = models.CharField(max_length=250, default="Berlin")
    latitude = models.FloatField(default=0, blank=True)
    longitude = models.FloatField(default=0, blank=True)

    # other metadata
    # date=models.DateTimeField(default=now)
    archived = models.BooleanField(default=False)
    #objects = RequestManager()  # TODO figure out what this was for
    assigned_bus = models.ForeignKey(Vehicle, related_name='assignedRequests', on_delete=models.SET_NULL, null=True, blank=True)
    active_route = models.BooleanField(default=True)

    @staticmethod
    def vehicles():
        """

        :return: all objects that belong to vehicle model
        """
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
        ordering = ['pinname']


    @property
    def languages(self):
        request_translations = self.translations.prefetch_related('language').all()
        language_list = []
        for request_translation in request_translations:
            language_list.append(request_translation.language)
        return language_list


    def get_translation(self, language_code):
        try:
            request_translation = self.translations.get(language__code=language_code)
        except ObjectDoesNotExist:
            request_translation = None
        return request_translation
