from django import forms


class AddToCartForm(forms.Form):
    amount = forms.IntegerField(required=True, min_value=1)
