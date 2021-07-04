from django.urls import path
from .views import CreatePostView, DeletePostView, LikePostView, \
    PostListView, PostView, LikeCommentView, JSONCommentView, UpdatePostView

app_name = 'posts'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create/', CreatePostView.as_view(), name='create'),
    path('delete/', DeletePostView.as_view(), name='delete'),
    path('like/', LikePostView.as_view(), name='like_post'),
    path('comment/like/', LikeCommentView.as_view(), name='like_comment'),
    path('comment/', JSONCommentView.as_view(), name='comment'),
    path('<pk>/', PostView.as_view(), name='detail'),
    path('<pk>/update/', UpdatePostView.as_view(), name='update'),
]
