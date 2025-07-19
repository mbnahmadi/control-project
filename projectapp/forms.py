from django import forms

class ProjectFilterForm(forms.Form):
    company_name = forms.CharField(required=False, label='Company Name')
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
