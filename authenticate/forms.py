from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from profiles.models import User


class Clean:
    def clean_username(self): 
        username = self.cleaned_data.get('username')

        return username.lower()


class CreateUserForm(Clean, UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')

    


class LoginForm(Clean, AuthenticationForm):
    pass