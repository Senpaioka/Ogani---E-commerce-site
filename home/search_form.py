from django import forms


class ProductSearchForm(forms.Form):
    search_key = forms.CharField(max_length=100, required=True)
