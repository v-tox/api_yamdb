import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(('Нельзя использовать имя пользователя me.'),)
    if not re.match(r'[\w.@+-]+\Z', value):
        raise ValidationError(
            'Нельзя использовать недопустимые символы'
        )
