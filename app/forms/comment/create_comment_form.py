"""
===========================================================
File: app/forms/comment/create_comment_form.py
===========================================================

PURPOSE

Form for creating comments.

===========================================================
"""

from django import forms

from app.models.comment import Comment


class CreateCommentForm(forms.ModelForm):
    """
    Form for creating a comment.
    """

    class Meta:

        model = Comment

        fields = [
            "content",
        ]

        widgets = {

            "content": forms.Textarea(

                attrs={

                    "rows": 3,

                    "placeholder": "Write a comment...",

                    "class": (
                        "w-full rounded-xl border "
                        "border-slate-300 p-3 "
                        "focus:border-primary "
                        "focus:outline-none "
                        "dark:border-slate-700 "
                        "dark:bg-slate-900"
                    ),

                }

            ),

        }

    # -------------------------------------------------------
    # Validation
    # -------------------------------------------------------

    def clean_content(self):
        """
        Validate comment content.
        """

        content = self.cleaned_data["content"].strip()

        if not content:

            raise forms.ValidationError(
                "Comment cannot be empty."
            )

        return content