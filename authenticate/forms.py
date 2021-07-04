from django.contrib.auth.forms import UserCreationForm
from profiles.models import User


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email')
