from django import forms
from .models import User


class UpdateProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}))
    biography = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'date_of_birth',
                  'avatar',
                  'country',
                  'gender',
                  'biography',
                  'is_private')
