from django.db import models

from .feedback import Feedback
from ..regions.region import Region


class OfferListFeedback(Feedback):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()
