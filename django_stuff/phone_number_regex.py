from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r'[+]?\d{10,14}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
