from django import forms
from .models import *

class CheckoutContactForm(forms.Form):
    adress = forms.CharField(required=True)
    comment = forms.CharField(required=False)