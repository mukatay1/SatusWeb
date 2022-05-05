from django.contrib import admin
from .models import NotificationModel


# Register your models here.
@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'to_user', 'from_user', 'created_time', 'user_has_seen')
    list_filter = ('to_user', 'from_user', 'user_has_seen')
    ordering = ('notification_type',)
    list_editable = ('user_has_seen',)
