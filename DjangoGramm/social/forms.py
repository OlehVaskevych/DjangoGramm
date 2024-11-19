from django import forms
from .models import Profile, Post, Image


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'avatar']


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']  # Fields for title, description, and content

