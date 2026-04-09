from django import forms


class HistoryForm(forms.Form):
    history_text = forms.CharField(label='Enter text', max_length=100)
