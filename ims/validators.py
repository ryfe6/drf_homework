from rest_framework.serializers import ValidationError


class ValidateGoodUrl:
    good_url = "https://www.youtube.com"

    def __call__(self, value):
        if self.good_url not in value.lower():
            raise ValidationError(f"Ссылка должна начинаться с {self.good_url}")
