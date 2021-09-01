from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView, SearchProfileView, \
    FriendRequest, CreateFriendshipView, FriendsView, JSONSearchFriend

app_name = 'profiles'
urlpatterns = [
    path('search/', SearchProfileView.as_view(), name='search_profile'),
    path('friend_request/', FriendRequest.as_view(), name='friend_request'),
    path('create_friendship/', CreateFriendshipView.as_view(), name='create_friendship'),
    path('friends/', FriendsView.as_view(), name='friends'),
    # path('json-search/', JSONSearchProfile.as_view(), name='json-search'),
    path('json-friend-search/', JSONSearchFriend.as_view(), name='json-friend-search'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='detail'),
    path('<int:pk>/update', ProfileUpdateView.as_view(), name='update'),
]
