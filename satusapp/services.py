from django.core.paginator import Paginator
from notification.notification_services import notification_create


def get_paginated_list(request, lst, number):
    paginator = Paginator(lst, number)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_like(request, obj):
    dislike = False
    for i in obj.dislikes.all():
        if i == request.user:
            dislike = True
            break
    if dislike:
        obj.dislikes.remove(request.user)
    like = False
    for i in obj.likes.all():
        if i == request.user:
            like = True
            break
    if not like:
        obj.likes.add(request.user)
        notification_create(1, obj.author, request.user, obj)
    if like:
        obj.likes.remove(request.user)


def get_dislike(request, obj):
    like = False
    for i in obj.likes.all():
        if i == request.user:
            like = True
            break
    if like:
        obj.likes.remove(request.user)
    dislike = False
    for i in obj.dislikes.all():
        if i == request.user:
            dislike = True
            break
    if dislike:
        obj.dislikes.remove(request.user)
    if not dislike:
        obj.dislikes.add(request.user)
