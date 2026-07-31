from django import forms

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=150,
        required=True,
        label="Username or Email",  # Correct placement for label
        widget=forms.TextInput(
            attrs={
                "class":"w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white", # Update this if using Tailwind
                "placeholder": "Username or Email",
                "autocomplete": "username",
                "id": "usernameOrEmail",
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label="Password",  # Correct placement for label
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white", # Update this if using Tailwind
                "placeholder": "Password",
                "autocomplete": "current-password",
                "id": "password",
            }
        ),
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Remember Me",
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input", # Standard class for checkboxes
                "id": "rememberMe",
            }
        )
    )