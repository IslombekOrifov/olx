from django.core.validators import RegexValidator, EmailValidator


validate_phone = RegexValidator(
    regex=r'^\+998\d{9}$',
    message='Raqam 13 ta belgidan iborat bolishi kerak. P.s: +998912345678'
)

validate_email = EmailValidator()