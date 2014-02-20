from config import ALPHANUMERIC_REGEX
from django import forms
from .models import DjangoDev

class UserForm(forms.ModelForm):
    """User form"""
    username = forms.RegexField(
        regex=ALPHANUMERIC_REGEX,
        max_length=65,
        error_messages={
            'invalid': 'A username can only contain alphanumeric characters, '
            'periods, hyphens, and underscores.'
        }
   )
    class Meta:
        model = DjangoDev
        exclude = ['image', 'is_company', 'is_active',
            'is_admin', 'last_updated', 'last_login', 'password']
    
    def save(self, commit=True):
        """Saves a JSON reprentation of the data"""
        try:
            user = super().save(commit=commit)
        except:
            error_dict = dict(self.errors.items())
            errors = [error[0] for error in error_dict.values()
                if len(error) > 0]
            return {"errors": errors}
        return {
            "username": self.cleaned_data.get('username'),
            "job_title": self.cleaned_data.get('job_title'),
            "company": self.cleaned_data.get('company'),
            "interests": self.cleaned_data.get('interests'),
            "email": self.cleaned_data.get('email'),
            "website": self.cleaned_data.get('website')
        }
