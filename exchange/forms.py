from django import forms

from .models import Rate


class RateForm(forms.Form):
    class Meta:
        models = Rate
        fields = []
