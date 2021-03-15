from django import forms
from .models import *

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category',  'blog_image', 'is_published']



