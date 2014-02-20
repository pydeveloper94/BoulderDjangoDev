"""Global configuration information, such as the oauth2 objects, api keys,
etc.
"""

from oauth.services import (GithubOAuth2Service, GoogleOAuth2Service,
    StackexchangeOAuth2Service, MeetupOAuth2Service)

from multiprocessing import Queue

import re

## API Keys
MEETUP_API_KEY = ''
STRIPE_API_KEY = ''

## Global variables
ALPHANUMERIC_REGEX = re.compile('^[A-z0-9\-\_\.]+$')
ANGULAR_PROFILE_URL = "http://localhost/#/profile/"
ANGULAR_PROFILE_URL = "http://localhost/#/profile/"
ANGULAR_404_URL = "http://localhost/#/404/"
BASE_URL = "http://localhost/api"
GROUP_URL = 'http://www.meetup.com/boulder-django/'
HOME_CAPTION = 'Boulder Django is a group for all levels of people '         \
    'interested in learning more about using Python and Django and sharing ' \
    'their knowledge and experiences with others. We accept all, from '      \
    'beginners to advanced. Please join us soon at a meetup!'
IMAGE_QUEUE = Queue()
IMAGE_SIZE = (128, 128)
JOB_COST = 2500
REDIRECT_URL = 'http://localhost'

GITHUB_AUTH = GithubOAuth2Service(
    client_id='',
    client_secret='')

GOOGLE_AUTH = GoogleOAuth2Service(
    client_id='',
    client_secret='',
    redirect_uri='http://127.0.0.1/api/oauth/google/')

MEETUP_AUTH = MeetupOAuth2Service(
    client_id='',
    client_secret='',
    redirect_uri='http://127.0.0.1/api/oauth/meetup')

STACKEXCHANGE_AUTH = StackexchangeOAuth2Service(
    client_id='',
    client_secret='',
    key='',
    redirect_uri="http://127.0.0.1/api/oauth/stackexchange")
