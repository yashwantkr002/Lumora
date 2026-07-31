"""
===========================================================
File: app/forms/post/create_post_form.py
===========================================================

PURPOSE

Create a new social media post.

Supports

• Text Post
• Image Post (1–10)
• Video Post (1)
• Caption
• Location
• Visibility
• Comments
• Download Permission

===========================================================
"""

from django import forms

from app.forms.post.fields import MultipleFileField
from app.models.post import Post


INPUT_CLASS = (
    "w-full rounded-xl border border-slate-300 "
    "bg-slate-50 px-4 py-3 text-slate-900 "
    "outline-none transition "
    "focus:border-primary focus:ring-1 focus:ring-primary "
    "dark:border-slate-700 dark:bg-slate-800 dark:text-white"
)


TEXTAREA_CLASS = (
    "w-full rounded-xl border border-slate-300 "
    "bg-slate-50 px-4 py-3 text-slate-900 "
    "outline-none transition resize-none "
    "focus:border-primary focus:ring-1 focus:ring-primary "
    "dark:border-slate-700 dark:bg-slate-800 dark:text-white"
)


CHECKBOX_CLASS = (
    "h-4 w-4 rounded border-slate-300 "
    "text-primary focus:ring-primary"
)


class CreatePostForm(forms.ModelForm):

    media = MultipleFileField(
        required=True,
        label="Photos or Video",
        help_text="Upload up to 10 images or 1 video.",
        widget=forms.ClearableFileInput(
            attrs={
                "id": "media",
                "accept": "image/*,video/*",
                "class": INPUT_CLASS,
            }
        ),
    )

    allow_comments = forms.BooleanField(
        required=False,
        label="Allow Comments",
        widget=forms.CheckboxInput(
            attrs={
                "id": "allow-comments",
                "class": CHECKBOX_CLASS,
            }
        ),
    )

    allow_download = forms.BooleanField(
        required=False,
        label="Allow Download",
        widget=forms.CheckboxInput(
            attrs={
                "id": "allow-download",
                "class": CHECKBOX_CLASS,
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
                    "id": "caption",
                    "rows": 5,
                    "maxlength": 2200,
                    "placeholder": "What's happening?",
                    "class": TEXTAREA_CLASS,
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "id": "location",
                    "placeholder": "Add location",
                    "class": INPUT_CLASS,
                }
            ),

            "visibility": forms.Select(
                attrs={
                    "id": "visibility",
                    "class": INPUT_CLASS,
                }
            ),

        }

    def clean_media(self):

        media = self.cleaned_data.get("media", [])

        if not media:
            raise forms.ValidationError(
                "Please upload at least one media file."
            )

        if len(media) > 10:
            raise forms.ValidationError(
                "You can upload a maximum of 10 files."
            )

        image_count = 0
        video_count = 0

        for file in media:

            content_type = (file.content_type or "").lower()

            if content_type.startswith("image/"):
                image_count += 1

            elif content_type.startswith("video/"):
                video_count += 1

            else:
                raise forms.ValidationError(
                    f'"{file.name}" is not a supported media file.'
                )

        if image_count and video_count:
            raise forms.ValidationError(
                "You cannot upload images and a video in the same post."
            )

        if video_count > 1:
            raise forms.ValidationError(
                "Only one video is allowed."
            )

        return media

    def clean_caption(self):

        caption = self.cleaned_data.get(
            "caption",
            "",
        )

        return caption.strip()

    def clean(self):

        cleaned_data = super().clean()

        return cleaned_data