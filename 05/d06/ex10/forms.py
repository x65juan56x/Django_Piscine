from django import forms
from .models import People


class FilterForm(forms.Form):
    min_date = forms.DateField(label='Movies minimum release date', widget=forms.DateInput(attrs={'type': 'date'}))
    max_date = forms.DateField(label='Movies maximum release date', widget=forms.DateInput(attrs={'type': 'date'}))
    planet_diameter = forms.IntegerField(label='Planet diameter greater than')

    gender = forms.ChoiceField(label='Character gender', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            genders = People.objects.values_list('gender', flat=True).distinct()
            self.fields['gender'].choices = [(g, g) for g in genders if g]
        except Exception:
            self.fields['gender'].choices = []
