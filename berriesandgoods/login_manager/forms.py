from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from home.models import Users


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["email", "password"]
        widgets = {"password": forms.PasswordInput()}


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    display_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Users
        fields = ["email", "display_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user


class ChangeUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    display_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Users
        fields = ("email", "password", "admin", "display_name")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = ChangeUserForm
    add_form = CreateUserForm

    list_display = ("email", "display_name", "admin")
    list_filter = ("admin",)
    fieldsets = (
        (None, {"fields": ("email", "display_name", "password")}),
        ("Permissions", {"fields": ("admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "display_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()
