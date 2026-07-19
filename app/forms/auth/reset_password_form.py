from django import forms
from django.contrib.auth.password_validation import validate_password


class ResetPasswordForm(forms.Form):
    """
    Form for resetting password.
    """

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class":"w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white",
                "placeholder": "New Password",
                "autocomplete": "new-password",
            }
        ),
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class":"w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
            }
        ),
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")

        validate_password(new_password)

        return new_password

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if (
            new_password
            and confirm_password
            and new_password != confirm_password
        ):
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data
