from django import forms


class BlogSearchForm(forms.Form):
    search_key = forms.CharField(max_length=100, required=True)