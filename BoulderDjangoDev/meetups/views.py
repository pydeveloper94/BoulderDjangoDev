"""Defines the views for
/meetups/
"""

from config import GROUP_URL
from django.views.generic import View
from restless.models import serialize
from utils.response import Http200, Http400, Http403, Http404
from utils.misc import paginate

from .models import Meetup

class MeetupList(View):
    """API endpoint for Boulder Django meetups."""
    def get(self, request, *args, **kwargs):
        """Returns a list of recent meetups."""
        meetups = paginate(request=request, model=Meetup)
        meetup_fields = ["address", "city", "description", "event_url",
             "location_name", "title",
            ("group_url", GROUP_URL),
            ("date", lambda obj: obj.date.strftime("%B %d, %Y"))
        ]
        serialized_data = {
            "meetups": serialize(meetups.object_list, meetup_fields),
            "page": meetups.number,
            "count": meetups.paginator.per_page
        }
        return Http200(serialized_data)
