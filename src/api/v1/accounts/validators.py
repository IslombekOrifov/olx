from django.core.validators import RegexValidator, EmailValidator


validate_phone = RegexValidator(
    regex=r'^\+998\d{9}$',
    message='Raqam 13 ta belgidan iborat bolishi kerak. P.s: +998912345678'
)

validate_email = EmailValidator()

validate_phone_and_email = RegexValidator(
    regex=r'^[+]998\d{9}|(^[a-zA-Z0-9]{6,30}@[a-zA-Z]{3,63}[.][a-zA-Z]{2,10}$)',
    message="""
        Telefon raqam: 13 ta belgidan iborat bolishi kerak. P.s: +998912345678
        Email: aaaa@gmail.com ko'rinishida bo'lishi kerak!
    """
)
