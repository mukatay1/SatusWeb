from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .models import Message
from .forms import ThreadForm, MessageForm
from .thread_services import get_thread, define_thread, filter_thread
from notification.notification_services import notification_create
from satusapp.services import get_paginated_list

# Create your views here.
User = get_user_model()


class ThreadListView(View):
    def get(self, request, *args, **kwargs):
        threads = filter_thread(request.user, request.user)
        page_obj = get_paginated_list(request, threads, 10)
        context = {
            'page_obj': page_obj,
            'threads': threads
        }
        return render(request, 'satusapp/thread.html', context=context)


class ThreadCreateView(View):
    def post(self, request, pk, *args, **kwargs):
        thread_form = ThreadForm(request.POST)
        threads = get_thread(pk=pk)
        username = request.POST.get('username', "error")
        define_thread(request, thread_form, username)
        return redirect('thread_detail', threads.pk)


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread_form = ThreadForm(request.POST)
        thread = get_thread(pk=pk)
        threads = filter_thread(request.user, request.user)

        message_list = Message.objects.filter(
            thread__pk__contains=pk).select_related('receiver_user')
        context = {
            'form': form,
            'message_list': message_list,
            'thread': thread,
            'threads': threads,
            'thread_form': thread_form,
            'title': 'Сообщения' + " " + str(request.user)

        }
        return render(request, 'satusapp/thread_detail.html', context=context)


class CreateMessageView(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = get_thread(pk=pk)

        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.thread = thread
            new_message.sender_user = request.user
            new_message.receiver_user = receiver
            new_message.save()
            notification_create(4, receiver, request.user, thread)

        return redirect('thread_detail', pk=pk)
