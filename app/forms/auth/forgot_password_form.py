from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ForgotPasswordForm(forms.Form):
    """
    Form for requesting a password reset email.
    """

    email = forms.EmailField(
        max_length=User._meta.get_field("email").max_length,
        widget=forms.EmailInput(
            attrs={
                "class":"w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white",
                "placeholder": "Enter your email",
                "label": "Email Address",
                "autocomplete": "email",
                "spellcheck": "false",
                "autofocus": True,
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if not email:
            raise forms.ValidationError(
                "Email is required."
            )

        # Enumeration attack avoid karne ke liye
        
        # yahan user existence check nahi karte.
        return email