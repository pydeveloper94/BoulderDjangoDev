"""Views for OAuth2 callbacks of OAuth2 providers."""

from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect
from django.views.generic import View

from config import (ANGULAR_PROFILE_URL, ANGULAR_404_URL, REDIRECT_URL
    GITHUB_AUTH, GOOGLE_AUTH,
    MEETUP_AUTH, STACKEXCHANGE_AUTH)
from users.models import (OAuthAccount,
    GITHUB, GOOGLE, MEETUP, STACKEXCHANGE)
from utils.errors import InvalidStackexchangeAccountType

def get_redirect_url(token):
    """Returns the redirect URL after an oauth callback"""
    return REDIRECT_URL + str(token)
    
def create_and_authenticate_user(request=None, account_type=None,
        username=None):
    """Takes a request, account_type, and username from a callback view,
    creates a new user if needed, and redirects the user to their profile,
    authenticated.
    """
    try:
        account = OAuthAccount.objects.get(
            account_type=account_type, username=username)
    except OAuthAccount.DoesNotExist:
        user = get_user_model().objects.create_user(username=None)
        user.save()
        account = OAuthAccount(
            user=user, account_type=account_type, username=username)
        account.save()
    user = authenticate(account=account)
    if user is not None:
        if user.is_active:
            login(request, user)
            response = redirect(ANGULAR_PROFILE_URL)
            response.set_cookie("username", user.username)
            return response
    return redirect(ANGULAR_404_URL)

class GithubOAuthCallback(View):
    """Github OAuth2 callback view. Creates or returns and authenticates a
    user.
    """
    def get(self, request, *args, **kwargs):
        try:
            code = request.GET.get('code')
            username = GITHUB_AUTH.get_username(code)
            return create_and_authenticate_user(request=request,
                account_type=GITHUB, username=username)
        except:
            return redirect(ANGULAR_404_URL)

class GoogleOAuthCallback(View):
    """Google OAuth2 callback view. Creates or returns and authenticates a
    user.
    """
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get('access_token')
        code = request.GET.get('code')
        if code:
            access_url = GOOGLE_AUTH.get_access_token(code)
            return redirect(get_redirect_url(access_url))
        if access_token:
            username = GOOGLE_AUTH.get_username(access_token)
            return create_and_authenticate_user(request=request,
                account_type=GOOGLE, username=username)
        return redirect(ANGULAR_404_URL)

class MeetupOAuthCallback(View):
    """Meetup OAuth2 callback view. Creates or returns and authenticates a
    user.
    """
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get('access_token')
        code = request.GET.get('code')
        if code:
            access_url = MEETUP_AUTH.get_access_token(code)
            return redirect(get_redirect_url(access_url))
        if access_token:
            username = MEETUP_AUTH.get_username(access_token)
            return create_and_authenticate_user(request=request,
                account_type=MEETUP, username=username)
        return redirect(ANGULAR_404_URL)

class StackexchangeOAuthCallback(View):
    """Stackexchange OAuth2 callback view. Creates or returns an authenticates
    user.
    """
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get('access_token')
        code = request.GET.get('code')

        if code:
            access_url = STACKEXCHANGE_AUTH.get_access_token(code)
            return redirect(get_redirect_url(access_url))
        if access_token:
            try:
                username = STACKEXCHANGE_AUTH.get_username(access_token)
                return create_and_authenticate_user(request=request,
                    account_type=STACKEXCHANGE, username=username)
            except InvalidStackexchangeAccountType:
                return redirect(ANGULAR_404_URL)
        return redirect(ANGULAR_404_URL)
