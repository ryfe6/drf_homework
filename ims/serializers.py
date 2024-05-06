from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ims.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "course",
        )


class CourseSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson = LessonSerializer(source="lesson_set", many=True)

    class Meta:
        model = Course
        fields = ("name", "lesson", "count_lesson_in_course")

    def get_count_lesson_in_course(self, instance):
        if instance.lesson_set.all().count():
            return instance.lesson_set.all().count()
        return 0
