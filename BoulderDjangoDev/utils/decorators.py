"""Module containing helper decorators for user authentication."""

from django.contrib.auth import get_user_model
from functools import wraps

from .response import Http400, Http403, Http404, Http500

import json

def check_json(func):
    """Checks that the request's body has valid JSON, and sets kwargs['json']
    to the serialized data."""
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try: # attaches the json to the view instance
            self.json_data = json.loads(request.body.decode('utf-8'))
        except:
            return Http400('Your JSON is invalid')
        return func(self, request, *args, **kwargs)
    return wrapper

def authenticated(func):
    """Makes sure that a user is authenticated to view a post."""
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return Http403("You are not authenticated")
        return func(self, request, *args, **kwargs)
    return wrapper
            

def authenticated_and_authorized(model=None, model_filters=None):
    """Checks that a user a authenticated and authorized to edit an object
    in a model. Specific filters which are passed into the url parameters
    should bet in a list set into model_filters. This should not be a tuple!.
    """
    filters = {}
    if model == None:
        return Http500('An error occured')
    def callable(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if 'username' in model_filters:
                # Check for username in the model_filters
                try:
                    model_filters.remove('username')
                except: # This would be an annoying error to debug
                    raise Exception("You can only pass a list into the "
                    "model_filters kwarg in the authenticated_and_authorized "
                    "decorator")
                # Set the user into the filters
                username = kwargs.get('username')
                try:
                    user = get_user_model().objects.get(username=username)
                    filters['user'] = user
                except:
                    return Http404("The user attached to this mode does not "
                        "exist.")
            # Add the rest of the model filters
            for model_filter in model_filters:
                filters[model_filter] = kwargs.get(model_filter)
            # Attempt to check that a model attached to the user exists
            if len(model_filters) > 0:
                try:
                    obj = model.objects.get(**filters)
                    username = obj.user.username
                    self.user = obj.user 
                    # attaches the user to the view instance
                except Exception as e:
                    return Http404('This object does not exist')
            else:
                username = kwargs.get('username')
            # Finally check if the attached user is the user logged in
            if request.user.is_authenticated() and \
                    (request.user.username == username):
                return func(self, request, *args, **kwargs)
            else:
                return Http403("You are not authorized to edit this object")
        return wrapper
    return callable          
