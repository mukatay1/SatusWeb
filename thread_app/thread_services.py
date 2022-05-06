from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from .models import Thread

User = get_user_model()


def get_thread(pk, user=None):
    if type(pk) is int:
        return Thread.objects.get(pk=pk)
    return Thread.objects.get(Q(user=pk) & Q(receiver=user) | Q(user=user) & Q(receiver=pk))


def filter_thread(user, receiver):
    return Thread.objects.filter(Q(user=user) | Q(receiver=receiver)).select_related('user')


def create_thread(request, user):
    return Thread.objects.create(Q(user=request) & Q(receiver=user))


def define_thread(request, thread_form, username):
    try:
        receiver = User.objects.get(username=username)
        if Thread.objects.filter(receiver=receiver, user=request.user).exists():
            thread = Thread.objects.filter(receiver=receiver, user=request.user)[0]
            return redirect('thread_detail', pk=thread.pk)
        elif Thread.objects.filter(receiver=request.user, user=receiver).exists():
            thread = Thread.objects.filter(receiver=request.user, user=receiver)[0]
            return redirect('thread_detail', pk=thread.pk)
        if thread_form.is_valid():
            thread = Thread(user=request.user, receiver=receiver)
            thread.save()
            return redirect('thread_detail', pk=thread.pk)
    except:
        messages.error(request, 'неверное имя пользователя')
