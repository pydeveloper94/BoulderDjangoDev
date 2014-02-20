"""Defined the django models for a blog post and comment of that post."""

from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.template.defaultfilters import slugify

from utils.urls import reverse_url

from datetime import datetime

class BlogPost(models.Model):
    """Blog post model. Will save all text in markdown."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name='blog_posts')
    title = models.CharField(max_length=100)
    title_slug = models.SlugField(max_length=100, unique=True)
    caption = models.TextField(max_length=255)
    text = models.TextField()
    is_draft = models.BooleanField(default=True)
    date_published = models.DateTimeField(editable=False, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_published']

    def save(self, *args, **kwargs):
        """When saving the model, it will set the date_published to the current
        datetime. Also, if it's published, then it cannot be retracted into a
        draft again.
        """
        if (self.is_draft == False) and (self.date_published == None):
            self.date_published = datetime.now()
        if self.date_published:
            self.is_draft = False
        self.title_slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_url(self):
        """Returns a hyperlink of the current BlogPost instance."""
        return reverse_url('blog-detail',
            args=[self.user.username, self.title_slug])

    def get_comments(self):
        """Returns a list of all comments attached to the current BlogPost
        instance.
        """
        return self.comment_set.all()

class Comment(models.Model):
    """Comment model for blog posts"""

    text = models.TextField()
    post = models.ForeignKey(BlogPost, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_updated']
