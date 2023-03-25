from django.core.exceptions import ValidationError


FORBIDDEN_NAMES = ('me', 'ME', 'Me', 'mE')


def validate_username(value):
    if value in FORBIDDEN_NAMES:
        raise ValidationError(
            f'Использовать имя {value} в качестве username запрещено')
    return value
