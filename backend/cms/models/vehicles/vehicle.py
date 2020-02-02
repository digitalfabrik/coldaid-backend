"""Model for vehicle

"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from ..regions.region import Region


class Vehicle(models.Model):
    """Object for a vehicle

    Args:
        models : Databas model inherit from the standard django models
    """
    region = models.ForeignKey(Region, related_name='vehicles', on_delete=models.CASCADE)
    type = models.CharField(max_length=250)
    licencePlate = models.CharField(max_length=20)
    seats = models.IntegerField()
    backSeats = models.IntegerField()
    equipment = models.CharField(max_length=200)

    def generate_route(self):
        url = "https://www.google.com/maps/dir//"

        for r in self.assignedRequests.filter(activeRoute=True):
            a = r.address.replace(" ", "+") + ",+" + r.postcode + ",+" + r.city + "/"
            url = url + a
        #url = url.replace(" ", "+")
        #print(url)

        return url

    @classmethod
    def get_list_view(cls):
        """Provides List of all vehicles in german

        Returns:
            [vehicles]: List of all vehicles
        """

        vehicles = cls.objects.all()

        return vehicles

    def __str__(self):
        return self.licencePlate

    class Meta:
        default_permissions = ()
        permissions = (
            ('manage_vehicles', 'Can manage vehicles'),
        )
