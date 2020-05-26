from django.conf import settings
from django.db import models

from .organization import Organization
from ..regions.region import Region


class UserProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    regions = models.ManyToManyField(Region, related_name='users', blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def roles(self):
        return self.user.groups.all()

    def __str__(self):
        return self.user.username

    class Meta:
        default_permissions = ()
        permissions = (
            ('change_user', 'Can change user'),
        )
