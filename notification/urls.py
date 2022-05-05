from django.urls import path
from .views import PostNotificationView, ThreadNotificationView, ProfileNotificationView

app_name = 'notify'

urlpatterns = [
    path('<int:notification_pk>/post/<slug:satus_slug>/', PostNotificationView.as_view(),
         name='post_notification'),
    path('<int:notification_pk>/profile/<int:pk>/', ProfileNotificationView.as_view(),
         name='profile_notification'),
    path('<int:notification_pk>/thread/<int:pk>/', ThreadNotificationView.as_view(),
         name='thread_notification'),
]
