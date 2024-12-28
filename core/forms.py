from django import forms
from .models import Circle, Post

class CircleForm(forms.ModelForm):
    class Meta:
        model = Circle
        fields = ['name', 'description']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

