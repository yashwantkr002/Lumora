from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Type a message..."}),
    )
