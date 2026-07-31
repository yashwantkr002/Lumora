from django import forms

TAILWIND_INPUT_CLASS = "w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white"
class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "currentPassword",
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Current Password",
                "autocomplete": "current-password",
                "autofocus": True,
            }
        )
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "newPassword",
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "New Password",
                "autocomplete": "new-password",
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "confirmPassword",
                "class": TAILWIND_INPUT_CLASS,
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
            }
        )
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
