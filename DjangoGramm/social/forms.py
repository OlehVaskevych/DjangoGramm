from django import forms
from .models import Profile, Post, Image


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'bio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bio',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Avatar',
            })
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter post description'
            })
        }


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter post description'
            })
        }
