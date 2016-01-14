from django import forms
from .models import Post, Suggestions

class BlogPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('post_title', 'content', 'image')

class BlogSuggestForm(forms.ModelForm):
    class Meta:
        model=Suggestions
        fields = ('author', 'post_title', 'content', 'image')