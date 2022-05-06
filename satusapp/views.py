from allauth.account.views import SignupView, LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Post, UserProfile, MultipleImages, Comment
from .forms import PostForm, UserProfileForm, CommentForm
from django.views import View
import logging
from notification.notification_services import notification_create, notification_filter
from thread_app.thread_services import get_thread, create_thread
from .services import get_paginated_list

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
        page_obj = get_paginated_list(request, posts, 5)
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
        page_obj = get_paginated_list(request, comments, 3)
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

            notification_create(2, post.author, request.user, post)
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
            notifications = notification_filter(request.user)
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
            thread = get_thread(request.user, user.user)
        except:
            thread = create_thread(request.user, user.user)

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
        notification_create(3, profile.user, request.user)
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
        page_obj = get_paginated_list(request, followers, 5)
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
        page_obj = get_paginated_list(request, followed, 5)

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
            notification_create(1, post.author, request.user, post)
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
            notification_create(1, comment.author, request.user, comment)

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
            notification_create(2, request.user, post.author, comment)
        reply_comment = request.POST.get('reply_comment', 'Error')
        return redirect(reply_comment)
