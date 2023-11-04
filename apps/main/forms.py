from django import forms
from . import models


class ContractorForm(forms.Form):
    ...
    class Meta:
        model = models.Contractor
        fields = ['title', 'category']