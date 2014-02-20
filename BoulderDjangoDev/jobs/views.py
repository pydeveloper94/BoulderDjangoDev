"""Defines the views for
/jobs/
/jobs/:username/
/jobs/:username/:job-slug/
/jobs/:username/:job-slug/renew/
"""

from config import STRIPE_API_KEY, JOB_COST

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.views.generic import View
from restless.models import serialize
from utils.decorators import (check_json, authenticated,
    authenticated_and_authorized)
from utils.misc import paginate
from utils.response import Http200, Http400, Http403, Http404

from .models import Job
from .forms import JobForm

import stripe

stripe.api_key = STRIPE_API_KEY

def create_or_update_job(data, job=None):
    """Method for creating or updating job posts"""
    if (type(job) != Job) and (job != None):
        raise ValidationError("You have passed an invalid object type, "
            "%s, into the create_or_update_job method." % str(type(post)))
    job_form = JobForm(data, instance=job)
    return_message = job_form.save()
    if "errors" in return_message:
        return Http400(return_message)
    return Http200(return_message)

class JobList(View):
    """API endpoint for getting a list of current job postings, and creating
    new jobs posts."""
    
    def get(self, request, *args, **kwargs):
        """Endpoint for getting jobs"""
        model_filters = {"is_expired": False}
        jobs = paginate(request=request, model=Job, 
            model_filters=model_filters)
        job_fields = ["title", "company", "company_slug", "pk",
            ("short_description", lambda obj: obj.get_short_description()),
            ("date_created", lambda obj: obj.date_created.ctime()),
            ("company_url", lambda obj: obj.get_company_url()),
            ("url", lambda obj: obj.get_url()),
            ("user", dict(fields=[
                'username',
                'image',
                ('url', lambda obj: obj.get_url())
            ]))
        ] 
        serialized_data = {
            "jobs": serialize(jobs.object_list, job_fields)
        }
        return Http200(serialized_data)
    
    @check_json
    @authenticated
    def post(self, request, *args, **kwargs):
        """Endpoint for creating a new job or updating an existing job."""
        # Get user and append into json data
        user = get_user_model().objects.get(username=request.user.username)
        self.json_data['user'] = user

        # Extract stripe token from json data
        try:
            token = self.json_data.pop('token')
        except:
            return Http400('You did not include a token')
        
        # Generate job form
        job_form = JobForm(self.json_data)
        try: # to charge stripe
            description = "%s created a new job" % (request.user.username,)
            stripe.Charge.create(
                amount=JOB_COST,
                currency="usd",
                card=token,
                description=description
            )
        except:
            return Http400("Stripe had an error processing your card")

        # Check form for valid job post
        return_message = job_form.save()
        if "errors" in return_message:
            return Http400(return_message)
        return Http200(return_message)

class JobCompanyList(View):
    """Returns a list of jobs posted by a company"""

    def get(self, request, *args, **kwargs):
        """Returns a company's jobs posted."""
        company_slug = kwargs.get('company_slug')
        model_filters = {"company_slug": company_slug, "is_expired": False}
        jobs = paginate(request=request, model=Job,
            model_filters=model_filters)
        job_fields = ["title", "company", "company_url", "company_slug", "pk",
            ("description", lambda obj: obj.get_short_description()),
            ("date_created", lambda obj: obj.date_created.strftime(
                "%B %d, %Y"))
        ]
        serialized_data = {
            "jobs": serialize(jobs.object_list, job_fields)
        }
        return Http200(serialized_data)
     
class JobDetail(View):
    """API endpoint for returning a job."""
    def get(self, request, *args, **kwargs):
        """Returns a job"""
        try: # Check that job exists
            pk = kwargs.get('pk', -1)
            job = Job.objects.get(pk=pk)
        except:
            return Http404("This job does not exist")

        job_fields = ["title", "company", "company_url", "description",
            ("username", lambda obj: obj.user.username),
            ("date_created", lambda obj: obj.date_created.strftime(
                "%B %d, %Y")),
        ]
        serialized_data = serialize(job, job_fields)
        return Http200(serialized_data)
    
    @check_json
    @authenticated_and_authorized(model=Job, model_filters=["pk"])
    def put(self, request, *args, **kwargs):
        """Updates a job"""
        user = get_user_model().objects.get(username=request.user.username)
        self.json_data['user'] = user
        pk = kwargs.get('pk')
        job = Job.objects.get(pk=pk)
        return create_or_update_job(self.json_data, job=job)

    @authenticated_and_authorized(model=Job, model_filters=["pk"])
    def delete(self, request, *args, **kwargs):
        """Deletes a job post"""
        pk = kwargs.get('pk')
        job = Job.objects.get(pk=pk)
        job.delete()
        return Http200()

class RenewJob(View):
    """API endpoint for renewing a job post."""
    
    @check_json
    @authenticated_and_authorized(model=Job, model_filters=["pk"])
    def post(self, request, *args, **kwargs):
        """Renews a post if it is within 5 days of expiring."""
        # Charge stripe first
        try:
            description = "%s created a new job" % (request.user.username,)
            stripe.Charge.create(
                amount=JOB_COST,
                currency="usd",
                card=self.json_data.get('token'),
                description=description
            )
        except:
            return Http400("Stripe had an error processing your card")
        
        # Renew listing
        pk = kwargs.get('pk')
        job = Job.objects.get(pk=pk)
        job.renew_listing()
        return Http200()
