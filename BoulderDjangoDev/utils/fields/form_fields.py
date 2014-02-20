from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from utils.errors import UnspecifiedModelFieldError

from blog.models import BlogPost
from users.models import DjangoDev

class ModelField(forms.Field):
    """Generic form field for validating a foreignkey of a model. This field
    does not serialize the attached object, but will check if the object is
    already saved into the database.
    """
    model = models.Model
    def __init__(self, required=True, label=None,
            initial=None, widget=None, help_text=''):
        if self.model == models.Model:
            raise UnspecifiedModelFieldError("You have created a model field "
                "called: %s, and have not specified a model. Please set the "
                "class variable model, which is inherited from ModelField, to "
                "your desired model class." % (self.__class__.__name__)) 
        super().__init__(required=required, label=label, initial=initial,
            widget=widget, help_text=help_text)

    def clean(self, obj):
        try:
            pk = obj.pk
        except AttributeError:
            raise ValidationError("You cannot pass a model object without a "
                "pk.")
        try:
            return_obj = self.model.objects.get(pk=pk)
            return return_obj
        except self.Model.DoesNotExist:
            raise ValidationError("You cannot pass a model that has not been "
                "instantiated into the database.")

class DjangoDevField(ModelField):
    model = DjangoDev

class BlogPostField(ModelField):
    model = BlogPost

