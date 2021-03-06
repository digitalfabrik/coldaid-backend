"""Model for Push Notifications
"""
from django.db import models
from django.utils import timezone


class PushNotificationTranslation(models.Model):
    """Class representing the Translation of a Push Notification

    Args:
        models : Database model inherit from the standard django models
    """
    title = models.CharField(max_length=250)
    text = models.CharField(max_length=250)
    language = models.ForeignKey('Language', on_delete=models.CASCADE)
    push_notification = models.ForeignKey('PushNotification', related_name='translations', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        default_permissions = ()
