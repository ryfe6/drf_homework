from rest_framework import serializers
from ims.validators import ValidateGoodUrl

from ims.models import Lesson, Course, Subscription


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[ValidateGoodUrl()])

    class Meta:
        model = Lesson
        fields = ("id", "name", "course", "url")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("user", "course")


class CourseSerializer(serializers.ModelSerializer):
    count_lesson_in_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription = SubscriptionSerializer(
        source="subscription_set", many=True, read_only=True
    )

    class Meta:
        model = Course
        fields = ("id", "name", "lesson", "subscription", "count_lesson_in_course")

    def get_count_lesson_in_course(self, instance):
        if instance.lesson_set.all().count():
            return instance.lesson_set.all().count()
        return 0
