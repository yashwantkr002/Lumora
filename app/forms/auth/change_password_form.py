from django import forms


class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        widget=forms.PasswordInput
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean(self):

        cleaned = super().clean()

        if cleaned.get("new_password") != cleaned.get(
            "confirm_password"
        ):

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned