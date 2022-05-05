from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from satusapp.models import Post, Comment, Thread

User = get_user_model()


# Create your models here.
class NotificationModel(models.Model):
    notification_type = models.PositiveSmallIntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    created_time = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'NotificationModel'
        verbose_name_plural = 'NotificationModel'
