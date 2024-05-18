from rest_framework.serializers import ValidationError


good_url = "https://www.youtube.com"


def validate_good_url(value):
    if good_url not in value.lower():
        raise ValidationError(f"Ссылка должна начинаться с {good_url}")