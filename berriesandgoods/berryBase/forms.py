from django import forms
from home.models import Review


class AddToCartForm(forms.Form):
    amount = forms.FloatField(required=True, min_value=0.01)


class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "content": forms.Textarea(attrs={"cols": 80, "rows": 10})
        }


class SearchForm(forms.Form):
    search = forms.CharField(label="Search", max_length=50)
