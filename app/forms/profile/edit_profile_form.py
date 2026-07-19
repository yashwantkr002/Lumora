from django import forms

from app.models.user import UserProfile


class EditProfileForm(forms.ModelForm):
    """
    Update user profile.
    """

    class Meta:

        model = UserProfile

        fields = [
            "avatar",
            "cover_image",
            "bio",
            "website",
            "location",
            "profession",
        ]

        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write something about yourself...",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "placeholder": "Your location",
                }
            ),
            "profession": forms.TextInput(
                attrs={
                    "placeholder": "Profession",
                }
            ),
        }

    def clean_bio(self):

        bio = self.cleaned_data.get("bio")

        if bio and len(bio) > 150:

            raise forms.ValidationError(
                "Bio cannot exceed 150 characters."
            )

        return bio

    def clean_website(self):

        website = self.cleaned_data.get("website")

        return website.strip() if website else website