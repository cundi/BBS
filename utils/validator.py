import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django import forms


def password_validator(password):
    if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        # match
        return True
    else:
        # no match
        return False


def email_validator(email):
    try:
        validate_email(email)
        return email
    except ValidationError:
        return False


def email_validator_2(email):
    f = forms.EmailField()
    clean_email = f.clean(email)
    return clean_email


def cleaned_data():
    pass


def form_validator(req_post):
    pass
