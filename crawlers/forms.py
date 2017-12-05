from django import forms


class StartForm(forms.Form):
    pixnet_url = forms.URLField(required=True, label="痞客邦網址")

