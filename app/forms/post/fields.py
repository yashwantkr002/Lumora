"""
===========================================================
File: app/forms/fields.py
===========================================================

Reusable custom form fields.

===========================================================
"""

from django import forms

from .widgets import MultipleFileInput


class MultipleFileField(forms.FileField):
    """
    Accept multiple uploaded files.
    """

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned = []

        for file in data:
            cleaned.append(
                super().clean(
                    file,
                    initial,
                )
            )

        return cleaned