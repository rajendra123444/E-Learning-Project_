from django import forms

from core.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Alias wrapper to keep registration logic separated from login template."""

    # no extra fields; inherits branch/semester/college from core.forms.UserCreationForm
    pass

