from django import forms
from .models import WastePlastic, WastePlasticRequestor, FeedBack

class WastePlasticForm(forms.ModelForm):
    class Meta:
        model = WastePlastic
        fields = ['user', 'wastePlastic_type', 'wastePlastic_size', 'pickUp_status']

class WastePlasticRequestorForm(forms.ModelForm):
    class Meta:
        model = WastePlasticRequestor
        fields = ['requestor', 'wastePlastic_type', 'wastePlastic_size', 'wastePlastic_address', 'unique_location', 'latitude', 'longitude', 'pickUp_status']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['average_rating', 'comment']
        widgets = {
            'average_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'average_rating': 'Rating (1 to 5)',
            'comment': 'Your Comment',
        }

