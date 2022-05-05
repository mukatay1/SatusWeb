import logging
from .models import NotificationModel
from satusapp.models import Post, Comment

logger = logging.getLogger('main')


def notification_delete(pk):
    logger.info('Notification deleted')
    notification = NotificationModel.objects.get(pk=pk)
    notification.user_has_seen = True
    notification.save()


def notification_create(notification_type, to_user, from_user, service=None):
    if not service:
        NotificationModel.objects.create(notification_type=notification_type, to_user=to_user, from_user=from_user)
    elif isinstance(service, Post):
        NotificationModel.objects.create(notification_type=notification_type, to_user=to_user, from_user=from_user,
                                         post=service)
    elif isinstance(service, Comment):
        NotificationModel.objects.create(notification_type=notification_type, to_user=to_user, from_user=from_user,
                                         comment=service)
    else:
        NotificationModel.objects.create(notification_type=notification_type, to_user=to_user, from_user=from_user,
                                         thread=service)
    logger.info('Notification created')


def notification_filter(user):
    return NotificationModel.objects.filter(to_user=user).exclude(user_has_seen=True).order_by(
        '-created_time')[0:5].select_related('comment')
