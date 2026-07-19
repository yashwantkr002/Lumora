"""
===========================================================
File: app/forms/post/create_post_form.py
===========================================================

PURPOSE

Create a new social media post.

Supports

• Carousel
• Multiple Images
• One Video
• Mixed Media
• Hashtags

===========================================================
"""

from django import forms

from app.forms.post.fields import MultipleFileField
from app.models.post import Post


class CreatePostForm(forms.ModelForm):

    media = MultipleFileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*,video/*",
            }
        ),
    )

    hashtags = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.TextInput(
            attrs={
                "placeholder": "#python #django #lumora",
            }
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
                    "placeholder": "What's happening?",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "Add location",
                }
            ),

        }

    def clean_media(self):

        media = self.cleaned_data["media"]

        if not media:

            raise forms.ValidationError(
                "Please upload at least one media file."
            )

        if len(media) > 10:

            raise forms.ValidationError(
                "Maximum 10 media files are allowed."
            )

        image_count = 0
        video_count = 0

        for file in media:

            content_type = (
                file.content_type or ""
            )

            if content_type.startswith("image/"):

                image_count += 1

            elif content_type.startswith("video/"):

                video_count += 1

            else:

                raise forms.ValidationError(
                    f"{file.name} is not supported."
                )

        if video_count > 1:

            raise forms.ValidationError(
                "Only one video is allowed."
            )

        return media

    def clean_caption(self):

        return (
            self.cleaned_data.get(
                "caption",
                "",
            ).strip()
        )

    def clean_hashtags(self):

        hashtags = self.cleaned_data.get(
            "hashtags",
            "",
        )

        return " ".join(
            hashtags.split()
        )

    def clean(self):

        return super().clean()