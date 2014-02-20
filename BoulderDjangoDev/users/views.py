from config import ANGULAR_PROFILE_URL
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.views.generic import View
from restless.models import serialize
from utils.decorators import (authenticated, authenticated_and_authorized,
    check_json)
from utils.misc import paginate
from utils.managers import push_image
from utils.response import Http200, Http201, Http400, Http403, Http404

from blog.models import BlogPost
from .forms import UserForm
from .models import DjangoDev, OAuthAccount

import base64
import json

class LogoutUser(View):
    """Endpoint for logging out a user."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
            response = Http201("Logout successful")
            response.delete_cookie("username")
            return response
        return Http404("You are cannot logout if you are not logged in.")

class UserProfile(View):
    """API endpoint for a user's profile"""

    def get(self, request, *args, **kwargs):
        """Returns a user's profile."""
        # Get user
        try:
            username = kwargs.get('username')
            user = DjangoDev.objects.get(username=username)
        except:
            return Http404('This user does not exist')

        # Serialize user
        user_fields = ['username', 'job_title', 'company',
            'interests', 'email', 'website', 'image']
        serialized_user = serialize(user, fields=user_fields)
        
        # Serialize attached posts
        # Check if logged in user is authorized to view these posts
        model_filters = {"user": user}
        if not ((request.user.is_authenticated()) and (user == request.user)):
            model_filters["is_draft"] = True
        posts = paginate(request=request, model=BlogPost,
            model_filters=model_filters)
        post_fields = ['title', 'caption', 
            ('url', lambda obj: obj.get_url()),
        ]
        serialized_posts = serialize(posts.object_list, fields=post_fields)
        
        # Conjoin the two together
        serialized_user['posts'] = serialized_posts
        return Http200(serialized_user)

    @check_json
    @authenticated_and_authorized(model=DjangoDev, model_filters=["username"])
    def put(self, request, *args, **kwargs):
        """Updates a user's profile"""
        # Check for a posted image, and send it into the queue
        # Note this a feature to change the image whether of not the data 
        # is valid.
        if 'image' in self.json_data.keys():
            image = self.json_data.pop('image')
            push_image(request.user.pk, image)
        
        # Save the rest of the data here
        user = get_user_model().objects.get(username=request.user.username)
        user_form = UserForm(self.json_data, instance=user)
        return_data = user_form.save()
        if "errors" in return_data:
            return Http400(return_data)
        return Http200(return_data)

    @check_json
    @authenticated_and_authorized(model=DjangoDev, model_filters=["username"])
    def delete(self, request, *args, **kwargs):
        """Deletes a user"""
        user = get_user_model().objects.get(username=request.user.username)
        user.delete()
        return Http200()
