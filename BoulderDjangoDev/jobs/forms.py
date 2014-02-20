"""Forms module for creating and editing jobs."""

from django import forms
from utils.fields.form_fields import DjangoDevField
from .models import Job

import json

class JobForm(forms.ModelForm):
    """For for validating Jobs. Save is overridden to return a JSON document"""
    user = DjangoDevField()
    
    class Meta:
        model = Job
        fields = ['title', 'company', 'company_url', 'description', 'user']
    
    def save(self, commit=True):
        """Saves the job and returns a JSON document displaying whether or
        not it was successful. If there was an error, there will be a field
        called 'error' included in the document."""
        try:
            job = super().save(commit=commit)
        except:
            error_dict = dict(self.errors.items())
            errors = [error[0] for error in error_dict.values()
                if len(error) > 0]
            return {"errors": errors}
        return {
            "title": self.cleaned_data.get('title'),
            "company": self.cleaned_data.get('company'),
            "company_url": self.cleaned_data.get('company_url'),
            "description": self.cleaned_data.get('description'),
            "pk": job.pk,
            "company_slug": job.company_slug,
            "url": job.get_url()
        }
