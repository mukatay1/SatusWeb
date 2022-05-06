from django.urls import path
from .views import ThreadListView, ThreadCreateView, ThreadView, CreateMessageView

urlpatterns = [
    path('', ThreadListView.as_view(), name='thread_list'),
    path('create/<int:pk>', ThreadCreateView.as_view(), name='thread_create'),
    path('<int:pk>/', ThreadView.as_view(), name='thread_detail'),
    path('<int:pk>/message_create/', CreateMessageView.as_view(), name='messages_create'),
]
