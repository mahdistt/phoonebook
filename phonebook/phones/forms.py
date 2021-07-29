from django import forms

from . import models


class EntryForm(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = (
            'name',
            'last_name',
            'phone_number',

        )
        widgets = {
            'phone_number': forms.NumberInput
        }


class ProfileFrom(forms.ModelForm):
    class Meta:
        model = models.Entry
        fields = (
            'creator',
        )
