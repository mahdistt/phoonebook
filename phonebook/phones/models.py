from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex='09(0[1-2]|1[0-9]|3[0-9]|2[0-1])-?[0-9]{3}-?[0-9]{4}', message='phone number invalid')


class Entry(models.Model):
    """
    An entry in the phonebook
    """
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
