"""Defines the views for
/blog/
/blog/:username/
/blog/:username/:title_slug/
/blog/:username/:title_slug/comments/
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.generic import View
from restless.models import serialize
from utils.decorators import (check_json, authenticated,
    authenticated_and_authorized)
from utils.misc import paginate
from utils.response import Http200, Http400, Http403, Http404

from .forms import BlogPostForm, CommentForm
from .models import BlogPost, Comment

import json

def create_or_update_post(data, post=None):
    """Method for creating or updating blog posts."""
    # If an instance is passed, check if the 
    if (type(post) != BlogPost) and (post != None):
        raise ValidationError("You have passed an invalid object type, "
            "%s, into the create_or_update_post method." % str(type(post)))
    post_form = BlogPostForm(data, instance=post)
    return_message = post_form.save()
    if "errors" in return_message:
        return Http400(return_message)
    return Http200(return_message)

def create_or_update_comment(data, comment=None):
    """Method for creating or updating comments for a blog."""
    if data.get('post', None) is None:
        return Http403("You cannot post a comment for a nonexisting blog post")
    if (type(comment) != Comment) and (comment != None):
        raise ValidationError("You have passed an invalid object type, %s, "
            "into the create_or_update_comment method." %str(type(comment)))
    comment_form = CommentForm(data, instance=comment)
    return_message = comment_form.save()
    if "errors" in return_message:
        return Http400(return_message)
    return Http200(return_message)

class BlogList(View):
    """API endpoint for allowing users to get a list of blog posts, and
    create/update new posts.
    """
    def get(self, request, *args, **kwargs):
        """API endpoint for getting a list of public blog posts."""
        model_filters = {"is_draft": False}
        posts = paginate(request=request,
            model=BlogPost, model_filters=model_filters)
        post_fields = ["title", "caption",
            ("date_published", lambda obj: obj.date_published.strftime(
                "%B %d, %Y")),
            ("url", lambda obj: obj.get_url()),
            ("user", dict(fields=[
                'username',
                'image',
                ('url', lambda obj: obj.get_url())
            ]))
        ]
        serialized_data = {
            "posts": serialize(posts.object_list, post_fields),
            "page": posts.number,
            "count": posts.paginator.per_page
        }
        return Http200(serialized_data)

    @check_json
    @authenticated
    def post(self, request, *args, **kwargs):
        """API endpoint for creating new posts."""
        user = get_user_model().objects.get(username=request.user.username)
        self.json_data['user'] = user
        return create_or_update_post(self.json_data)

class BlogListUser(View):
    """API endpoint for getting a list of posts related to a user."""

    def get(self, request, *args, **kwargs):
        """Returns a list of public or private posts, depending on whether or 
        not the requested user is the one authenticated,
        """
        username = kwargs.get('username')
        try:
            request_user = get_user_model().objects.get(username=username)
        except:
            return Http404("User, %s, does not exist" % username)
        if request.user.is_authenticated() and \
                username == request.user.username:
            model_filters = {'user': request_user}
        else:
            model_filters = {'user': request_user, 'is_draft': False}
        posts = paginate(request=request, model=BlogPost, 
            model_filters=model_filters)
        post_fields = ["title", "caption",
            ("last_updated", lambda obj: obj.last_updated.strftime(
                "%B %d, %Y")),
            ("url", lambda obj: obj.get_url()),
            ("user", dict(fields=[
                "username",
                'image',
                ("url", lambda obj: obj.get_url())
            ]))
        ]
        serialized_data = {
            "posts": serialize(posts.object_list, post_fields),
            "page": posts.number,
            "count": posts.paginator.per_page
        }
        return Http200(serialized_data)
        
class BlogDetail(View):
    """API endpoint for returning a single blog post."""

    def get(self, request, *args, **kwargs):
        """Returns the data for a full blog post, and a hyperlink for attached
        comments.
        """
        try: # Check if blog post exists
            title = kwargs.get('title_slug')
            username = kwargs.get('username')
            user = get_user_model().objects.get(username=username)
            post = BlogPost.objects.get(title_slug=title, user=user) 
        except:
            return Http404("This blog post does not exist.")

        if post.is_draft and request.user.username != user.username:
            return Http403("You are not authorized to view this post "
                "because you are not the owner, and it is not public yet.")
        post_fields = ['title', 'caption', 'text', 'pk',
            ('last_updated', lambda obj: obj.last_updated.strftime(
                "%B %d, %Y")),
            ('user', dict(fields=[
                'username',
                ('url', lambda obj: obj.get_url())
            ]))
        ]
        if post.is_draft == False:
            post_fields.append(('date_published', 
                lambda obj: obj.date_published.strftime("%B %d, %Y")))
        return_data = serialize(post, fields=post_fields)
        return Http200(return_data)

    @check_json
    @authenticated_and_authorized(model=BlogPost,
        model_filters=["username", "title_slug"])
    def put(self, request, *args, **kwargs):
        """API endpoint for updating a post"""
        # The BlogPost instance will not keep an attr user, referencing
        # the user owning the post.
        user = get_user_model().objects.get(username=request.user.username)
        self.json_data['user'] = user
        pk = self.json_data.pop('pk', -1)
        post = BlogPost.objects.get(user=self.user, pk=pk)
        return create_or_update_post(self.json_data, post=post)

    @authenticated_and_authorized(model=BlogPost,
        model_filters=["username", "title_slug"])
    def delete(self, request, *args, **kwargs):
        """API endpoint for deleting a post."""
        title_slug = kwargs.get('title_slug')
        user = get_user_model().objects.get(username=request.user.username)
        post = BlogPost.objects.get(title_slug=title_slug, user=user)
        post.delete()
        return Http200()

class CommentList(View):
    """API endpoint for getting a list of comments, creating a new comment, or
    updating a comment
    """
    def get(self, request, *args, **kwargs):
        """Returns a list of paginated comments."""
        try: # Check if Blog post exists, and return a list of related comments
            username = kwargs.get('username')
            user = get_user_model().objects.get(username=username)
            title_slug = kwargs.get('title_slug')
            post = BlogPost.objects.get(user=user, title_slug=title_slug)
            model_filters = {"post": post}
            comments = paginate(request=request,
                model=Comment, model_filters=model_filters)
            comment_fields = ['text', 'pk',
                ('date_created', lambda obj: obj.date_created.strftime(
                    "%B %d, %Y")),
                ('date_updated', lambda obj: obj.date_updated.strftime(
                    "%B %d, %Y")),
                ('user', dict(fields=[
                    'username',
                    'image',
                    ('url', lambda obj: obj.get_url())
                ]))
            ]
            return_data = {
                "comments": serialize(comments.object_list, comment_fields),
                "page": comments.number,
                "count": comments.paginator.per_page
            }
            return Http200(return_data)
        except:
            return Http404("Blog post does not exist.")

    @check_json
    @authenticated
    def post(self, request, *args, **kwargs):
        """Creates a new comment."""
        try:
            username = kwargs.get('username')
            post_user = get_user_model().objects.get(username=username)
        except:
            return Http404("This post does not exist")
        user = get_user_model().objects.get(username=request.user.username)
        title_slug = kwargs.get('title_slug')
        try:
            post = BlogPost.objects.get(title_slug=title_slug, user=post_user)
        except:
            post = None
        self.json_data['user'] = user
        self.json_data['post'] = post  
        return create_or_update_comment(self.json_data)

class CommentEdit(View):
    """API endpoint for editting a comment"""
    
    @check_json
    @authenticated_and_authorized(model=Comment, model_filters=["pk"])
    def put(self, request, *args, **kwargs):
        """Updates a comment."""
        username = kwargs.get('username')
        try:
            post_user = get_user_model().objects.get(username=username)
        except:
            return Http404('This user does not exist')
        title_slug = kwargs.get('title_slug')
        pk = kwargs.get('pk')
        try:
            post = BlogPost.objects.get(user=post_user, title_slug=title_slug)
        except:
            return Http404('This blog post does not exist')
        try:
            comment = Comment.objects.get(pk=pk)
        except:
            return Http404("This comment does not exist")
        user = get_user_model().objects.get(username=request.user.username)
        self.json_data['user'] = user
        self.json_data['post'] = post
        return create_or_update_comment(self.json_data, comment=comment)

    @authenticated_and_authorized(model=Comment, model_filters=["pk"])
    def delete(self, request, *args, **kwargs):
        """Deletes a comment."""
        pk = kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Http200()
