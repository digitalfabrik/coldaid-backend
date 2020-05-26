"""
Form for creating a region user object
"""
import logging


from ..users import UserProfileForm
from ...models import UserProfile


logger = logging.getLogger(__name__)


class RegionUserProfileForm(UserProfileForm):

    class Meta:
        model = UserProfile
        fields = ['organization']

    def __init__(self, data=None, instance=None):

        logger.info('RegionUserProfileForm instantiated with data %s and instance %s', data, instance)

        # Instantiate ModelForm
        super(RegionUserProfileForm, self).__init__(data=data, instance=instance)

    def save(self, *args, **kwargs):

        logger.info('RegionUserProfileForm saved with cleaned data %s and changed data %s', self.cleaned_data, self.changed_data)

        # pop kwarg to make sure the super class does not get this param
        region = kwargs.pop('region', None)

        # check if instance exists now because after save() from UserProfileForm it will exist anyway
        instance_exists = bool(self.instance.id)

        # save UserProfileForm
        user_profile = super(RegionUserProfileForm, self).save(*args, **kwargs)

        if not instance_exists:
            # only update the region when user is created
            user_profile.regions.add(region)
            user_profile.save()
            logger.info(
                'The new user %s was added to the region %s.',
                user_profile.user,
                region
            )

        return user_profile
