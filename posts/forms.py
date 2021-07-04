from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    user = forms.HiddenInput

    class Meta:
        model = Post
        fields = ['image', 'description', 'location']


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description', 'location']


class CommentForm(forms.ModelForm):
    user = forms.HiddenInput
    post = forms.HiddenInput

    class Meta:
        model = Comment
        fields = ['text']
