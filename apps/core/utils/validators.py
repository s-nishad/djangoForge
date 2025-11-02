import re
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.translation import gettext_lazy as _


ONE_MB = 1024 * 1024


def is_valid_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    return re.fullmatch(regex, email) is not None


def file_upload_validator(value: File):
    try:
        if value.size > 5 * ONE_MB:
            raise ValidationError(
                _('File size must be lower than 5MB'),
                params={'value': value},
            )
    except FileNotFoundError:
        pass

    return None