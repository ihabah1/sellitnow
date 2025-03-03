from django import forms
from .models import Product  # Ensure Product model is correctly imported

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']  # Ensure these fields exist in Product model
