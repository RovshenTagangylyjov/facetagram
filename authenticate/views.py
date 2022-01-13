from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse
from django.shortcuts import redirect

from .forms import CreateUserForm, LoginForm


class RegisterView(CreateView):
    template_name = 'authenticate/register.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('authenticate:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("posts:list"))
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'authenticate/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm    