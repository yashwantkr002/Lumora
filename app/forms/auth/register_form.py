from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from app.models.user import CustomUser

# Reusable Tailwind class string to keep your code DRY (Don't Repeat Yourself)
TAILWIND_INPUT_CLASS = "w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-primary focus:ring-1 focus:ring-primary dark:border-slate-700 dark:bg-slate-800 dark:text-white"

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS, "placeholder": "Username","id": "username","autocomplete": "username",})
    )
    
    email = forms.EmailField(
        required=True,  # Crucial: Forces the user to provide an email
        widget=forms.EmailInput(attrs={"class": TAILWIND_INPUT_CLASS, "placeholder": "Email Address","id": "email","autocomplete": "email",})
    )
    
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS, "placeholder": "First Name","id": "firstName", "autocomplete": "given-name",})
    )
    
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": TAILWIND_INPUT_CLASS, "placeholder": "Last Name","id": "lastName", "autocomplete": "family-name",})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT_CLASS + " pr-12", "placeholder": "Password","id": "password", "autocomplete": "new-password",})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": TAILWIND_INPUT_CLASS + " pr-12", "placeholder": "Confirm Password","id": "confirmPassword", "autocomplete": "new-password",})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        # Attach the error specifically to the confirm_password field
        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        # Get the instance but don't save it to the DB yet
        user = super().save(commit=False)
        
        # Securely hash the password before saving
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user