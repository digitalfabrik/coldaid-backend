"""Model for logbook

"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from ..regions.region import Region
from ..vehicles.vehicle import Vehicle


class Logbook(models.Model):
    """Object for a logbook

    Args:
        models : Database model inherit from the standard django models
    """
    vehicle = models.ForeignKey(Vehicle, related_name='logbooks', on_delete=models.CASCADE)
    driver = models.CharField(max_length=20)
    coDriver = models.CharField(max_length=20)
    startDate = models.DateTimeField(default=timezone.now)
    startMileage = models.FloatField()
    press = models.CharField(max_length=250)
    endDate = models.DateTimeField(auto_now=True)
    endMileage = models.FloatField(default=0)
    comments = models.CharField(max_length=200)
    finished = models.BooleanField(default=False)

    @classmethod
    def get_list_view(cls):
        """Provides List of all logbooks in german

        Returns:
            [logbooks]: List of all logbooks
        """

        logbooks = cls.objects.all()

        return logbooks

    class Meta:
        default_permissions = ()
        permissions = (
            ('manage_logbooks', 'Can manage logbooks'),
        )
