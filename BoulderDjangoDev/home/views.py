from config import HOME_CAPTION
from django.views.generic import View
from restless.models import serialize
from utils.response import Http200

from blog.models import BlogPost
from jobs.models import Job
from meetups.models import Meetup

class HomePage(View):
    """API endpoint for the homepage"""
    def get(self, request, *args, **kwargs):
        """Returns the main quote, and the latest meetups, jobs, and posts."""
        # Posts{"is_draft": False}
        posts = BlogPost.objects.filter(**{"is_draft": False})[:5]
        post_fields = [ "title", "caption",
            ("url", lambda obj: obj.get_url())
        ]
        
        # Jobs
        jobs = Job.objects.all()[:5]
        job_fields = ["title", "company",
            ("url", lambda obj: obj.get_url())
        ]
        
        # Meetups
        meetups = Meetup.objects.all()[:5]
        meetup_fields = ["title", "event_url"]
        
        return_data = {
            "caption": HOME_CAPTION,
            "posts": serialize(posts, post_fields),
            "jobs": serialize(jobs, job_fields),
            "meetups": serialize(meetups, meetup_fields)
        }
        return Http200(return_data)
