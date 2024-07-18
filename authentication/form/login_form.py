"""Module for the 'LoginForm' class."""
from django import forms

from validators.validators import FileValidator


class LoginForm(forms.Form):
    """User login form."""

    phone_number = forms.CharField(
        label="Phone number",
        validators=[FileValidator.phone_number_validator],
        widget=forms.TextInput(attrs={"placeholder": "512 345 678"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "•••••••••", "aria-describedby": "password"}
        ),
    )
