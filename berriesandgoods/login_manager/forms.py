from django import forms
from home.models import Users


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["email", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }
