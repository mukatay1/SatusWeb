from django.contrib import admin
from .views import Post, UserProfile, Comment, Thread, Notification


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'slug', 'time_created')
    list_filter = ('author', 'time_created')
    ordering = ('time_created',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'phone', 'birth', 'city')
    list_filter = ('gender', 'city')
    ordering = ('birth',)
    list_editable = ('city',)


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('user', 'receiver')
    list_filter = ('user', 'receiver')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('context', 'time_created', 'parent')


