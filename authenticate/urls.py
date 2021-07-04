from django.urls import path
from .views import RegisterView, CustomLoginView
from django.contrib.auth.views import LogoutView
from facetagram import settings

app_name = 'authenticate'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]
