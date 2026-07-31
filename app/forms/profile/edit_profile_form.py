from django import forms
from django.contrib.auth import get_user_model

from app.models.user import UserProfile

User = get_user_model()

INPUT_CLASS = (
    "w-full rounded-xl border border-slate-300 "
    "bg-white px-4 py-3 text-slate-900 "
    "placeholder:text-slate-400 "
    "focus:border-primary focus:ring-2 "
    "focus:ring-primary/20 "
    "dark:border-slate-700 "
    "dark:bg-slate-800 "
    "dark:text-white"
)

TEXTAREA_CLASS = (
    "w-full rounded-xl border border-slate-300 "
    "bg-white px-4 py-3 text-slate-900 "
    "placeholder:text-slate-400 "
    "focus:border-primary focus:ring-2 "
    "focus:ring-primary/20 "
    "dark:border-slate-700 "
    "dark:bg-slate-800 "
    "dark:text-white resize-none"
)


class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "firstName",
                "class": INPUT_CLASS,
                "placeholder": "First Name",
                "autocomplete": "given-name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "lastName",
                "class": INPUT_CLASS,
                "placeholder": "Last Name",
                "autocomplete": "family-name",
            }
        ),
    )

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "id": "username",
                "class": INPUT_CLASS,
                "placeholder": "Username",
                "autocomplete": "username",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "class": INPUT_CLASS,
                "placeholder": "Email Address",
                "autocomplete": "email",
            }
        ),
    )

    class Meta:

        model = UserProfile

        fields = [
            "avatar",
            "cover_image",
            "first_name",
            "last_name",
            "username",
            "email",
            "bio",
            "website",
            "location",
            "profession",
        ]

        widgets = {

            "avatar": forms.FileInput(
                attrs={
                    "id": "avatar",
                    "class": INPUT_CLASS,
                    "accept": "image/*",
                }
            ),

            "cover_image": forms.FileInput(
                attrs={
                    "id": "coverImage",
                    "class": INPUT_CLASS,
                    "accept": "image/*",
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "id": "bio",
                    "rows": 4,
                    "maxlength": 150,
                    "class": TEXTAREA_CLASS,
                    "placeholder": "Tell people about yourself...",
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "id": "website",
                    "class": INPUT_CLASS,
                    "placeholder": "https://example.com",
                    "autocomplete": "url",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "id": "location",
                    "class": INPUT_CLASS,
                    "placeholder": "Your Location",
                    "autocomplete": "address-level2",
                }
            ),

            "profession": forms.TextInput(
                attrs={
                    "id": "profession",
                    "class": INPUT_CLASS,
                    "placeholder": "Profession",
                    "autocomplete": "organization-title",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if self.user:

            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["username"].initial = self.user.username
            self.fields["email"].initial = self.user.email

    def clean_bio(self):

        bio = self.cleaned_data.get("bio", "").strip()

        if len(bio) > 150:
            raise forms.ValidationError(
                "Bio cannot exceed 150 characters."
            )

        return bio

    def clean_website(self):

        website = self.cleaned_data.get("website", "")

        return website.strip()

    def clean_username(self):

        username = self.cleaned_data["username"]

        if (
            self.user
            and User.objects.exclude(pk=self.user.pk)
            .filter(username=username)
            .exists()
        ):
            raise forms.ValidationError(
                "Username already exists."
            )

        return username

    def clean_email(self):

        email = self.cleaned_data["email"]

        if (
            self.user
            and User.objects.exclude(pk=self.user.pk)
            .filter(email=email)
            .exists()
        ):
            raise forms.ValidationError(
                "Email already exists."
            )

        return email