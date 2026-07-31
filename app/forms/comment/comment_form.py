from django import forms

from app.models.comment import Comment


class CommentForm(forms.ModelForm):
    """
    Create or update comment.
    """

    class Meta:

        model = Comment

        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Write a comment...",
                }
            ),
        }

    def clean_content(self):

        content = self.cleaned_data.get("content")

        if not content.strip():

            raise forms.ValidationError(
                "Comment cannot be empty."
            )

        return content.strip()