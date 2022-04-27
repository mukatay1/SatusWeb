from django.urls import path
from .views import PostListView, PostDetailView, UserProfileView, ProfileEditView, logout_user, AddFollowers, \
    RemoveFollowers, ShowFollowers, ShowFollowed, SearchUserView, PostUpdateView, PostDeleteView, PostLikeView, \
    PostDislikeView, CommentDislikeView, CommentLikeView, CommentUpdateView, CommentDeleteView, CommentChildView, \
    ThreadListView, ThreadCreateView, ThreadView, CreateMessageView, PostNotificationView, ProfileNotificationView, \
    ThreadNotificationView, MySignupView, MyLoginView

urlpatterns = [
    path('notification/<int:notification_pk>/post/<slug:satus_slug>/', PostNotificationView.as_view(),
         name='post_notification'),
    path('notification/<int:notification_pk>/profile/<int:pk>/', ProfileNotificationView.as_view(),
         name='profile_notification'),
    path('notification/<int:notification_pk>/thread/<int:pk>/', ThreadNotificationView.as_view(),
         name='thread_notification'),
    path('', PostListView.as_view(), name='home'),
    path('post/<slug:satus_slug>/detail/', PostDetailView.as_view(), name='detail'),
    path('post/<slug:satus_slug>/comment/<int:pk>/like/', CommentLikeView.as_view(), name='comment_like'),
    path('post/<slug:satus_slug>/comment/<int:pk>/dislike/', CommentDislikeView.as_view(), name='comment_dislike'),
    path('logout/', logout_user, name='logout_url'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='edit'),
    path('profile/<int:pk>/add_followers/', AddFollowers.as_view(), name='add_followers'),
    path('profile/<int:pk>/remove_followers/', RemoveFollowers.as_view(), name='remove_followers'),
    path('profile/<int:pk>/followers/', ShowFollowers.as_view(), name='show_followers'),
    path('profile/<int:pk>/followed/', ShowFollowed.as_view(), name='show_followed'),
    path('profile/search/user/', SearchUserView.as_view(), name='search_user'),
    path('post/<slug:satus_slug>/edit/', PostUpdateView.as_view(), name='update'),
    path('post/<slug:satus_slug>/delete/', PostDeleteView.as_view(), name='delete'),
    path('post/<slug:satus_slug>/like>', PostLikeView.as_view(), name='like'),
    path('post/<slug:satus_slug>/dislike/', PostDislikeView.as_view(), name='dislike'),
    path('post/<slug:satus_slug>/comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('post/<slug:satus_slug>/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<slug:satus_slug>/comment/<int:pk>/reply/', CommentChildView.as_view(), name='comment_reply'),
    path('threads/', ThreadListView.as_view(), name='thread_list'),
    path('threads/create/<int:pk>', ThreadCreateView.as_view(), name='thread_create'),
    path('threads/<int:pk>/', ThreadView.as_view(), name='thread_detail'),
    path('threads/<int:pk>/message_create/', CreateMessageView.as_view(), name='messages_create'),
    path('accounts/signup/', MySignupView.as_view(), name='account_signup'),
    path('accounts/login/', MyLoginView.as_view(), name='account_login')

]
