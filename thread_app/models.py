from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


# Create your models here.
class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Thread'


class Message(models.Model):
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name="thread", blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=1000)
    time_created = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body + ' ' + str(self.time_created.date())

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Message'
