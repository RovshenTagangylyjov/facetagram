from django.shortcuts import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import CreateUserForm


class RegisterView(CreateView):
    template_name = 'authenticate/register.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('authenticate:login')


class CustomLoginView(LoginView):
    template_name = 'authenticate/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts:list')
        return super(CustomLoginView, self).get(request, *args, **kwargs)
