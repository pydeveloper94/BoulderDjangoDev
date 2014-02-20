"""Forms module for creating and editing blog posts and comments."""

from django import forms
from utils.fields.form_fields import BlogPostField, DjangoDevField
from .models import BlogPost, Comment

import json

class BlogPostForm(forms.ModelForm):
    """Form for validating blog posts. The save method is overridden to return
    a json document letting the user know whether or not it was successful.
    """
    user = DjangoDevField()
    caption = forms.CharField(max_length=500)
    class Meta:
        model = BlogPost
        fields = ['caption', 'text', 'title', 'is_draft', 'user']

    def save(self, commit=True):
        """Saves the blog post and returns its dictionary representation"""
        try:
            post = super().save(commit=commit)
        except:
            error_dict = dict(self.errors.items())
            errors = [error[0] for error in error_dict.values()
                if len(error) > 0]
            return {"errors": errors}
        return {
            "title": self.cleaned_data.get('title'),
            "text": self.cleaned_data.get('text'),
            "is_draft": self.cleaned_data.get('is_draft'),
            "caption": post.caption,
            "pk": post.pk, 
            "url": post.get_url()
        }

class CommentForm(forms.ModelForm):
    """Form for validating comments."""
    user = DjangoDevField()
    post = BlogPostField()
    class Meta:
        model = Comment
        fields = ['text', 'post', 'user']
    
    def save(self, commit=True):
        """Saves the comment and returns a JSON representation of it."""
        try:
            comment = super().save(commit=commit)
        except:
            error_dict = dict(self.errors.items())
            errors = [error[0] for error in error_dict.values()
                if len(error) > 0]
            return {"errors": errors}
        return {
            "text": self.cleaned_data.get('text'),
            "date_created": comment.date_created.strftime("%B %d, %Y"),
            "date_updated": comment.date_updated.strftime("%B %d, %Y")
        }
