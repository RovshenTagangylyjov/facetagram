from django.urls import path
from .views import ProfileDetailView, ProfileListView, ProfileUpdateView, FriendRequest, \
                    CreateFriendshipView, EndFriendshipView, JSONSearchProfile, JSONGetNotifications

app_name = 'profiles'
urlpatterns = [
    path('', ProfileListView.as_view(), name='list'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='detail'),
    path('<int:pk>/update', ProfileUpdateView.as_view(), name='update'),
    path('friend_request/', FriendRequest.as_view(), name='friend_request'),
    path('create_friendship/', CreateFriendshipView.as_view(), name='create_friendship'),
    path('end_friendship', EndFriendshipView.as_view(), name='end_friendship'),
    path('search/', JSONSearchProfile.as_view(), name='search'),
    path('get_notifications,', JSONGetNotifications.as_view(), name='get_notifications')
]
