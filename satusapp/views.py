from allauth.account.views import SignupView, LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Post, UserProfile, MultipleImages, Comment, Thread, User, Message
from .forms import PostForm, UserProfileForm, CommentForm, ThreadForm, MessageForm
from django.views import View
import logging
from notification.models import NotificationModel

logger = logging.getLogger('main')


def logout_user(request):
    logger.info(f"The {request.user.username} logged out of his account . ")
    logout(request)
    return redirect(reverse_lazy('home'))


class MyLoginView(LoginView):
    def get_context_data(self, **kwargs):
        context = super(MyLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context


class MySignupView(SignupView):
    def get_context_data(self, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = cache.get('posts')
        if not posts:
            posts = Post.objects.all().order_by('-time_created').select_related('author').prefetch_related('photo')
            cache.set('posts', posts, 3)
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = PostForm()

        context = {
            'title': 'Главная страница',
            'posts': posts,
            'form': form,
            'page_obj': page_obj,

        }
        return render(request, 'satusapp/index.html', context=context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('photo')

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for f in files:
                img = MultipleImages(photo=f)
                img.save()
                post.photo.add(img)
            post.save()

            return redirect(reverse_lazy('home'))

        context = {
            'title': 'Главная страница',
        }

        return render(request, 'satusapp/index.html', context=context)


class PostDetailView(View):
    def get(self, request, satus_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=satus_slug)
        comments = Comment.objects.filter(post=post, parent=None).order_by('-time_created').select_related('author')
        paginator = Paginator(comments, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        number = len(post.photo.all())
        lst = []
        for i in range(number):
            lst.append(i)
        form = CommentForm()
        context = {
            'title': post.name,
            'post': post,
            'lst': lst,
            'form': form,
            'page_obj': page_obj

        }
        return render(request, 'satusapp/detail.html', context=context)

    def post(self, request, satus_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=satus_slug)
        number = len(post.photo.all())
        lst = []
        for i in range(number):
            lst.append(i)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            NotificationModel.objects.create(notification_type=2, to_user=post.author, from_user=request.user, post=post)
            return redirect(reverse_lazy('detail', args=[satus_slug]))

        context = {
            'title': post.name,
            'post': post,
            'lst': lst,
            'form': form,

        }
        return render(request, 'satusapp/detail.html', context=context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'satusapp/post_delete.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'satus_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить'
        return context

    def test_func(self):
        check_post = self.get_object()
        return check_post.author == self.request.user


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'satusapp/edit.html'
    form_class = PostForm
    slug_url_kwarg = 'satus_slug'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактировать'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class UserProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(UserProfile, pk=pk)
        user_posts = cache.get('user_posts')
        notifications = cache.get('notifications')
        if not user_posts:
            posts = Post.objects.filter(author=user.user).order_by('-time_created')[0:5].select_related('author')
            cache.set('user_posts', posts, 2)
        followed = UserProfile.objects.filter(followers=user.user).prefetch_related('followers')
        if not notifications:
            notifications = NotificationModel.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by(
                '-created_time')[0:5].select_related('comment')
            cache.set('notifications', notifications, 2)

        total = len(followed)
        followers = user.followers.all()
        if len(followers) == 0:
            is_follower = False

        for i in followers:
            if i == request.user:
                is_follower = True
                break
            else:
                is_follower = False
        try:
            thread = Thread.objects.get(
                Q(user=request.user) & Q(receiver=user.user) | Q(user=user.user) & Q(receiver=request.user))

        except:
            thread = Thread.objects.create(user=request.user, receiver=user.user)

        context = {
            'title': 'Профиль' + ' ' + str(user),
            'posts': posts,
            'user': user,
            'is_follower': is_follower,
            'total': total,
            'thread': thread,

            'notifications': notifications

        }
        return render(request, 'satusapp/profile.html', context=context)


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = UserProfile
    template_name = 'satusapp/profile_edit.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        user = get_object_or_404(UserProfile, pk=pk)
        posts = Post.objects.filter(author=user.user)
        context['count'] = len(posts)
        context['user'] = user
        context['title'] = 'Изменить профиль'
        return context

    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('profile', kwargs={'pk': pk})


class AddFollowers(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        profile.followers.add(request.user)
        NotificationModel.objects.create(notification_type=3, to_user=profile.user, from_user=request.user)
        next = request.POST['next']
        return redirect(next)


class RemoveFollowers(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        profile.followers.remove(request.user)
        next = request.POST['next']
        return redirect(next)


class ShowFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        followers = profile.followers.all()
        paginator = Paginator(followers, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'followers': followers,
            'title': 'Подписчики ' + ' ' + str(profile.user),
            'page_obj': page_obj

        }
        return render(request, 'satusapp/followers.html', context=context)


class ShowFollowed(View):
    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        followed = UserProfile.objects.filter(followers=profile.user)
        paginator = Paginator(followed, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'followed': followed,
            'title': 'Подписки' + ' ' + str(profile.user),
            'profile': profile,
            'page_obj': page_obj
        }
        return render(request, 'satusapp/followed.html', context=context)


class SearchUserView(View):
    def get(self, request, *args, **kwargs):
        search_satus = request.GET.get('search_satus', 'Error')
        profiles = UserProfile.objects.filter(user__username__contains=search_satus)

        is_found = True
        if len(profiles) == 0:
            is_found = False
        context = {
            'profiles': profiles,
            'is_found': is_found,

        }
        return render(request, 'satusapp/search_satus.html', context=context)


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, satus_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=satus_slug)
        dislike = False
        for i in post.dislikes.all():
            if i == request.user:
                dislike = True
                break
        if dislike:
            post.dislikes.remove(request.user)
        like = False
        for i in post.likes.all():
            if i == request.user:
                like = True
                break
        if not like:
            post.likes.add(request.user)

            NotificationModel.objects.create(notification_type=1, to_user=post.author, from_user=request.user, post=post)
        if like:
            post.likes.remove(request.user)

        address = request.POST.get('address')
        return redirect(address)


class PostDislikeView(LoginRequiredMixin, View):
    def post(self, request, satus_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=satus_slug)
        like = False
        for i in post.likes.all():
            if i == request.user:
                like = True
                break
        if like:
            post.likes.remove(request.user)
        dislike = False
        for i in post.dislikes.all():
            if i == request.user:
                dislike = True
                break
        if dislike:
            post.dislikes.remove(request.user)
        if not dislike:
            post.dislikes.add(request.user)

        address = request.POST.get('address')
        return redirect(address)


class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        dislike = False
        for i in comment.dislikes.all():
            if i == request.user:
                dislike = True
                break
        if dislike:
            comment.dislikes.remove(request.user)
        like = False
        for i in comment.likes.all():
            if i == request.user:
                like = True
                break
        if like:
            comment.likes.remove(request.user)

        if not like:
            comment.likes.add(request.user)
            NotificationModel.objects.create(notification_type=1, to_user=comment.author, from_user=request.user,
                                        comment=comment)

        comment_address = request.POST.get('comment_address')
        return redirect(comment_address)


class CommentDislikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        like = False
        for i in comment.likes.all():
            if i == request.user:
                like = True
                break
        if like:
            comment.likes.remove(request.user)
        dislike = False
        for i in comment.dislikes.all():
            if i == request.user:
                dislike = True
                break
        if dislike:
            comment.dislikes.remove(request.user)
        if not dislike:
            comment.dislikes.add(request.user)

        comment_address = request.POST.get('comment_address')
        return redirect(comment_address)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'satusapp/edit.html'
    form_class = CommentForm
    slug_url_kwarg = 'satus_slug'

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Редактировать комментарий'
        return context

    def get_success_url(self):
        slug = self.kwargs.get('satus_slug')
        return reverse_lazy('detail', kwargs={'satus_slug': slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'satusapp/post_delete.html'

    def get_success_url(self):
        slug = self.kwargs['satus_slug']
        return reverse_lazy('detail', kwargs={'satus_slug': slug})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentChildView(LoginRequiredMixin, View):
    def post(self, request, satus_slug, pk, *args, **kwargs):
        post = get_object_or_404(Post, slug=satus_slug)
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.parent = comment
            new_comment.author = request.user
            new_comment.save()

            NotificationModel.objects.create(notification_type=2, from_user=request.user, to_user=post.author,
                                        comment=comment)
        reply_comment = request.POST.get('reply_comment', 'Error')
        return redirect(reply_comment)


class ThreadListView(View):
    def get(self, request, *args, **kwargs):
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        paginator = Paginator(threads, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'threads': threads
        }
        return render(request, 'satusapp/thread.html', context=context)


class ThreadCreateView(View):
    def post(self, request, pk, *args, **kwargs):
        thread_form = ThreadForm(request.POST)
        threads = Thread.objects.get(pk=pk)
        username = request.POST.get('username', "error")
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
            return redirect('thread_detail', threads.pk)


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread_form = ThreadForm(request.POST)
        thread = Thread.objects.get(pk=pk)
        threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user)).select_related('user')

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
        thread = Thread.objects.get(pk=pk)

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

            NotificationModel.objects.create(notification_type=4, to_user=receiver, from_user=request.user, thread=thread)

        return redirect('thread_detail', pk=pk)



