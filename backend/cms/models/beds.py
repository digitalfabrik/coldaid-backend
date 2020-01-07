from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .accommodation import Accommodation
from .bed_target_group import BedTargetGroup


class Beds(models.Model):

    accommodation = models.ForeignKey(Accommodation, related_name='beds', on_delete=models.CASCADE)
    target_group = models.ForeignKey(BedTargetGroup, related_name='beds', on_delete=models.CASCADE)
    num_beds = models.IntegerField(validators=[MinValueValidator(0)])
    num_free_beds = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return "Beds: {}/{} for {}".format(
            self.num_beds,
            self.num_free_beds,
            self.target_group
        )

    def clean(self):
        # Don't allow num_free_beds to exceed num_beds
        if self.num_free_beds > self.num_beds:
            raise ValidationError(_('There cannot be more free beds than the total number of beds.'))

    class Meta:
        default_permissions = ()
        permissions = (
            ('manage_beds', 'Can manage beds'),
        )
