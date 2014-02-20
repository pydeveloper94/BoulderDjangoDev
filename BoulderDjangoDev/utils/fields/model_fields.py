from django.core.exceptions import ValidationError
from django.db import models
from decimal import Decimal

import re

class CurrencyField(models.DecimalField):
    """
    Thanks Will Hardy. http://is.gd/Z1SOPU
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        return super(
            CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
            
class UsernameField(models.CharField):
    """
    Allows users to have alphanumeric characters, hyphens, underscores, and
    periods in their usernames.
    """
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        value = super().to_python(value)
        if not re.match(r'[A-z0-9\-\_\.]+', value):
            raise ValidationError('Only alphanumeric characters, hyphens, '
                'underscores, and periods are valid.', code='invalid')
        return value
