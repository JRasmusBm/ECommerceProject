from django import forms


class ChangeAmount(forms.Form):
    amount = forms.IntegerField(label="", min_value=1)
