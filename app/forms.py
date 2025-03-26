from django import forms
from allauth.account.forms import LoginForm

from .models import Product  # Ensure Product model is correctly imported

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']  # Ensure these fields exist in Product model

        from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def clean_login(self):
        login = self.cleaned_data['login']
        return login  # This ensures it doesn't force an @ symbol
