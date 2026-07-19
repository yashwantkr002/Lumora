"""
===========================================================
File: app/forms/post/update_post_form.py
===========================================================

PURPOSE

Update an existing post.

Supports

• Caption
• Media Replacement
• Location
• Visibility
• Post Settings

===========================================================
"""

from django import forms

from app.forms.post.fields import MultipleFileField
from app.forms.post.widgets import MultipleFileInput
from app.models.post import Post


class UpdatePostForm(forms.ModelForm):
    """
    Form for updating an existing post.
    """

    media = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "accept": "image/*,video/*",
            }
        ),
        help_text=(
            "Upload new media to replace the existing media."
        ),
    )

    class Meta:

        model = Post

        fields = [
            "caption",
            "location",
            "visibility",
            "allow_comments",
            "allow_download",
        ]

        widgets = {

            "caption": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Update your caption...",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "Add location",
                }
            ),

        }

    # -------------------------------------------------------
    # Caption
    # -------------------------------------------------------

    def clean_caption(self):

        return self.cleaned_data.get(
            "caption",
            "",
        ).strip()

    # -------------------------------------------------------
    # Media
    # -------------------------------------------------------

    def clean_media(self):

        media = self.cleaned_data.get(
            "media",
            [],
        )

        if not media:

            return media

        if len(media) > 10:

            raise forms.ValidationError(
                "Maximum 10 media files are allowed."
            )

        video_count = 0

        for file in media:

            content_type = (
                file.content_type or ""
            )

            if content_type.startswith(
                "image/"
            ):

                continue

            if content_type.startswith(
                "video/"
            ):

                video_count += 1

                continue

            raise forms.ValidationError(
                f"{file.name} is not a supported media file."
            )

        if video_count > 1:

            raise forms.ValidationError(
                "Only one video is allowed per post."
            )

        return media

    # -------------------------------------------------------
    # Cross-field Validation
    # -------------------------------------------------------

    def clean(self):

        return super().clean()