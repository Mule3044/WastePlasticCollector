from django import forms
from .models import WastePlastic, WastePlasticRequestor

class WastePlasticForm(forms.ModelForm):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'wastePlastic_size', 'pickUp_status']

class WastePlasticRequestorForm(forms.ModelForm):
    class Meta:
        model = WastePlasticRequestor
        fields = ['requestor', 'wastePlastic_type', 'wastePlastic_size', 'wastePlastic_address', 'unique_location', 'latitude', 'longitude', 'message', 'recent_activity', 'request_history']
