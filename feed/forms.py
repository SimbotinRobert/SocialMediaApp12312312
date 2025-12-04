
from django import forms
from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_name', 'post_content', 'image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_picture']
        labels = {
            'bio': 'Biografia ta',
            'profile_picture': 'Poza de profil',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']