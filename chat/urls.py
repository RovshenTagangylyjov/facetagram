from django.urls import path
from .views import ChatView, SendTextView, GetTextView

app_name = 'chat'
urlpatterns = [
    path('<int:pk>/', ChatView.as_view(), name='room'),
    path('text/', SendTextView.as_view(), name='send_text'),
    path('get_text/', GetTextView.as_view(), name='get_text'),
]
