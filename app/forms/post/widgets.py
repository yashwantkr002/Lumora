"""
===========================================================
File: app/forms/widgets.py
===========================================================

Reusable form widgets.

===========================================================
"""

from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    """
    Django 5.x / 6.x compatible multiple file widget.
    """

    allow_multiple_selected = True