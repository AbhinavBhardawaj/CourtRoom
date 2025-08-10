from django import forms
from .models import Court
from django.utils import timezone

CASE_TYPE_CHOICES=[
    ('CRL', 'Criminal'),
    ('CIV', 'Civil'),
    ('FAO', 'First Appeal'),
    ('CRL.A', 'Criminal Appeal'),
    ('CRL.M.C', 'Criminal Misc'),
    ('W.P.(C)', 'Writ Petition (Civil)'),
    ('W.P.(CRL)', 'Writ Petition (Criminal)'),
    ('CS(COMM)', 'Commercial Suit'),
    ('OTHER', 'Other'),
]

class CaseSearchForm(forms.Form):
    court = forms.ModelChoiceField(
        queryset=Court.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-control bg-white text-gray-900 border border-gray-300 rounded px-3 py-2'
        })
    )
    case_type = forms.ChoiceField(
        choices=CASE_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control bg-white text-gray-900 border border-gray-300 rounded px-3 py-2'
        })
    )
    case_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-white text-gray-900 border border-gray-300 rounded px-3 py-2',
            'placeholder': 'Enter case number (e.g., 123)'
        })
    )
    filing_year = forms.IntegerField(
        min_value=1950,
        max_value=2030,
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-white text-gray-900 border border-gray-300 rounded px-3 py-2',
            'placeholder': '2024'
        })
    )
    
    def clean_filing_year(self):
        year = self.cleaned_data['filing_year']
        if year > timezone.now().year:
            raise forms.ValidationError("Filing year cannot be in the future.")
        return year