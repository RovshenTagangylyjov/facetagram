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
    
    def form_valid(self, form):
        form = form.save(commit=False)
        form.username = form.username.lower()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'authenticate/login.html'

