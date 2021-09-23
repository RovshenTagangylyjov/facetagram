from django.urls import path
from .views import CreatePostView, DeletePostView, RatePostView, \
    PostListView, PostView, RateCommentView

app_name = 'posts'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create/', CreatePostView.as_view(), name='create'),
    path('delete/', DeletePostView.as_view(), name='delete'),
    path('rate/', RatePostView.as_view(), name='rate_post'),
    path('comment/rate/', RateCommentView.as_view(), name='like_comment'),
    path('<pk>/', PostView.as_view(), name='detail'),
]
