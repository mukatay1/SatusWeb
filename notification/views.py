from django.shortcuts import redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from .notification_services import notification_delete


class PostNotificationView(View):
    def get(self, request, notification_pk, satus_slug, *args, **kwargs):
        notification_delete(notification_pk)
        return redirect(reverse_lazy('detail', kwargs={'satus_slug': satus_slug}))


class ThreadNotificationView(View):
    def get(self, request, notification_pk, pk, *args, **kwargs):
        notification_delete(notification_pk)
        return redirect(reverse_lazy('thread_detail', kwargs={'pk': pk}))


class ProfileNotificationView(View):
    def get(self, request, notification_pk, pk, *args, **kwargs):
        notification_delete(notification_pk)
        return redirect(reverse_lazy('profile', kwargs={'pk': pk}))
