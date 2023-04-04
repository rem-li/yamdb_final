import datetime
import re

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            '%(value)s is not a correcrt year!',
            params={'value': value},
        )


def slug_validator(value):
    for i in value:
        if not re.search(r'^[\w.@+-]+$', i):
            raise ValidationError(
                f'Импользовать символ {i} в имени запрещено',
            )
