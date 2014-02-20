"""
Module for OAuth2 services. It includes the following providers:
Github, Google, Meetup, and Stackexchange.
"""

from utils.errors import InvalidStackexchangeAccountType
import requests

def _post_to_dict(text):
    """
    Parses a querystring into a dictionary.
    """
    return_dict = {}
    split_text = text.split("&")
    for item in split_text:
        text = item.split("=")
        return_dict[text[0]] = text[1]
    return return_dict

class _OAuth2Service(object):
    """Inherited helper class for creating OAuth2 services."""

    def __init__(self, client_id=None, key=None,
        client_secret=None, redirect_uri=None):
        """
        Initializes an api object with the client_id and client_secret saved
        as instance variables. These are required from all oauth providers and
        are given when you register an application.
        """
        if (not client_id) or (not client_secret):
            raise ValueError('You must specify a client_id and client secret '
                'in your OAuthService instance')
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.key = key

class GithubOAuth2Service(_OAuth2Service):
    """Service for authenticating users with Github's OAuth2 implementation.
    """
    access_token_url = 'https://github.com/login/oauth/access_token'
    api_url = "https://api.github.com/user"

    def get_username(self, code):
        if not code:
            raise ValueError('You must have a token to get a user')

        access_token = self._get_access_token(code)
        user = self._get_user(access_token)
        return user.get("login")

    def _get_access_token(self, code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code
        }
        headers = {'accept': 'application/json'}

        request = requests.post(
            self.access_token_url, data=data, headers=headers)

        response = request.json()
        return response.get("access_token")

    def _get_user(self, access_token):
        if not access_token:
            return
        params = {"access_token": access_token}
        headers = {'accept': 'application/json'}
        request = requests.get(self.api_url, params=params, headers=headers)
        return request.json()

class GoogleOAuth2Service(_OAuth2Service):
    """Service for authenticating users with Google's OAuth2 implementation.
    """
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    user_api_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    def __init__(self, *args, **kwargs):
        if kwargs.get('redirect_uri') == None:
            raise Exception('You must specify a redirect_uri for your '
                'instance of GoogleOAuth2Service')
        super().__init__(*args, **kwargs)

    def get_access_token(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'authorization_code',
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        request = requests.post(
            self.access_token_url, data=data, headers=headers)
        json_data = request.json()
        access_token = json_data.get('access_token')
        return '/api/oauth/google/?access_token=%s' % access_token

    def get_username(self, access_token):
        params = {"access_token": access_token}
        headers = {"Accept": "application/json"}
        request = requests.get(
            self.user_api_url, headers=headers, params=params)
        return request.json().get('email')

class MeetupOAuth2Service(_OAuth2Service):
    """
    Service for authenticating users with Meetup's OAuth2 implementation.
    """
    access_token_url = "https://secure.meetup.com/oauth2/access"
    api_url = "https://api.meetup.com/2/member/self"

    def __init__(self, *args, **kwargs):
        if kwargs.get('redirect_uri') == None:
            raise Exception('You must specify a redirect_uri for your '
                'instance of MeetupOAuth2Service')
        super().__init__(*args, **kwargs)

    def get_access_token(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": 'authorization_code',
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        request = requests.post(
            self.access_token_url, data=data)
        access_token = request.json().get('access_token')
        redirect_url = '/api/oauth/meetup/?access_token=%s' % access_token
        return redirect_url

    def get_username(self, access_token):
        """
        Returns a meetup users id.
        """
        params = {
            "access_token": access_token,
            "member_id": "self"
        }
        headers = {'accept': 'application/json'}
        request = requests.get(self.api_url, params=params, headers=headers)
        return request.json().get('id')

class StackexchangeOAuth2Service(_OAuth2Service):
    """
    Service for authenticating users with Stackexchanges's OAuth2
    implementation.
    """
    access_token_url = "https://stackexchange.com/oauth/access_token"
    api_url = "https://api.stackexchange.com/2.1/me"

    def __init__(self, *args, **kwargs):
        if kwargs.get('redirect_uri') == None:
            raise Exception('You must specify a redirect_uri for your '
                'instance of StackexchangeOAuth2Service')
        super().__init__(*args, **kwargs)

    def get_access_token(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        request = requests.post(
            self.access_token_url, data=data, headers=headers)
        dict_response = _post_to_dict(request.text)
        access_token = dict_response.get('access_token')
        return '/api/oauth/stackexchange?access_token=%s' % access_token

    def get_username(self, access_token):
        params = {
            "access_token": access_token,
            "key": self.key,
            "site": "stackoverflow",
            "filter": "!T6o*9deY.k9v25gWDe"
        }
        request = requests.get(self.api_url, params=params)
        for item in request.json().get('items'):
            if 'display_name' in item:
                return item['display_name']
        raise InvalidStackexchangeAccountType("You can only login with "
            "a stackoverflow account.")
