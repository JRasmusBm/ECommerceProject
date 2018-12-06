from django import forms
from home.models import Review


class AddToCartForm(forms.Form):
    amount = forms.IntegerField(required=True, min_value=1)


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "content": forms.Textarea(attrs={"cols": 80, "rows": 10})
        }
