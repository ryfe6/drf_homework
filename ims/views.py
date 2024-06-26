import datetime

from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ims.models import Course, Lesson, Subscription
from ims.paginations import CustomPagination
from ims.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsAuthor, IsModer
from ims.tasks import check_update


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.author = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action in ["destroy"]:
            self.permission_classes = (IsAuthenticated, ~IsModer, IsAuthor)
        elif self.action in [
            "update",
            "retrieve",
        ]:
            self.permission_classes = (IsAuthenticated, IsModer | IsAuthor)
        return super().get_permissions()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # После сохранения изменений в курсе, вызываем задачу Celery.
        course_id = serializer.instance.id
        course_name = serializer.instance.name
        check_update.delay(course_id, course_name)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course = serializer.save()
        course.author = self.request.user
        course.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsAuthor]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsAuthor]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class SubscriptionCreateView(CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        if Subscription.objects.filter(user=user, course=course_item).exists():
            Subscription.objects.get(user=user, course=course_item).delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
