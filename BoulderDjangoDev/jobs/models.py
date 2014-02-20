from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
from utils.urls import reverse_url

RENEW_DAYS = 45
RENEWAL_PERIOD = 7

class Job(models.Model):
    """Job listings model"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=75)
    company = models.CharField(max_length=75)
    company_slug = models.CharField(max_length=75)
    company_url = models.URLField(max_length=255, blank=True, null=True)
    description = models.TextField()
    date_created = models.DateTimeField()
    date_to_delete = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overrides default save method to include the date_to_delete"""
        if not self.date_to_delete:
            self.date_created = datetime.utcnow().replace(tzinfo=utc)
            self.date_to_delete = self.date_created + \
                timedelta(days=RENEW_DAYS)
        self.company_slug = slugify(self.company)
        super().save(*args, **kwargs)

    def calculate_end_date(self, days):
        """Calculates the end date for a job listing."""
        return datetime.now() + timedelta(days=days)
        
    def renew_listing(self):
        """Adds additional months to a job listing."""
        self.date_to_delete = self.date_to_delete + timedelta(days=RENEW_DAYS)
    
    def get_short_description(self):
        """Returns the first 200 words in the description"""
        return "%s" % (" ".join(self.description.split(" ")[:200]),)

    def get_company_url(self):
        """Returns the url for the company"""
        return reverse_url('job-company-list', args=[self.company_slug])

    def get_url(self):
        """Returns a url to the job listing's page."""
        return reverse_url('job-detail', args=[self.pk])

    class Meta:
        ordering = ['-date_to_delete']
