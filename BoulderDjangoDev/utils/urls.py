from config import BASE_URL
from django.core.urlresolvers import reverse

from .errors import InvalidViewNameError

def reverse_url(view_name, args=None, kwargs=None, current_app=None):
    try:
        url = reverse(view_name, args=args, kwargs=kwargs, 
            current_app=current_app)
        return "%s%s" % (BASE_URL, url)
    except:
        raise InvalidViewNameError("You must specify a valid view name "
            "when you call reverse_url in the utils.urls file.")
