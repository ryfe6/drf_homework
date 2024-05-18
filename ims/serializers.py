from rest_framework import serializers
from ims.validators import validate_good_url

from ims.models import Lesson, Course, Subscription


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validate_good_url])

    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "course",
            "url"
        )


class CourseSerializer(serializers.ModelSerializer):
    count_lesson_in_course = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = ("name", "lesson", "count_lesson_in_course")

    def get_count_lesson_in_course(self, instance):
        if instance.lesson_set.all().count():
            return instance.lesson_set.all().count()
        return 0


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
