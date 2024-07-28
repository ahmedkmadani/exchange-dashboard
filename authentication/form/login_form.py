"""Module for the 'LoginForm' class."""
from django import forms
from django.contrib.auth import authenticate

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

    def clean(self):
        """Override clean method to add custom validation."""
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if user is None:
                raise forms.ValidationError("Invalid phone number or password.")
        return cleaned_data
