from django.urls import path
from .views import ChatView, TextView, GetTextView

app_name = 'chat'
urlpatterns = [
    path('<int:pk>/', ChatView.as_view(), name='chat'),
    path('text/', TextView.as_view(), name='text'),
    path('get_text/', GetTextView.as_view(), name='get_text'),
]
