import logging

from .models import NotificationModel

logger = logging.getLogger('main')


def notification_delete(pk):
    logger.info('Notification deleted')
    notification = NotificationModel.objects.get(pk=pk)
    notification.user_has_seen = True
    notification.save()
