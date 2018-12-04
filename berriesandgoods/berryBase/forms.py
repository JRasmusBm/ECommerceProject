from django import forms


class AddToCartForm(forms.Form):
    amount = forms.FloatField(required=True, min_value=0.01)
