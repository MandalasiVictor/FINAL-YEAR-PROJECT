from django import forms
from ..models import Integration

class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(), # render password field as password input
        }