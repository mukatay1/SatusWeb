from django.contrib import admin
from .models import Thread


# Register your models here.
@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver')
    list_filter = ('user', 'receiver')
