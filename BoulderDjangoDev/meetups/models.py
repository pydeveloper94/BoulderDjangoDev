from django.db import models

class Meetup(models.Model):
    """Model for Boulder Django meetups."""
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=75, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    event_url = models.URLField(max_length=255, blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    meetup_id = models.IntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ['-date']
