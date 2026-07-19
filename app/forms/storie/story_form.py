from django import forms

from app.models.story import Story


class StoryForm(forms.ModelForm):
    """
    Create story.
    """

    class Meta:

        model = Story

        fields = [
            "image",
            "video",
        ]

    def clean(self):

        cleaned_data = super().clean()

        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        if not image and not video:

            raise forms.ValidationError(
                "Please upload an image or a video."
            )

        if image and video:

            raise forms.ValidationError(
                "Upload either image or video."
            )

        return cleaned_data