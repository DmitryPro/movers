from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'from_address', 'to_address', 'date', 'time', 'move_type',
            'items_description', 'floors_from', 'floors_to'
        ]
